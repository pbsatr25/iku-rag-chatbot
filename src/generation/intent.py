"""
intent.py
Menentukan jalur jawaban sebuah pertanyaan, tanpa LLM:

- "data"     : butuh data dasbor/spreadsheet milik pengguna. app.py mengembalikan
               action fetch_data, lalu Next.js mengirim ulang pertanyaan + data.
- "formula"  : rumus / cara menghitung, dijawab dari Buku IKU (+ kalkulator).
- "definisi" : definisi, kriteria, ketentuan, atau pertanyaan lain dari Buku IKU.

Aturan dievaluasi berurutan (yang pertama cocok menang):
1. Sinyal data kuat: kepemilikan ("IKU 1 saya", "PT kami"), peringkat ("terendah",
   "ranking"), "data IKU 1"/"data 2025", atau tahun + IKU/capaian.
2. Kata rumus/cara hitung -> formula.
3. Kata definisi/kriteria -> definisi.
4. Di halaman IKU, pertanyaan tentang capaian/realisasi, unit dasbor (fakultas/prodi), atau
   analisis/rangkuman = data dasbor halaman itu. Konteks halaman dipakai karena pengguna sedang
   melihat datanya ("rangkum analisis fakultas"). Kata umum seperti "berapa" atau "mahasiswa"
   sengaja tidak dipakai: "Berapa SKS minimal agar diakui?" tetap pertanyaan dokumen.
5. Tanpa halaman IKU: unit dasbor + kata tanya angka/analisis -> data;
   "berapa capaian IKU N" tanpa data pengguna -> formula (jelaskan cara menghitungnya).
6. Selain itu -> definisi.

Di Overview, aturan 4 sengaja tidak dipakai: data Overview lintas IKU, sedangkan jalur
fetch_data saat ini mengambil satu IKU. Modul ini murni agar bisa diuji di CI.
"""

import re

from cakupan import KODE_IKU_RE, Cakupan

DATA, FORMULA, DEFINISI = "data", "formula", "definisi"

_PEMILIK = (r"kampus|pt|perguruan tinggi|universitas|institusi|prodi|program studi|fakultas|jurusan"
            r"|data|nilai|capaian|iku(?: \d+)?")
# "IKU 1 saya", "PT kami", "capaian kita"; bukan "saya ingin tahu rumus ..."
KEPEMILIKAN_RE = re.compile(rf"\b(?:{_PEMILIK})\s+(?:saya|kami|kita)\b|\bdata kampus\b")
PERINGKAT_RE = re.compile(r"\b(tertinggi|terendah|paling (tinggi|rendah|banyak|sedikit|baik|buruk)"
                          r"|ranking|peringkat|top \d+|bottom \d+)\b")
TAHUN_RE = re.compile(r"\b20[2-3]\d\b|\btahun lalu\b")
DATA_RE = re.compile(r"\bdata\b")
CAPAIAN_RE = re.compile(r"\b(capaian|capaiannya|realisasi|nilai|skor|persentase)\b")

FORMULA_RE = re.compile(r"\b(rumus|rumusnya|formula|bobot|(cara|langkah) (meng)?hitung(nya)?"
                        r"|menghitung|dihitung|gimana hitung|bagaimana hitung)\b")
DEFINISI_RE = re.compile(r"\b(apa itu|apa yang dimaksud|pengertian|definisi|arti|maksud|jelaskan"
                         r"|kriteria|ketentuan|itu apa)\b")

UNIT_DASBOR_RE = re.compile(r"\b(fakultas|prodi|program studi|jurusan)\b")
CAPAIAN_HALAMAN_RE = re.compile(r"\b(capaian|capaiannya|realisasi|skor)\b")
TANYA_ANGKA_RE = re.compile(r"\b(berapa|brp|jumlah|total|tampilkan|lihat|tunjukkan|cek|periksa"
                            r"|capaian|capaiannya|realisasi|nilai|skor|persentase|rata-rata)\b")
ANALISIS_RE = re.compile(r"\b(analisis|analisa|rangkum\w*|ringkas\w*|rekap\w*|tren|perbandingan|bandingkan"
                         r"|evaluasi|kesimpulan|insight)\b")


def normalisasi(pertanyaan: str) -> str:
    """Huruf kecil, spasi rapat, dan kode IKU seragam: 'IKU001' / 'iku-009' -> 'iku 1' / 'iku 9'."""
    teks = KODE_IKU_RE.sub(lambda m: f"iku {int(m.group(1))}", pertanyaan.lower())
    return re.sub(r"\s+", " ", teks).strip()


def deteksi_intent(pertanyaan: str, cakupan: Cakupan | None = None) -> str:
    q = normalisasi(pertanyaan)
    sebut_iku = re.search(r"\biku \d+\b", q) is not None

    # 1) sinyal data kuat
    if (KEPEMILIKAN_RE.search(q) or PERINGKAT_RE.search(q)
            or (DATA_RE.search(q) and (sebut_iku or TAHUN_RE.search(q)))
            or (TAHUN_RE.search(q) and (sebut_iku or CAPAIAN_RE.search(q)))):
        return DATA

    # 2-3) pertanyaan dokumen
    if FORMULA_RE.search(q):
        return FORMULA
    if DEFINISI_RE.search(q):
        return DEFINISI

    # 4) halaman IKU: pertanyaan angka/analisis merujuk data dasbor yang sedang dilihat
    if cakupan is not None and cakupan.jenis == "iku":
        if UNIT_DASBOR_RE.search(q) or CAPAIAN_HALAMAN_RE.search(q) or ANALISIS_RE.search(q):
            return DATA
        return DEFINISI

    # 5) tanpa halaman IKU
    if UNIT_DASBOR_RE.search(q) and (TANYA_ANGKA_RE.search(q) or ANALISIS_RE.search(q)):
        return DATA
    if sebut_iku and CAPAIAN_RE.search(q):
        return FORMULA
    return DEFINISI
