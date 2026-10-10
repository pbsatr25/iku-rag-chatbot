"""
answer.py
Inti chatbot: retriever v2 -> LLM (+ alat hitung_iku) -> jawaban dengan sitasi halaman.

Alur satu pertanyaan:
1. Retriever mengambil 5 chunk terbaik.
2. LLM menerima instruksi + konteks bernomor + pertanyaan, dan boleh memanggil hitung_iku.
3. Selama LLM meminta alat, kode menjalankan kalkulator dan mengirim hasilnya kembali.
   Bila LLM ternyata menghitung sendiri tanpa kalkulator, ia diminta mengulang sekali.
4. Jawaban akhir dirapikan (postproses.py) lalu diperiksa: rujukan [n] diubah menjadi
   sitasi halaman dari metadata, dan angka hasil kalkulator harus muncul di jawaban.
"""

import json
import re
import sys
from pathlib import Path
import openai

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "retrieval"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "generation"))

from retriever import Retriever  # noqa: E402
from llm_client import get_client  # noqa: E402
from postproses import angka_muncul, rapikan_jawaban, tampak_menghitung_sendiri, varian_angka  # noqa: E402,F401
from prompt import SYSTEM_PROMPT, build_user_message  # noqa: E402
from tools import NAMA_ALAT, TOOL_HITUNG_IKU, jalankan_alat  # noqa: E402

MAX_PUTARAN_ALAT = 4
MAX_ULANG_ALAT_DITOLAK = 2
MAX_ULANG_KOSONG = 2
PESAN_JAWABAN_KOSONG = ("Maaf, chatbot belum berhasil menyusun jawaban untuk pertanyaan ini. "
                        "Silakan ulangi pertanyaan beberapa saat lagi.")
PESAN_ALAT_DITOLAK = (
    "Catatan sistem: panggilan alat sebelumnya ditolak server karena formatnya salah ({alasan}). "
    f"Satu-satunya alat adalah '{NAMA_ALAT}' dengan parameter 'fungsi' dan 'argumen_json'. "
    "Ulangi dengan nama alat dan format yang benar."
)
PESAN_HITUNG_SENDIRI = (
    f"Catatan sistem: jawabanmu memuat perhitungan atau penentuan predikat yang tidak berasal dari alat "
    f"'{NAMA_ALAT}'. Panggil alat itu untuk perhitungan tersebut, lalu tulis ulang jawaban lengkap "
    "berdasarkan hasil alat, tanpa LaTeX. Jika datanya belum lengkap atau pertanyaannya di luar cakupan, "
    "tulis ulang jawaban tanpa angka hasil hitunganmu sendiri."
)


def alat_ditolak_server(e: openai.BadRequestError) -> bool:
    """Penyedia seperti Groq memvalidasi panggilan alat di server dan menolak (400) bila nama
    alat atau JSON argumennya rusak. Kesalahan ini acak, jadi aman diulang."""
    teks = str(e)
    return (getattr(e, "code", None) == "tool_use_failed"
            or "tool_use_failed" in teks
            or "Tool call validation failed" in teks)


def ringkas_alasan(e: Exception) -> str:
    m = re.search(r"attempted to call tool '([^']*)'", str(e))
    return f"nama alat '{m.group(1)}' tidak dikenal" if m else str(e)[:120]


def format_sitasi(chunk: dict) -> str:
    sumber = "Buku IKU Diktisaintek Berdampak V1" if chunk["source_file"].startswith("Buku") \
        else "PPT IKU Diktisaintek Berdampak PTS V2"
    if chunk.get("doc_part") == "lampiran":
        sumber += " (Lampiran Kepmen 358/M/KEP/2025)"
    a, b = chunk["page_start"], chunk["page_end"]
    teks = f"{sumber}, hlm. {a}" + (f"–{b}" if b != a else "")
    detail = [x for x in (f"IKU {chunk['iku_id']}" if chunk.get("iku_id") else None, chunk.get("bagian")) if x]
    if detail:
        teks += f" ({', '.join(detail)})"
    if chunk.get("also_in"):
        teks += f"; juga di {'; '.join(chunk['also_in'])}"
    return teks


def periksa_jawaban(pertanyaan: str, jawaban: str, chunks: list[dict],
                    hasil_alat: list[dict]) -> tuple[list[str], list[str]]:
    """Ubah rujukan [n] menjadi daftar sitasi dan kumpulkan peringatan."""
    peringatan = []
    dipakai = sorted({int(n) for n in re.findall(r"\[(\d+)\]", jawaban)})
    sitasi = [f"[{n}] {format_sitasi(chunks[n - 1])}" for n in dipakai if 1 <= n <= len(chunks)]

    salah = [n for n in dipakai if not 1 <= n <= len(chunks)]
    if salah:
        peringatan.append(f"Rujukan tidak valid (tidak ada di konteks): {salah}")

    berhasil = [h for h in hasil_alat if "error" not in h["hasil"]]
    for h in berhasil:
        nilai = h["hasil"]["hasil"]
        semua = list(nilai.values()) if isinstance(nilai, dict) else [nilai]
        for v in semua:
            if not angka_muncul(v, jawaban):
                peringatan.append(f"Hasil kalkulator {v} tidak muncul di jawaban; periksa apakah LLM mengubah angkanya.")

    soal_hitungan = re.search(r"\d", pertanyaan) and re.search(r"\b(berapa|hitung)", pertanyaan, re.I)
    if soal_hitungan and not hasil_alat and re.search(r"\d+(?:[.,]\d+)?\s*%", jawaban):
        peringatan.append("Soal hitungan dijawab dengan persentase tetapi kalkulator tidak dipanggil.")
    if not dipakai and not re.search(r"tidak (ditemukan|terdapat|ada)", jawaban, re.I):
        peringatan.append("Jawaban tidak memuat rujukan [n] ke konteks.")
    return sitasi, peringatan


