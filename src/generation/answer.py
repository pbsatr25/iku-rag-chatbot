"""
answer.py
Inti chatbot: retrieval RAG + spreadsheet tool -> LLM (+ alat hitung_iku) -> jawaban.

Alur satu pertanyaan:
1. Retriever mengambil 5 chunk terbaik (selalu dipanggil untuk konteks IKU).
2. Intent detection: apakah butuh data spreadsheet?
   - Ya -> panggil spreadsheet tool, format konteks spreadsheet untuk LLM
   - Tidak -> skip spreadsheet tool
3. LLM menerima instruksi + konteks (chunk + spreadsheet) + pertanyaan.
4. Selama LLM meminta alat hitung_iku, kode jalankan kalkulator dan kirim hasilnya.
5. Jawaban akhir dirapikan (postproses.py) lalu diperiksa.
"""

import json
import re
import sys
from pathlib import Path
import openai
from spreadsheet_calc import precalculate_spreadsheet

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "retrieval"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "generation"))

from retriever import Retriever  # noqa: E402
from llm_client import get_client  # noqa: E402
from postproses import angka_muncul, rapikan_jawaban, tampak_menghitung_sendiri, varian_angka  # noqa: E402,F401
from prompt import SYSTEM_PROMPT, build_user_message  # noqa: E402
from cakupan import Cakupan, chunk_boleh, instruksi_cakupan  # noqa: E402
from tools import NAMA_ALAT, TOOL_HITUNG_IKU, jalankan_alat  # noqa: E402
from tools import NAMA_ALAT_SPREADSHEET, TOOL_QUERY_SPREADSHEET, jalankan_spreadsheet_tool  # noqa: E402,F401

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


