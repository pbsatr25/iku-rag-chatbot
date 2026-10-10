"""
postproses.py
Merapikan teks jawaban LLM sebelum diperiksa dan ditampilkan.

Beberapa model (mis. openai/gpt-oss) punya kebiasaan bawaan yang merusak format kita:
- rujukan ditulis 【3】 atau 【2†L1-L3】, bukan [3], sehingga sitasi halaman tidak terbaca;
- spasi khusus (narrow no-break space U+202F, no-break space U+00A0) di antara angka dan
  satuan ("33 %", "SDG 1"), dan tanda hubung khusus (U+2011) yang menyulitkan pencarian teks.
Perapian di sini tidak mengubah isi jawaban, hanya bentuk tulisannya.

Modul ini juga mendeteksi jawaban yang menghitung sendiri tanpa kalkulator (kasus H07/H08/H16:
angkanya kebetulan benar, tetapi tidak terverifikasi), supaya answer.py bisa meminta LLM
mengulang dengan alat hitung_iku.
"""

import re

RUJUKAN_BAWAAN = re.compile(r"【\s*(\d+)\s*(?:†[^】]*)?】")
# "4 × 0,2 = 0,8", "30 ÷ 120 × 100% = 25%": operasi antar-angka yang diikuti hasil
ARITMETIKA = re.compile(r"\d[\d.,]*\s*%?\s*[×x*÷/]\s*\d[^=\n]*=\s*\d")
LATEX = re.compile(r"\\(?:frac|times|div|cdot|sum)\b|\\\[|\\\(")
PREDIKAT = re.compile(r"\bpredikat", re.I)
SPASI_KHUSUS = str.maketrans({" ": " ", " ": " ", " ": " ", "‑": "-"})


def rapikan_jawaban(teks: str) -> str:
    """'… tepat waktu【3†L1-L4】, 33 %' -> '… tepat waktu[3], 33 %'."""
    return RUJUKAN_BAWAAN.sub(r"[\1]", teks.translate(SPASI_KHUSUS))


def varian_angka(nilai) -> list[str]:
    """Bentuk tulisan yang wajar untuk sebuah angka: 21.5 -> ['21.5', '21,5', '21,50', ...]."""
    if isinstance(nilai, bool) or not isinstance(nilai, (int, float)):
        return [str(nilai)]
    dua_desimal = f"{nilai:.2f}"
    ringkas = dua_desimal.rstrip("0").rstrip(".")
    varian = {ringkas, ringkas.replace(".", ","), dua_desimal, dua_desimal.replace(".", ",")}
    if float(nilai).is_integer():
        bulat = int(nilai)
        varian |= {f"{bulat:,}".replace(",", "."), f"{bulat:,}", str(bulat)}
    # nominal rupiah besar sering ditulis "14 juta" / "1,25 miliar"
    for besar, satuan in ((10 ** 9, "miliar"), (10 ** 6, "juta")):
        if abs(nilai) >= besar:
            angka = f"{nilai / besar:.3f}".rstrip("0").rstrip(".")
            varian |= {f"{angka} {satuan}", f"{angka.replace('.', ',')} {satuan}"}
            break
    return sorted(varian)


def angka_muncul(nilai, jawaban: str) -> bool:
    """True bila angka itu tertulis UTUH di jawaban. Tidak cukup memeriksa 'x in jawaban': kasus H28,
    hasil kalkulator 14.000 dianggap muncul karena '14,000' ada di dalam '14,000,000' (jawaban
    yang salah). Angka tidak boleh bersambung dengan angka lain di depan atau belakangnya."""
    for v in varian_angka(nilai):
        pola = r"(?<!\d)(?<!\d[.,])" + re.escape(v) + r"(?!\d)(?![.,]\d)"
        if re.search(pola, jawaban, re.I):
            return True
    return False


def tampak_menghitung_sendiri(pertanyaan: str, jawaban: str) -> bool:
    """True bila jawaban (yang dibuat TANPA hasil kalkulator) memuat perhitungan angka,
    rumus LaTeX, atau penentuan predikat dari nilai yang diberikan pengguna."""
    if ARITMETIKA.search(jawaban) or LATEX.search(jawaban):
        return True
    return bool(re.search(r"\d", pertanyaan) and PREDIKAT.search(pertanyaan) and PREDIKAT.search(jawaban))