class Chatbot:
    def __init__(self, top_k: int = 5):
        self.retriever = Retriever.v2(top_k=top_k)
        self.client, self.model = get_client()

    def ask(self, question: str) -> dict:
        chunks = self.retriever.search(question)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_message(question, chunks)},
        ]
        hasil_alat, masalah_alat = [], []

        message = self._putaran_alat(messages, hasil_alat, masalah_alat)
        berhasil = any("error" not in h["hasil"] for h in hasil_alat)
        if message and not berhasil and tampak_menghitung_sendiri(question, message.content or ""):
            # angka tanpa kalkulator tidak terverifikasi walaupun kebetulan benar: minta ulang sekali
            masalah_alat.append("LLM menghitung sendiri tanpa kalkulator; diminta mengulang dengan alat.")
            messages += [{"role": "assistant", "content": message.content or ""},
                         {"role": "user", "content": PESAN_HITUNG_SENDIRI}]
            message = self._putaran_alat(messages, hasil_alat, masalah_alat)

        jawaban = rapikan_jawaban(message.content or "").strip() if message else \
            "Maaf, perhitungan tidak selesai dalam batas percobaan. Coba ulangi dengan data yang lebih lengkap."
        if not jawaban:
            # jangan gagal diam-diam: user tetap mendapat pesan, dan kejadiannya tercatat
            jawaban = PESAN_JAWABAN_KOSONG
            masalah_alat.append(f"LLM tetap mengembalikan jawaban kosong setelah diulang {MAX_ULANG_KOSONG}x.")
        sitasi, peringatan = periksa_jawaban(question, jawaban, chunks, hasil_alat)
        peringatan = masalah_alat + peringatan
        sumber_rumus = sorted({h["hasil"]["sumber"] for h in hasil_alat if "sumber" in h["hasil"]})
        return {
            "pertanyaan": question,
            "jawaban": jawaban,
            "sitasi": sitasi,
            "sumber_rumus": sumber_rumus,
            "kalkulator": hasil_alat,
            "peringatan": peringatan,
            "chunks": chunks,
        }

    def _putaran_alat(self, messages: list[dict], hasil_alat: list[dict], masalah_alat: list[str]):
        """Tanya LLM; selama ia meminta alat, jalankan kalkulator dan kirim hasilnya kembali.
        Mengembalikan pesan jawaban akhir, atau None bila batas putaran habis."""
        for _ in range(MAX_PUTARAN_ALAT):
            response = self._minta_llm(messages, masalah_alat)
            message = response.choices[0].message
            if not message.tool_calls:
                return message
            # pesan asisten (berisi permintaan alat) dikirim balik APA ADANYA: Gemini menyisipkan
            # data tambahan ("thought signature") yang wajib dikembalikan tanpa diubah
            messages.append(message.model_dump(exclude_none=True))
            for call in message.tool_calls:
                if call.function.name != NAMA_ALAT:
                    masalah_alat.append(f"LLM memakai nama alat tidak baku '{call.function.name}' (tetap diproses).")
                hasil = jalankan_alat(call.function.name, call.function.arguments)
                hasil_alat.append({"argumen": call.function.arguments, "hasil": hasil})
                messages.append({"role": "tool", "tool_call_id": call.id,
                                "content": json.dumps(hasil, ensure_ascii=False)})
        return None

    def _minta_llm(self, messages: list[dict], masalah_alat: list[str]):
        """Panggil LLM, dengan dua percobaan ulang otomatis:
        - server menolak panggilan alat yang rusak (400): ulangi dengan catatan koreksi
          (catatan hanya dipakai untuk percobaan ulang, tidak masuk riwayat percakapan);
        - LLM mengembalikan respons kosong (tanpa teks dan tanpa panggilan alat): ulangi apa adanya."""
        percobaan = messages
        ditolak = kosong = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model, messages=percobaan, tools=[TOOL_HITUNG_IKU], tool_choice="auto",
                )
            except openai.BadRequestError as e:
                if not alat_ditolak_server(e) or ditolak == MAX_ULANG_ALAT_DITOLAK:
                    raise
                ditolak += 1
                alasan = ringkas_alasan(e)
                masalah_alat.append(f"Panggilan alat ditolak server ({alasan}); diulang otomatis.")
                percobaan = messages + [{"role": "user", "content": PESAN_ALAT_DITOLAK.format(alasan=alasan)}]
                continue
            message = response.choices[0].message
            if message.tool_calls or (message.content or "").strip() or kosong == MAX_ULANG_KOSONG:
                return response
            kosong += 1
            masalah_alat.append("LLM mengembalikan respons kosong; diulang otomatis.")


def tampilkan(hasil: dict) -> str:
    baris = [hasil["jawaban"], ""]
    if hasil["sitasi"]:
        baris += ["Sumber:"] + [f"  {s}" for s in hasil["sitasi"]]
    if hasil["sumber_rumus"]:
        baris += ["Sumber rumus (kalkulator):"] + [f"  {s}" for s in hasil["sumber_rumus"]]
    if hasil["peringatan"]:
        baris += ["", "PERINGATAN:"] + [f"  - {p}" for p in hasil["peringatan"]]
    return "\n".join(baris)
