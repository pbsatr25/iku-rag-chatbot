"""
retriever.py
Pencarian chunk untuk chatbot IKU (lihat docs/02-desain/skema_embedding.md bagian B).

Tahapan (setiap fitur bisa dinyalakan terpisah agar dampaknya bisa diukur):
1. Dense     : bge-m3, ambil `candidates` kandidat (bukan langsung top_k)
2. Hybrid    : + BM25 (pencocokan kata persis: "IKU 4", "NUPTK", "MDPI"),
               digabung dengan Reciprocal Rank Fusion (RRF)
3. IKU boost : pertanyaan yang menyebut "IKU N" -> chunk IKU tsb dipastikan masuk
               kandidat dan didahulukan (sub-indikator / LLDIKTI dibedakan)
4. Dedupe    : isi kembar Bab V / Lampiran / PPT -> yang dipakai Bab V Buku; salinan
               lain dicatat di `also_in` (Lampiran sebagai dasar hukum)
5. Rerank    : (opsional) cross-encoder bge-reranker-v2-m3 mengurutkan ulang kandidat
6. Ambil top_k
7. Sambung   : potongan lanjutan tabel yang terambil disambung dengan potongan
               sebelumnya (lihat sambung_tabel.py)

Retriever() tanpa argumen = perilaku lama (dense saja + buang dokumen < 80 karakter).
Retriever.v2(...) = semua fitur best practice kecuali reranker.
"""

from pathlib import Path
import json
import math
import re
from collections import Counter

import chromadb
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from sambung_tabel import cari_lanjutan_tabel, gabung_tabel


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = PROJECT_ROOT / "data" / "vectorstore"

MODEL_NAME = "BAAI/bge-m3"
RERANKER_NAME = "BAAI/bge-reranker-v2-m3"
COLLECTION_NAME = "pmpt_qa"        # koleksi lama (v1)
COLLECTION_NAME_V2 = "pmpt_qa_v2"

RRF_K = 60
RERANK_DEPTH = 20
PRIMARY_SOURCE_PREFIX = "Buku"

STOPWORDS = set("""yang dan di ke dari untuk dengan atau pada dalam adalah ini itu berapa apa
sebuah suatu oleh sebagai tersebut tidak akan juga dapat bagi serta per jika maka""".split())
# (?![a-z]): huruf awal kata berikutnya bukan sub-indikator ("IKU 1 apa itu" bukan 1a)
IKU_IN_QUESTION_RE = re.compile(r"\bIKU\s*(\d{1,2})(?:\s*\(?\s*([a-d])(?![a-z])\s*\)?)?(?!\d)", re.I)
# maksud pertanyaan -> bagian tabel definisi yang didahulukan di antara chunk IKU yang disebut
BAGIAN_INTENT = [
    (re.compile(r"\b(apa itu|apa yang dimaksud|pengertian|definisi|maksud dari)\b", re.I), ("Definisi",)),
    (re.compile(r"\b(rumus|formula|cara (menghitung|hitung)|dihitung)\b", re.I), ("Formula",)),
]


def intended_bagian(question: str) -> tuple[str, ...]:
    for pattern, bagian in BAGIAN_INTENT:
        if pattern.search(question):
            return bagian
    return ()


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+(?:[.,][0-9]+)*", text.lower()) if t not in STOPWORDS]