def intent_butuh_spreadsheet(question: str) -> bool:
    """Deteksi apakah pertanyaan butuh data spreadsheet (data kampus user)."""
    question_lower = question.lower()
    keywords = ["kampus saya", "data saya", "nilai iku", "capaian iku", "berapa iku"]
    tahun_pattern = re.compile(r"\b(202[0-9]|203[0-9])\b")
    
    has_keyword = any(kw in question_lower for kw in keywords)
    has_tahun = bool(tahun_pattern.search(question))
    
    return has_keyword and has_tahun


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

    def _cari(self, question: str, cakupan: Cakupan | None) -> list[dict]:
        """Retrieval yang dibatasi cakupan halaman (tanpa cakupan = seluruh dokumen)."""
        if cakupan is None:
            return self.retriever.search(question)
        return self.retriever.search(question, boleh=lambda meta: chunk_boleh(meta, cakupan),
                                     iku_cakupan=cakupan.iku_id)

    @staticmethod
    def _system_prompt(dasar: str, cakupan: Cakupan | None) -> str:
        tambahan = instruksi_cakupan(cakupan)
        return f"{dasar}\n\n{tambahan}" if tambahan else dasar

    def ask(self, question: str, cakupan: Cakupan | None = None) -> dict:
        """
        Jawab pertanyaan menggunakan RAG + kalkulator IKU.

        CATATAN: Metode ini HANYA dipanggil untuk intent "definisi" atau "formula"
        (tidak butuh data spreadsheet). Untuk intent "data", app.py mengembalikan
        action fetch_data ke Next.js yang akan memanggil ask_with_spreadsheet().
        jalankan_spreadsheet_tool() dengan email dummy sudah dinonaktifkan.

        `cakupan` = halaman dasbor aktif; None untuk CLI dan evaluasi (tanpa batas cakupan).
        """
        chunks = self._cari(question, cakupan)

        konteks = build_user_message(question, chunks)
        messages = [
            {"role": "system", "content": self._system_prompt(SYSTEM_PROMPT, cakupan)},
            {"role": "user", "content": konteks},
        ]
        hasil_alat, masalah_alat = [], []

        tools_available = [TOOL_HITUNG_IKU]
        message = self._putaran_alat(messages, hasil_alat, masalah_alat, tools_available)
        berhasil = any("error" not in h["hasil"] for h in hasil_alat)
        if message and not berhasil and tampak_menghitung_sendiri(question, message.content or ""):
            masalah_alat.append("LLM menghitung sendiri tanpa kalkulator; diminta mengulang dengan alat.")
            messages += [{"role": "assistant", "content": message.content or ""},
                         {"role": "user", "content": PESAN_HITUNG_SENDIRI}]
            message = self._putaran_alat(messages, hasil_alat, masalah_alat, tools_available)

        jawaban = rapikan_jawaban(message.content or "").strip() if message else \
            "Maaf, perhitungan tidak selesai dalam batas percobaan. Coba ulangi dengan data yang lebih lengkap."
        if not jawaban:
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
            "spreadsheet": None,
            "butuh_spreadsheet": False,
        }


    def ask_with_spreadsheet(self, question: str, spreadsheet_context: str,
                             cakupan: Cakupan | None = None) -> dict:
        """
        Jawab pertanyaan menggunakan RAG + spreadsheet_context yang sudah dihitung
        secara deterministik oleh spreadsheet_calc.py (1x panggilan LLM, bebas Error 400/413).
        """
        # 1. Ambil 3 chunk dokumen terbaik untuk sitasi
        chunks = self._cari(question, cakupan)[:3]

        # 2. Pre-calculate semua baris & rekap menggunakan kalkulator resmi Python
        enriched_context, hasil_alat = precalculate_spreadsheet(spreadsheet_context)

        instruksi_data = (
            f"{enriched_context}\n\n"
            "INSTRUKSI PENJAWABAN DATA KAMPUS (PENTING):\n"
            "- Seluruh angka Rekap, Pembilang, Penyebut, dan Tabel di atas SUDAH dihitung secara resmi oleh kalkulator server.\n"
            "- JANGAN memanggil fungsi/alat/tool apa pun (termasuk hitung_iku, python, atau container.exec). Cukup baca dan tulis ulang rincian angka yang sudah tersedia di atas dalam bentuk teks biasa.\n"
            "- Gunakan langsung angka dari bagian Rekap atau Tabel sesuai pertanyaan user.\n"
            "- Sertakan sitasi [1], [2], [3] dari potongan dokumen ketika menjelaskan definisi, kriteria, atau rumus IKU."
        )

        konteks = build_user_message(question, chunks) + "\n\n" + instruksi_data

        # Override instruksi tool di SYSTEM_PROMPT agar model tidak mencoba memanggil tool saat tool_choice=none
        system_prompt_no_tool = (
            SYSTEM_PROMPT
            + "\n\nCATATAN MODE SPREADSHEET: Pada panggilan ini semua perhitungan telah selesai dijalankan di server. "
            "DILARANG memanggil tool/function call apa pun. Jawab langsung dengan teks."
        )

        messages = [
            {"role": "system", "content": self._system_prompt(system_prompt_no_tool, cakupan)},
            {"role": "user", "content": konteks},
        ]

        masalah_alat = []
        message = None

        # 3. Panggil LLM 1 kali (dengan penyelamatan otomatis jika Groq terkena tool_use_failed)
        for percobaan_ke in range(MAX_ULANG_ALAT_DITOLAK + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.0,
                )
                message = response.choices[0].message
                break
            except openai.BadRequestError as e:
                if not alat_ditolak_server(e):
                    raise
                masalah_alat.append(f"Groq menolak tool call pada mode non-tool (percobaan {percobaan_ke + 1}); diulang.")
                if percobaan_ke < MAX_ULANG_ALAT_DITOLAK - 1:
                    messages.append({
                        "role": "system",
                        "content": "PERINGATAN SISTEM: Jangan memanggil tool atau mengeksekusi kode apa pun! Tuliskan jawaban langsung dalam teks bahasa Indonesia berdasarkan data yang sudah dihitung di atas."
                    })
                else:
                    # Fallback terakhir: jika model tetap memaksa panggil tool, berikan TOOL_HITUNG_IKU agar tidak crash 400
                    message = self._putaran_alat(messages, hasil_alat, masalah_alat, [TOOL_HITUNG_IKU])
                    break

        jawaban = rapikan_jawaban(message.content or "").strip() if message else \
            "Maaf, tidak dapat memproses data spreadsheet. Coba ulangi pertanyaan."
        if not jawaban:
            jawaban = PESAN_JAWABAN_KOSONG

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
            "spreadsheet": {"from_nextjs": True, "context_length": len(spreadsheet_context)},
            "butuh_spreadsheet": True,
        }

    def _putaran_alat(self, messages: list[dict], hasil_alat: list[dict], masalah_alat: list[str], tools: list[dict]):
        """Tanya LLM; selama ia meminta alat, jalankan kalkulator/spreadsheet dan kirim hasilnya kembali."""
        for _ in range(MAX_PUTARAN_ALAT):
            response = self._minta_llm(messages, masalah_alat, tools)
            message = response.choices[0].message
            if not message.tool_calls:
                return message
            messages.append(message.model_dump(exclude_none=True))
            for call in message.tool_calls:
                if call.function.name == NAMA_ALAT_SPREADSHEET:
                    hasil = jalankan_spreadsheet_tool(call.function.arguments or "{}")
                    hasil_alat.append({"argumen": call.function.arguments, "hasil": hasil})
                    messages.append({"role": "tool", "tool_call_id": call.id,
                                     "content": json.dumps(hasil, ensure_ascii=False)})
                else:
                    if call.function.name != NAMA_ALAT:
                        masalah_alat.append(f"LLM memakai nama alat tidak baku '{call.function.name}' (tetap diproses).")
                    hasil = jalankan_alat(call.function.name, call.function.arguments)
                    hasil_alat.append({"argumen": call.function.arguments, "hasil": hasil})
                    messages.append({"role": "tool", "tool_call_id": call.id,
                                     "content": json.dumps(hasil, ensure_ascii=False)})
        return None

    def _minta_llm(self, messages: list[dict], masalah_alat: list[str], tools: list[dict]):
        """Panggil LLM, dengan penyelamatan otomatis jika Groq menolak nama alat (mis. 'hitungan_iku')
        atau percobaan ulang bila format JSON rusak / respons kosong."""
        percobaan = messages
        ditolak = kosong = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model, messages=percobaan, tools=tools, tool_choice="auto",
                )
            except openai.BadRequestError as e:
                if not alat_ditolak_server(e) or ditolak == MAX_ULANG_ALAT_DITOLAK:
                    raise
                ditolak += 1
                alasan = ringkas_alasan(e)
                masalah_alat.append(f"Panggilan alat ditolak server ({alasan}); diulang otomatis.")
                # Gunakan role system atau gabungkan ke pesan terakhir agar tidak ada 2 role 'user' berurutan
                percobaan = messages + [{"role": "system", "content": PESAN_ALAT_DITOLAK.format(alasan=alasan)}]
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
    if hasil.get("spreadsheet"):
        baris += [f"Data spreadsheet: {len(hasil['spreadsheet'].get('rows', []))} baris"]
    if hasil["peringatan"]:
        baris += ["", "PERINGATAN:"] + [f"  - {p}" for p in hasil["peringatan"]]
    return "\n".join(baris)
