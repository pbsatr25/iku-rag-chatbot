# Changelog

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/), versi mengikuti [Semantic Versioning](https://semver.org/lang/id/).

## [Unreleased]

### Ditambahkan
- **Deteksi intent memakai konteks halaman** (`src/generation/intent.py`, menggantikan isi `detect_intent` di `app.py`):
  - "IKU001" tanpa spasi dikenali; kepemilikan ("PT kami", "IKU 1 saya"), peringkat ("terendah", "ranking"), dan analisis/rangkuman unit dasbor (fakultas/prodi) dibaca sebagai `data`.
  - Di halaman IKU, pertanyaan capaian/fakultas/prodi/analisis = data dasbor halaman itu; rumus & definisi tetap ke dokumen.
  - Akurasi dataset tim `tests/intent_cases.json`: 39/48 → 48/48; 11 kasus halaman baru (PAGE-*): 6/11 → 11/11.
  - `tests/test_intent.py` (pytest, berjalan di CI tanpa `openai`).

### Diperbaiki
- `KODE_IKU_RE` (`cakupan.py`) membaca huruf awal kata berikutnya sebagai sub-indikator ("IKU 9 dihitung" → 9d).
- **Cakupan per halaman dasbor** (`src/generation/cakupan.py`, PRD Asisten IKU RAG-01–RAG-03):
  - `scope` di `POST /v1/answer` divalidasi; nilai tidak dikenal → `400`. Tanpa `scope` perilaku lama tetap (CLI, evaluasi).
  - Gerbang aturan **sebelum LLM**: kode IKU lain, topik khas IKU lain, atau konsep lintas IKU → `outOfScope: { suggestedTab }` dengan penolakan singkat, tanpa memakai kuota LLM.
  - Retrieval difilter `iku_id` halaman (`Retriever.search(boleh=, iku_cakupan=)`); Overview memakai chunk umum + IKU tanpa halaman dasbor.
  - Cakupan aktif ditulis eksplisit di system prompt kedua jalur jawaban (`ask`, `ask_with_spreadsheet`).
  - 42 unit test tanpa GPU (`tests/test_cakupan.py`).

### Direncanakan
- Tahap 7: LLM + sitasi (konteks top-k + `source_notes`, kalkulator via *tool calling*)
- Manifest embedding (model, revisi, hash chunk) dan cek kesehatan vektor
- Evaluasi reranker `bge-reranker-v2-m3`

## [0.2.0] - 2026-10-03

Repo dipisahkan dari repo tim `RAG-Chatbot-IKU` (branch `AI-Rio`) dan distrukturkan ulang.

### Ditambahkan
- **Parsing v2**: penanda halaman `<!-- page: N -->`, header/footer disertakan, cadangan `.pages.json`, job LlamaParse dapat dilanjutkan (`_jobs.json`), opsi `--rebuild` dan `--force`.
- **Validasi processing**: cakupan angka 100%, integritas tabel, dan validasi silang angka Buku vs PPT (`validate_cross_source.py`). Cacat dokumen sumber dicatat di `data/metadata/known_source_issues.json` dan dibawa sebagai `source_notes`.
- **Chunking v2 berbasis struktur** (`chunk_structured.py`): satu chunk = satu bagian (Definisi/Kriteria/Ketentuan/Formula), maksimal 512 token bge-m3, header konteks ikut di-embed. Divalidasi dengan `validate_chunks.py` (0 angka hilang).
- **Embedding v2** ternormalisasi dan koleksi Chroma `pmpt_qa_v2` dengan jarak cosine.
- **Retriever v2**: 30 kandidat, hybrid BM25 + RRF, deteksi IKU dan maksud pertanyaan, dedupe Bab V > Lampiran > PPT, reranker opsional.
- **Kalkulator IKU** (`src/calculator/iku_formulas.py`): rumus Bab V sebagai fungsi deterministik dengan langkah dan sitasi.
- **Evaluasi**: `eval_retrieval.py` (Hit@k, MRR, halaman sitasi) dan `run_calc_tests.py` (18 soal hitungan).
- Dokumentasi: inventaris formula, panduan chunking, skema embedding.
- Unit test kalkulator (`tests/`), CI GitHub Actions, template issue/PR, CONTRIBUTING.

### Diubah
- Struktur folder: `data/input` → `data/raw`; `*_v2` → nama tanpa sufiks; `data/chroma` → `data/vectorstore` (tidak di-commit); hasil validasi/evaluasi → `reports/`; artefak v1 → `data/legacy/v1/`.
- Default script mengarah ke pipeline v2: `build_chroma.py` → `pmpt_qa_v2`; `eval_retrieval.py` → `--preset v2 --collection pmpt_qa_v2 --oos-threshold 0.45`.

### Hasil

| Metrik | v1 | v2 |
|---|---|---|
| Hit@1 | 15/29 | 22/29 |
| Hit@5 | 25/29 | 26/29 |
| MRR@5 | 0,649 | 0,822 |
| Halaman sitasi benar | 15/23 | 25/26 |
| Soal hitungan benar | – | 18/18 (sitasi 17/18) |

## [0.1.0] - 2026-09-30

### Ditambahkan
- Pipeline awal dari repo tim: parsing LlamaParse, processing, chunking JSON, embedding bge-m3, Chroma `pmpt_qa` (L2), retriever dense.