class BM25:
    """BM25 Okapi sederhana untuk korpus kecil (ratusan chunk)."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in docs]
        self.len = [len(d) for d in docs]
        self.avgdl = sum(self.len) / max(len(docs), 1)
        df = Counter(t for d in docs for t in set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def top(self, query: list[str], n: int) -> list[int]:
        scores = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for t in query:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avgdl))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [i for i in order[:n] if scores[i] > 0]


def mentioned_iku(question: str) -> list[dict]:
    """'Berapa capaian IKU 11d?' -> [{'iku_id': '11d', 'jenis': 'iku'}]"""
    targets = []
    for num, sub in IKU_IN_QUESTION_RE.findall(question):
        ident = f"{int(num)}{sub.lower()}" if sub else str(int(num))
        if re.search(r"LLDIKTI", question, re.I):
            targets.append({"iku_id": f"LLDIKTI-{ident}", "jenis": "iku_lldikti"})
        elif re.search(r"sub[\s-]?indikator", question, re.I):
            targets.append({"iku_id": ident, "jenis": "sub_indikator"})
        else:
            targets.append({"iku_id": ident, "jenis": "iku"})
    return targets


def tier(meta: dict) -> int:
    """0 = Bab utama Buku, 1 = Lampiran Buku, 2 = PPT."""
    if meta.get("source_file", "").startswith(PRIMARY_SOURCE_PREFIX):
        return 0 if meta.get("doc_part", "utama") == "utama" else 1
    return 2


def dedupe_key(meta: dict):
    if meta.get("iku_id") and meta.get("bagian"):
        return (meta["iku_id"], meta.get("jenis"), meta["bagian"])
    return None


def where_and(**conds) -> dict:
    items = [{k: {"$eq": v}} for k, v in conds.items()]
    return items[0] if len(items) == 1 else {"$and": items}


class Retriever:
    def __init__(self, top_k=5, collection_name=COLLECTION_NAME, candidates=None, hybrid=False,
                 iku_boost=False, dedupe=False, rerank=False, min_chars=80, sambung_tabel=False):
        self.top_k = top_k
        self.candidates = candidates or top_k
        self.hybrid, self.iku_boost, self.dedupe, self.rerank = hybrid, iku_boost, dedupe, rerank
        self.min_chars = min_chars

        self.model = SentenceTransformer(
            MODEL_NAME,
            device="cuda" if torch.cuda.is_available() else "cpu"
        )

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_collection(
            name=collection_name
        )

        self.bm25 = None
        self.lanjutan_tabel: dict[str, str] = {}   # id potongan lanjutan -> id potongan sebelumnya
        self.potongan_awal: dict[str, tuple[str, dict]] = {}
        if hybrid or sambung_tabel:
            corpus = self.collection.get(include=["documents", "metadatas"])
            self.corpus_ids = corpus["ids"]
            if hybrid:
                self.bm25 = BM25([tokenize(d) for d in corpus["documents"]])
            if sambung_tabel:
                self.lanjutan_tabel = cari_lanjutan_tabel(corpus["ids"], corpus["documents"], corpus["metadatas"])
                awal = set(self.lanjutan_tabel.values())
                self.potongan_awal = {i: (d, m) for i, d, m in
                                      zip(corpus["ids"], corpus["documents"], corpus["metadatas"]) if i in awal}

        self.reranker = None
        if rerank:
            from sentence_transformers import CrossEncoder
            self.reranker = CrossEncoder(RERANKER_NAME, device=self.model.device, max_length=1024)

    @classmethod
    def v2(cls, top_k=5, collection_name=COLLECTION_NAME_V2, rerank=False):
        """Konfigurasi best practice (docs/02-desain/skema_embedding.md)."""
        return cls(top_k=top_k, collection_name=collection_name, candidates=30, hybrid=True,
                   iku_boost=True, dedupe=True, rerank=rerank, min_chars=0, sambung_tabel=True)

    # -- bantuan --------------------------------------------------------------

    def _fetch(self, ids: list[str], query_emb: np.ndarray) -> dict[str, dict]:
        """Ambil dokumen + metadata + jarak cosine ke query untuk id tertentu."""
        if not ids:
            return {}
        got = self.collection.get(ids=ids, include=["documents", "metadatas", "embeddings"])
        out = {}
        for i, doc, meta, emb in zip(got["ids"], got["documents"], got["metadatas"], got["embeddings"]):
            dist = float(1 - np.dot(query_emb, np.asarray(emb)))
            out[i] = {"id": i, "document": doc, "metadata": meta, "distance": dist}
        return out

    def _query_ids(self, query_emb: np.ndarray, n: int, where: dict | None = None) -> list[str]:
        kwargs = {"query_embeddings": [query_emb.tolist()], "n_results": n}
        if where:
            kwargs["where"] = where
        try:
            return self.collection.query(**kwargs)["ids"][0]
        except Exception:            # filter tidak cocok dengan dokumen mana pun
            return []

    # -- pencarian ------------------------------------------------------------

    def search(self, question, boleh=None, iku_cakupan=None):
        """
        boleh       : fungsi metadata -> bool; chunk yang tidak lolos dibuang (filter cakupan halaman).
        iku_cakupan : iku_id halaman IKU aktif; chunk IKU ini dipastikan masuk kandidat & didahulukan.
        """
        query_emb = np.asarray(self.model.encode([question], normalize_embeddings=True)[0])
        # dengan filter, sebagian kandidat akan dibuang -> ambil kandidat lebih banyak
        n_kandidat = self.candidates if boleh is None else self.candidates * 4

        # 1) dense: jarak diambil langsung dari Chroma (sesuai metrik koleksi: L2 lama / cosine v2)
        dense = self.collection.query(query_embeddings=[query_emb.tolist()], n_results=n_kandidat,
                                      include=["documents", "metadatas", "distances"])
        pool = {i: {"id": i, "document": d, "metadata": m, "distance": dist}
                for i, d, m, dist in zip(dense["ids"][0], dense["documents"][0],
                                         dense["metadatas"][0], dense["distances"][0])}

        # 2-3) daftar peringkat tambahan, lalu digabung dengan RRF
        rankings = [dense["ids"][0]]
        if self.bm25:
            rankings.append([self.corpus_ids[i] for i in self.bm25.top(tokenize(question), n_kandidat)])
        targets = mentioned_iku(question) if self.iku_boost else []
        if iku_cakupan:
            # di halaman IKU hanya IKU itu yang relevan; tanpa penyebutan, IKU halaman jadi target
            targets = [t for t in targets if t["iku_id"] == iku_cakupan] or [{"iku_id": iku_cakupan, "jenis": "iku"}]
            rankings.append(self._query_ids(query_emb, self.candidates, where_and(iku_id=iku_cakupan)))
        for t in targets:
            rankings.append(self._query_ids(query_emb, 10, where_and(iku_id=t["iku_id"], jenis=t["jenis"])))

        fused: dict[str, float] = {}
        for ranking in rankings:
            for rank, cid in enumerate(ranking, start=1):
                fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + rank)
        order = sorted(fused, key=lambda c: -fused[c]) if len(rankings) > 1 else rankings[0]
        pool.update(self._fetch([c for c in order if c not in pool], query_emb))
        items = [pool[c] for c in order if c in pool]

        # 4) dedupe: dahulukan Bab V Buku, salinan Lampiran/PPT dicatat di also_in
        if self.dedupe:
            items = self._dedupe(items, query_emb)

        # 5) rerank (opsional)
        if self.reranker:
            head = items[:RERANK_DEPTH]
            scores = self.reranker.predict([(question, it["document"]) for it in head])
            for it, s in zip(head, scores):
                it["rerank_score"] = float(s)
            items = sorted(head, key=lambda it: -it["rerank_score"]) + items[RERANK_DEPTH:]

        # 3b) IKU yang disebut di pertanyaan didahulukan (urutan relatif tetap)
        if targets:
            wanted = {(t["iku_id"], t["jenis"]) for t in targets}
            hit = lambda it: (it["metadata"].get("iku_id"), it["metadata"].get("jenis")) in wanted
            matched = [it for it in items if hit(it)]
            # di antara chunk IKU tsb, bagian yang sesuai maksud pertanyaan didahulukan
            # ("apa itu IKU 1" -> Definisi; "rumus IKU 3" -> Formula)
            bagian = intended_bagian(question)
            if bagian:
                matched = ([it for it in matched if it["metadata"].get("bagian") in bagian]
                           + [it for it in matched if it["metadata"].get("bagian") not in bagian])
            items = matched + [it for it in items if not hit(it)]

        output = []
        for it in items:
            if self.min_chars and len(it["document"].strip()) < self.min_chars:
                continue
            if boleh is not None and not boleh(it["metadata"]):
                continue
            output.append(it)
            if len(output) == self.top_k:
                break

        # 7) sambung potongan lanjutan tabel dengan potongan sebelumnya
        if self.lanjutan_tabel:
            output = self._sambung_tabel(output)
        return [self._format(it) for it in output]

    def _sambung_tabel(self, items: list[dict]) -> list[dict]:
        disambung = set()
        hasil = []
        for it in items:
            awal = self.lanjutan_tabel.get(it["id"])
            if awal:
                dok_awal, meta_awal = self.potongan_awal[awal]
                it = {**it, "document": gabung_tabel(dok_awal, it["document"]),
                      "metadata": {**it["metadata"], "page_start": meta_awal.get("page_start")},
                      "disambung_dari": awal}
                disambung.add(awal)
            hasil.append(it)
        # potongan awal yang sudah tersambung tidak perlu muncul dua kali
        return [it for it in hasil if it["id"] not in disambung]

    def _dedupe(self, items: list[dict], query_emb: np.ndarray) -> list[dict]:
        best_tier: dict = {}
        kept: list[dict] = []
        kept_ids: set[str] = set()
        buku_words = [set(tokenize(it["document"])) for it in items if tier(it["metadata"]) == 0]

        for it in items:
            meta = it["metadata"]
            key = dedupe_key(meta)
            it.setdefault("also_in", [])

            if key is None:
                # chunk naratif PPT yang isinya hampir sama dengan chunk Buku di kandidat -> buang
                if tier(meta) == 2:
                    words = set(tokenize(it["document"]))
                    if any(len(words & b) / max(len(words | b), 1) >= 0.6 for b in buku_words):
                        continue
                if it["id"] not in kept_ids:
                    kept.append(it)
                    kept_ids.add(it["id"])
                continue

            if key in best_tier and tier(meta) > best_tier[key]:
                owner = next((k for k in kept if dedupe_key(k["metadata"]) == key), None)
                if owner is not None:
                    owner["also_in"].append(self._citation(meta))
                continue

            if tier(meta) > 0:
                # cari padanan di Bab utama Buku untuk IKU + jenis + bagian yang sama. Satu bagian
                # bisa terpecah ke beberapa chunk (mis. Kriteria IKU 2) -> ambil semua potongannya,
                # urut sesuai dokumen, agar isinya tidak terpotong setelah dedupe
                ids = self._query_ids(query_emb, 4, where_and(
                    iku_id=meta["iku_id"], jenis=meta.get("jenis"), bagian=meta["bagian"], doc_part="utama",
                    source_priority=1))
                new_ids = sorted((i for i in ids if i not in kept_ids))
                if new_ids:
                    fetched = self._fetch(new_ids, query_emb)
                    for n, cid in enumerate(new_ids):
                        upgraded = fetched[cid]
                        upgraded["also_in"] = [self._citation(meta)] if n == 0 else []
                        kept.append(upgraded)
                        kept_ids.add(cid)
                    best_tier[key] = 0
                    continue
                if ids:
                    continue

            if it["id"] not in kept_ids:
                kept.append(it)
                kept_ids.add(it["id"])
                best_tier[key] = min(best_tier.get(key, 9), tier(meta))
        return kept

    @staticmethod
    def _citation(meta: dict) -> str:
        src = "Buku" if meta.get("source_file", "").startswith(PRIMARY_SOURCE_PREFIX) else "PPT"
        part = " (Lampiran Kepmen 358/M/KEP/2025)" if meta.get("doc_part") == "lampiran" else ""
        a, b = meta.get("page_start", meta.get("page")), meta.get("page_end", meta.get("page"))
        return f"{src}{part} hlm. {a}" + (f"–{b}" if b != a else "")

    @staticmethod
    def _format(it: dict) -> dict:
        metadata = it["metadata"]
        return {
            "chunk_id": it["id"],
            "content": it["document"],
            "source_file": metadata["source_file"],
            "page": metadata.get("page", metadata.get("page_start")),
            "page_start": metadata.get("page_start", metadata.get("page")),
            "page_end": metadata.get("page_end", metadata.get("page")),
            "section_path": metadata["section_path"],
            "source_priority": metadata.get("source_priority"),
            "iku_id": metadata.get("iku_id"),
            "jenis": metadata.get("jenis"),
            "doc_part": metadata.get("doc_part"),
            "bagian": metadata.get("bagian"),
            "source_notes": json.loads(metadata["source_notes"]) if metadata.get("source_notes") else [],
            "also_in": it.get("also_in", []),
            "rerank_score": it.get("rerank_score"),
            "disambung_dari": it.get("disambung_dari"),
            "distance": it["distance"],
        }
