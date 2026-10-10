"""
iku_formulas.py
Kalkulator IKU: rumus Buku IKU Diktisaintek Berdampak V1 sebagai fungsi Python
yang deterministik.

Prinsip: LLM tidak menghitung sendiri. LLM cukup memilih fungsi dan mengisi
argumennya dari pertanyaan user; fungsi di sini yang menghitung, lalu
mengembalikan hasil, langkah perhitungan, dan sumber halaman untuk sitasi.

Sumber kebenaran ada di spec/buku_iku_v1.json, bukan di file ini:
- konstanta (AEE ideal, bobot, daftar pos pendapatan, tabel predikat, ...)
- metadata tiap rumus (ikuCode, teks rumus, halaman sumber, catatan tafsir, status)
File JSON itu bisa dibaca bahasa apa pun, jadi tim BE/FE (TypeScript) memakai
angka yang sama. File ini hanya berisi LOGIKA hitung.

Setiap fungsi mengembalikan dict:
    id, ikuCode  : identitas rumus di spec
    hasil        : angka / teks akhir (angka mentah, belum diformat)
    satuan       : satuan hasil
    langkah      : langkah perhitungan yang bisa ditampilkan ke user
    formula_teks : teks rumus (untuk blok "formula" di UI)
    sumber       : sitasi rumus dalam satu kalimat ("..., hlm. 49–50")
    rujukan      : {dokumen, versi, bagian, halaman} (untuk blok sitasi di UI)
    status       : terverifikasi / ada_tafsir / perlu_konfirmasi_po
    catatan      : keputusan tafsir untuk bagian dokumen yang ambigu (bila ada)

Input yang tidak masuk akal (penyebut 0, nilai negatif, kunci tidak dikenal)
ditolak dengan ValueError berpesan jelas, tidak pernah diam-diam menjadi 0.
"""

import json
import math
import re
from pathlib import Path

SPEC_FILE = Path(__file__).resolve().parent / "spec" / "buku_iku_v1.json"
SPEC = json.loads(SPEC_FILE.read_text(encoding="utf-8"))
RUMUS = {r["id"]: r for r in SPEC["rumus"]}
_K = SPEC["konstanta"]

BUKU = f"{SPEC['dokumen']} {SPEC['versi']}"


def _pct(x: float) -> float:
    return round(x * 100, 2)


def _fmt(x: float) -> str:
    """Format angka gaya Indonesia: 1234.5 -> '1.234,5'."""
    s = f"{x:,.2f}".rstrip("0").rstrip(".")
    return s.replace(",", "#").replace(".", ",").replace("#", ".")


def _halaman(halaman: list[int]) -> str:
    return str(halaman[0]) if len(halaman) == 1 else f"{min(halaman)}–{max(halaman)}"


def _keluaran(id_rumus: str, hasil, satuan: str, langkah: list[str], pakai_catatan: bool = True) -> dict:
    """Bungkus hasil hitung dengan metadata rumus dari spec."""
    r = RUMUS[id_rumus]
    out = {
        "id": id_rumus,
        "ikuCode": r["ikuCode"],
        "hasil": hasil,
        "satuan": satuan,
        "langkah": langkah,
        "formula_teks": r["formula_teks"],
        "sumber": f"{BUKU}, {r['sumber']['bagian']}, hlm. {_halaman(r['sumber']['halaman'])}",
        "rujukan": {"dokumen": SPEC["dokumen"], "versi": SPEC["versi"], **r["sumber"]},
        "status": r["status"],
    }
    if pakai_catatan and r["catatan"]:
        out["catatan"] = r["catatan"]
    return out


# ---------------------------------------------------------------------------
# Validasi input
# ---------------------------------------------------------------------------

def _wajib_positif(nilai: float, nama: str) -> None:
    if nilai <= 0:
        raise ValueError(f"{nama} harus lebih dari 0 (diberikan: {nilai})")


def _tidak_negatif(nilai: float, nama: str) -> None:
    if nilai < 0:
        raise ValueError(f"{nama} tidak boleh negatif (diberikan: {nilai})")


def _pilih(kamus: dict, kunci, nama: str):
    if kunci not in kamus:
        raise ValueError(f"{nama} {kunci!r} tidak dikenal. Pilihan: {', '.join(map(str, kamus))}")
    return kamus[kunci]


def _tidak_melebihi(bagian: float, total: float, nama_bagian: str, nama_total: str) -> None:
    if bagian > total * (1 + 1e-9):
        raise ValueError(f"{nama_bagian} ({_fmt(bagian)}) melebihi {nama_total} ({_fmt(total)})")


# ---------------------------------------------------------------------------
# Konstanta (dibaca dari spec; nama tetap sama agar modul lain tidak berubah)
# ---------------------------------------------------------------------------

AEE_IDEAL = _K["aee_ideal"]
MASA_TEMPUH = _K["masa_tempuh_semester"]
BOBOT_IKU2 = _K["bobot_iku2"]
GALAT_SLOVIN = _K["galat_slovin"]
BOBOT_SKS = _K["bobot_sks"]
BOBOT_PRESTASI = {(tingkat, peringkat): bobot
                  for tingkat, daftar in _K["bobot_prestasi"].items()
                  for peringkat, bobot in daftar.items()}
BOBOT_PUBLIKASI = _K["bobot_publikasi"]
BONUS_KOLABORASI = _K["bonus_kolaborasi"]
PENDAPATAN_DIAKUI = set(_K["pendapatan_diakui"])
PENDAPATAN_TIDAK_DIAKUI = set(_K["pendapatan_tidak_diakui"])
PREDIKAT_SAKIP = sorted(((p["nilai_min"], p["predikat"]) for p in _K["predikat_sakip"]), reverse=True)
KELIPATAN_UMP = _K["kelipatan_ump"]
SATUAN_NOMINAL = _K["satuan_nominal"]
UMP_MINIMUM = _K["batas_wajar"]["ump_minimum_rupiah"]

# kode rasio -> (label pembilang, label penyebut, bagian sumber)
RASIO = {r["id"]: (r["input"]["pembilang"], r["input"]["penyebut"], r["sumber"]["bagian"])
         for r in SPEC["rumus"] if r["pola"] == "rasio"}


# ---------------------------------------------------------------------------
# Nominal uang
# ---------------------------------------------------------------------------
# Konversi satuan uang juga perhitungan, jadi dikerjakan di sini, bukan oleh LLM. Kasus H27
# (laporan 2026-10-10): LLM membaca "0,2 M" sebagai 0,2 juta (M = million), padahal dalam
# keuangan Indonesia M = miliar. LLM cukup menyalin teks nominal dari pertanyaan.

_NOMINAL_RE = re.compile(r"^(?:rp\.?)?\s*(\d[\d.,]*)\s*([a-z]*)\.?$")


def _kelompok_ribuan(teks: str, pemisah: str) -> bool:
    """'3,500,000' (pemisah ',') -> True: 1-3 angka di depan, lalu kelompok tepat 3 angka."""
    bagian = teks.split(pemisah)
    return len(bagian) > 1 and 1 <= len(bagian[0]) <= 3 and all(len(b) == 3 for b in bagian[1:])


def _angka_id(teks: str, tanpa_satuan: bool = False) -> float:
    """Angka gaya Indonesia maupun Inggris. Aturan pemisah:
    - titik DAN koma: yang paling kanan = desimal, yang lain = ribuan
      ('1.250.000,5' dan '1,250,000.5' -> 1250000.5)
    - koma saja, beberapa kelompok 3 angka = ribuan ('3,500,000' -> 3500000; kasus H28)
    - koma tunggal: desimal ('0,2' -> 0.2), KECUALI nominal tanpa satuan dengan 3 angka di belakang koma
      ('Rp3,500' -> 3500), karena Rp3,5 dan Rp3,500 tidak mungkin bermakna 3,5 rupiah
    - titik saja: kelompok 3 angka = ribuan ('1.250.000', '4.250'), selain itu desimal ('1.5')"""
    if "," in teks and "." in teks:
        if teks.rfind(",") > teks.rfind("."):
            return float(teks.replace(".", "").replace(",", "."))
        return float(teks.replace(",", ""))
    if "," in teks:
        if teks.count(",") > 1:
            if not _kelompok_ribuan(teks, ","):
                raise ValueError(f"angka '{teks}' tidak jelas")
            return float(teks.replace(",", ""))
        if tanpa_satuan and _kelompok_ribuan(teks, ","):
            return float(teks.replace(",", ""))
        return float(teks.replace(",", "."))
    bagian = teks.split(".")
    if len(bagian) > 1 and all(len(b) == 3 for b in bagian[1:]):
        return float("".join(bagian))
    if len(bagian) > 2:
        raise ValueError(f"angka '{teks}' tidak jelas")
    return float(teks)


def baca_nominal(nilai, nama: str) -> tuple[float, str | None]:
    """Nominal dari LLM -> (rupiah, teks asli). Angka biasa dipakai apa adanya; teks seperti
    "Rp1.250.000.000", "900jt", "0,2 M", "2 milyar" dibaca dengan aturan SATUAN_NOMINAL."""
    if isinstance(nilai, bool):
        raise ValueError(f"{nama} harus berupa angka atau teks nominal (diberikan: {nilai!r})")
    if isinstance(nilai, (int, float)):
        return float(nilai), None
    asli = str(nilai).strip()
    # "Rp1.000.000,-" dan "500 juta rupiah" juga lazim ditulis
    m = _NOMINAL_RE.match(re.sub(r"\s*rupiah$", "", asli.lower().rstrip("-").strip()))
    if not m or m.group(2) not in SATUAN_NOMINAL:
        raise ValueError(f"{nama} '{asli}' tidak terbaca. Tulis nominal persis seperti di pertanyaan, "
                         f"mis. \"300 jt\", \"0,2 M\", \"Rp1.250.000.000\" (satuan: "
                         f"{', '.join(s for s in SATUAN_NOMINAL if s)})")
    try:
        angka = _angka_id(m.group(1).rstrip(".,"), tanpa_satuan=m.group(2) == "")
    except ValueError as e:
        raise ValueError(f"{nama} '{asli}' tidak terbaca: {e}") from None
    return angka * SATUAN_NOMINAL[m.group(2)], asli


def _tulis_nominal(rupiah: float, asli: str | None) -> str:
    return f"\"{asli}\" = Rp{_fmt(rupiah)}" if asli else _fmt(rupiah)


# ---------------------------------------------------------------------------
# IKU 1 — Angka Efisiensi Edukasi (AEE), hlm. 49–50
# ---------------------------------------------------------------------------

def iku1_aee_prodi(jenjang: str, lulus_tepat_waktu: int, total_mahasiswa: int,
                   pindah: int = 0, drop_out: int = 0, cuti_lebih: int = 0) -> dict:
    """AEE satu program pendidikan. Mahasiswa pindah, DO, dan cuti melebihi ketentuan
    TIDAK dihitung (Ketentuan c)."""
    jenjang = jenjang.upper()
    ideal = _pilih(AEE_IDEAL, jenjang, "Jenjang")
    for nilai, nama in [(lulus_tepat_waktu, "lulus_tepat_waktu"), (pindah, "pindah"),
                        (drop_out, "drop_out"), (cuti_lebih, "cuti_lebih")]:
        _tidak_negatif(nilai, nama)
    basis = total_mahasiswa - pindah - drop_out - cuti_lebih
    _wajib_positif(basis, "Basis mahasiswa (total − pindah − DO − cuti berlebih)")
    _tidak_melebihi(lulus_tepat_waktu, basis, "Lulus tepat waktu", "basis mahasiswa")

    aee = lulus_tepat_waktu / basis
    capaian = (aee * 100) / ideal
    langkah = []
    if basis != total_mahasiswa:
        langkah.append(f"Basis = {total_mahasiswa} − {pindah} pindah − {drop_out} DO − {cuti_lebih} cuti = {basis} "
                       f"(Ketentuan c: pindah/DO/cuti berlebih tidak dihitung)")
    langkah += [
        f"AEE realisasi = {lulus_tepat_waktu} / {basis} × 100% = {_fmt(_pct(aee))}%",
        f"AEE ideal {jenjang} = {ideal}% (masa tempuh {MASA_TEMPUH[jenjang]} semester)",
        f"Tingkat pencapaian = {_fmt(_pct(aee))}% / {ideal}% × 100% = {_fmt(round(capaian * 100, 2))}%",
    ]
    hasil = {"aee_realisasi_pct": _pct(aee), "tingkat_pencapaian_pct": round(capaian * 100, 2)}
    return _keluaran("iku1_aee_prodi", hasil, "%", langkah)


def iku1_aee_pt(realisasi_per_jenjang: dict[str, float]) -> dict:
    """AEE perguruan tinggi = rata-rata tingkat pencapaian semua program pendidikan (Formula c).
    realisasi_per_jenjang: {"D3": 30, "S1": 22.5, ...} dalam persen."""
    if not realisasi_per_jenjang:
        raise ValueError("realisasi_per_jenjang kosong; isi minimal satu jenjang, mis. {\"S1\": 22.5}")
    langkah, capaian = [], []
    for jenjang, realisasi in realisasi_per_jenjang.items():
        ideal = _pilih(AEE_IDEAL, jenjang.upper(), "Jenjang")
        _tidak_negatif(realisasi, f"Realisasi {jenjang}")
        c = realisasi / ideal * 100
        capaian.append(c)
        langkah.append(f"Tingkat pencapaian {jenjang} = {_fmt(realisasi)}% / {ideal}% = {_fmt(round(c, 2))}%")
    hasil = sum(capaian) / len(capaian)
    langkah.append(f"AEE PT = ({' + '.join(_fmt(round(c, 2)) + '%' for c in capaian)}) / {len(capaian)} "
                   f"= {_fmt(round(hasil, 2))}%")
    return _keluaran("iku1_aee_pt", round(hasil, 2), "%", langkah)


# ---------------------------------------------------------------------------
# IKU 2 — Lulusan bekerja / studi lanjut / wirausaha, hlm. 51–52
# ---------------------------------------------------------------------------

def jumlah_berbobot(kategori: dict[str, int], bobot: dict[str, float], total: int) -> tuple[float, list[str]]:
    _wajib_positif(total, "Total")
    langkah, skor = [], 0.0
    for nama, n in kategori.items():
        k = _pilih(bobot, nama, "Kategori")
        _tidak_negatif(n, f"Jumlah '{nama}'")
        skor += n * k
        langkah.append(f"{nama}: {n} × {_fmt(k)} = {_fmt(round(n * k, 4))}")
    _tidak_melebihi(sum(kategori.values()), total, "Jumlah seluruh kategori", "total")
    langkah.append(f"Σ(n·k) = {_fmt(round(skor, 4))}")
    langkah.append(f"Capaian = {_fmt(round(skor, 4))} / {total} × 100% = {_fmt(round(skor / total * 100, 2))}%")
    return round(skor / total * 100, 2), langkah


def iku2(total_responden: int, kategori: dict[str, int]) -> dict:
    hasil, langkah = jumlah_berbobot(kategori, BOBOT_IKU2, total_responden)
    return _keluaran("iku2", hasil, "%", langkah)


def iku2_responden_minimum(jumlah_lulusan: int, galat: float = GALAT_SLOVIN) -> dict:
    """Rumus Slovin n = N / (N·d² + 1). Dokumen menulis '× 100%', tetapi hasil yang bermakna
    adalah jumlah orang, dibulatkan ke atas."""
    _wajib_positif(jumlah_lulusan, "Jumlah lulusan")
    _wajib_positif(galat, "Galat")
    n = jumlah_lulusan / (jumlah_lulusan * galat ** 2 + 1)
    langkah = [f"N·d² = {jumlah_lulusan} × {galat}² = {_fmt(round(jumlah_lulusan * galat ** 2, 4))}",
               f"n = {jumlah_lulusan} / ({_fmt(round(jumlah_lulusan * galat ** 2, 4))} + 1) = {_fmt(round(n, 2))}",
               f"Dibulatkan ke atas = {math.ceil(n)} responden"]
    return _keluaran("iku2_responden_minimum", math.ceil(n), "responden", langkah)


# ---------------------------------------------------------------------------
# IKU 3 — Mahasiswa berkegiatan / berprestasi di luar prodi, hlm. 53–54
# ---------------------------------------------------------------------------

def bobot_sks(sks: int) -> float:
    _tidak_negatif(sks, "SKS")
    for aturan in BOBOT_SKS:
        if aturan["sks_kurang_dari"] is None or sks < aturan["sks_kurang_dari"]:
            return aturan["bobot"]


def iku3(total_mahasiswa: int, kegiatan: list[dict] | None = None, prestasi: list[dict] | None = None) -> dict:
    """kegiatan: [{"jumlah": 100, "sks": 20}, ...]
    prestasi: [{"jumlah": 5, "tingkat": "nasional", "peringkat": "juara1"}, ...]"""
    _wajib_positif(total_mahasiswa, "Total mahasiswa")
    langkah, skor = [], 0.0
    for k in kegiatan or []:
        _tidak_negatif(k["jumlah"], "Jumlah mahasiswa kegiatan")
        b = bobot_sks(k["sks"])
        skor += k["jumlah"] * b
        langkah.append(f"Kegiatan {k['sks']} SKS: {k['jumlah']} × {_fmt(b)} = {_fmt(round(k['jumlah'] * b, 4))}")
    for p in prestasi or []:
        _tidak_negatif(p["jumlah"], "Jumlah mahasiswa berprestasi")
        b = _pilih(BOBOT_PRESTASI, (p["tingkat"], p["peringkat"]), "Prestasi (tingkat, peringkat)")
        skor += p["jumlah"] * b
        langkah.append(f"Prestasi {p['peringkat']} {p['tingkat']}: {p['jumlah']} × {_fmt(b)} = "
                       f"{_fmt(round(p['jumlah'] * b, 4))}")
    hasil = skor / total_mahasiswa * 100
    langkah += [f"Σ(n·k) = {_fmt(round(skor, 4))}",
                f"Capaian = {_fmt(round(skor, 4))} / {total_mahasiswa} × 100% = {_fmt(round(hasil, 2))}%"]
    return _keluaran("iku3", round(hasil, 2), "%", langkah)


# ---------------------------------------------------------------------------
# IKU 6 — Publikasi bereputasi internasional, hlm. 63
# ---------------------------------------------------------------------------

def iku6(total_publikasi: int, publikasi: dict[str, int], kolaborasi: dict[str, int] | None = None) -> dict:
    """publikasi: {"q1": 40, ...} (tanpa kolaborasi internasional)
    kolaborasi: {"q1": 4, ...} publikasi dengan penulis luar negeri (mendapat bonus)."""
    _wajib_positif(total_publikasi, "Total publikasi")
    kolaborasi = kolaborasi or {}
    langkah, skor = [], 0.0
    for jenis, n in publikasi.items():
        k = _pilih(BOBOT_PUBLIKASI, jenis, "Jenis publikasi")
        _tidak_negatif(n, f"Jumlah publikasi '{jenis}'")
        skor += n * k
        langkah.append(f"{jenis}: {n} × {_fmt(k)} = {_fmt(round(n * k, 4))}")
    for jenis, n in kolaborasi.items():
        dasar = _pilih(BOBOT_PUBLIKASI, jenis, "Jenis publikasi")
        _tidak_negatif(n, f"Jumlah kolaborasi '{jenis}'")
        k = dasar + BONUS_KOLABORASI
        skor += n * k
        langkah.append(f"{jenis} + kolaborasi internasional: {n} × ({_fmt(dasar)} + "
                       f"{_fmt(BONUS_KOLABORASI)}) = {_fmt(round(n * k, 4))}")
    _tidak_melebihi(sum(publikasi.values()) + sum(kolaborasi.values()), total_publikasi,
                    "Jumlah publikasi per jenis", "total publikasi")
    hasil = skor / total_publikasi * 100
    langkah += [f"Σ(n·k) = {_fmt(round(skor, 4))}",
                f"Capaian = {_fmt(round(skor, 4))} / {total_publikasi} × 100% = {_fmt(round(hasil, 2))}%"]
    return _keluaran("iku6", round(hasil, 2), "%", langkah, pakai_catatan=bool(kolaborasi))


# ---------------------------------------------------------------------------
# IKU dengan rumus rasio (a / b × 100%) — daftarnya di spec (pola "rasio")
# ---------------------------------------------------------------------------

def rasio(kode: str, pembilang: float, penyebut: float) -> dict:
    nama_a, nama_b, _ = _pilih(RASIO, kode, "Kode rasio")
    _tidak_negatif(pembilang, f"Pembilang ({nama_a})")
    _wajib_positif(penyebut, f"Penyebut ({nama_b})")
    hasil = pembilang / penyebut * 100
    langkah = [f"({nama_a}) / ({nama_b}) × 100%",
               f"= {_fmt(pembilang)} / {_fmt(penyebut)} × 100% = {_fmt(round(hasil, 2))}%"]
    return _keluaran(kode, round(hasil, 2), "%", langkah)


# ---------------------------------------------------------------------------
# IKU 9 — Pendapatan non pendidikan/UKT, hlm. 59
# ---------------------------------------------------------------------------

def iku9(total_pendapatan: float | str, rincian: dict[str, float | str]) -> dict:
    """Nominal boleh angka (satuan bebas asal konsisten) atau teks seperti di pertanyaan
    ("Rp1.250.000.000", "900jt", "0,2 M"); teks diubah ke rupiah oleh baca_nominal."""
    jenis = {isinstance(v, str) for v in [total_pendapatan, *rincian.values()]}
    if len(jenis) > 1:
        # "2 milyar" (teks -> rupiah) dicampur 300 (angka, mis. maksudnya juta) = satuan tidak konsisten
        raise ValueError("Nominal tercampur antara teks dan angka. Tulis SEMUA nominal sebagai teks persis "
                         "seperti di pertanyaan, mis. {\"total_pendapatan\": \"2 milyar\", \"rincian\": "
                         "{\"hibah_riset\": \"300 jt\"}}")
    total, total_asli = baca_nominal(total_pendapatan, "Total pendapatan")
    _wajib_positif(total, "Total pendapatan")
    langkah = [f"Total pendapatan: {_tulis_nominal(total, total_asli)}"] if total_asli else []
    diakui = jumlah = 0.0
    for pos, nilai_asli in rincian.items():
        nilai, asli = baca_nominal(nilai_asli, f"Pos '{pos}'")
        _tidak_negatif(nilai, f"Pos '{pos}'")
        jumlah += nilai
        if pos in PENDAPATAN_DIAKUI:
            diakui += nilai
            langkah.append(f"{pos}: {_tulis_nominal(nilai, asli)} → DIHITUNG (Kriteria a)")
        elif pos in PENDAPATAN_TIDAK_DIAKUI:
            langkah.append(f"{pos}: {_tulis_nominal(nilai, asli)} → TIDAK dihitung (Kriteria b)")
        else:
            raise ValueError(f"Pos pendapatan '{pos}' belum dikategorikan; tambahkan ke daftar diakui/tidak diakui")
    _tidak_melebihi(jumlah, total, "Jumlah rincian pendapatan", "total pendapatan")
    if jumlah < total * (1 - 1e-9):
        # bukan error (bisa ada pendapatan lain yang tidak dirinci), tetapi ditampilkan agar
        # salah baca nominal mudah terlihat
        langkah.append(f"Catatan: rincian berjumlah {_fmt(jumlah)} dari total {_fmt(total)}; selisih "
                       f"{_fmt(total - jumlah)} dianggap pendapatan lain yang tidak dihitung")
    hasil = diakui / total * 100
    langkah.append(f"Capaian = {_fmt(diakui)} / {_fmt(total)} × 100% = {_fmt(round(hasil, 2))}%")
    return _keluaran("iku9", round(hasil, 2), "%", langkah)


# ---------------------------------------------------------------------------
# IKU 11b — Predikat SAKIP, hlm. 66 ; IKU 12 — standar penghasilan dosen, hlm. 60
# ---------------------------------------------------------------------------

def iku11b_predikat(nilai_akhir: float) -> dict:
    if not 0 <= nilai_akhir <= 100:
        raise ValueError(f"Nilai akhir SAKIP harus 0–100 (diberikan: {nilai_akhir})")
    predikat = next(p for batas, p in PREDIKAT_SAKIP if nilai_akhir >= batas)
    langkah = [f"Nilai akhir {_fmt(nilai_akhir)} → rentang tabel predikat SAKIP → {predikat}"]
    return _keluaran("iku11b_predikat", predikat, "predikat", langkah)


def iku12_penghasilan_minimum(ump: float | str, jabatan: list[str]) -> dict:
    """ump dalam rupiah penuh, atau teks seperti di pertanyaan ("3,5jt", "Rp 4.250.000")."""
    ump, ump_asli = baca_nominal(ump, "UMP")
    _wajib_positif(ump, "UMP")
    if ump < UMP_MINIMUM:
        # kemungkinan besar salah baca satuan atau pemisah ribuan (kasus H28: Rp3.500 alih-alih Rp3.500.000)
        raise ValueError(f"UMP Rp{_fmt(ump)} tidak wajar (di bawah Rp{_fmt(UMP_MINIMUM)}); periksa satuan atau "
                         f"pemisah ribuan, dan tulis nominal persis seperti di pertanyaan")
    hasil = {}
    langkah = [f"UMP: {_tulis_nominal(ump, ump_asli)}"] if ump_asli else []
    for j in jabatan:
        kelipatan = _pilih(KELIPATAN_UMP, j, "Jabatan")
        nilai = kelipatan * ump
        hasil[j] = nilai
        langkah.append(f"{j}: ≥ {_fmt(kelipatan)} × UMP = {_fmt(kelipatan)} × Rp{_fmt(ump)} = Rp{_fmt(nilai)}")
    return _keluaran("iku12_penghasilan_minimum", hasil, "Rp", langkah)


# ---------------------------------------------------------------------------
# Daftar fungsi yang boleh dipanggil (dipakai LLM lewat tool calling)
# ---------------------------------------------------------------------------

REGISTRY = {
    "iku1_aee_prodi": iku1_aee_prodi,
    "iku1_aee_pt": iku1_aee_pt,
    "iku2": iku2,
    "iku2_responden_minimum": iku2_responden_minimum,
    "iku3": iku3,
    "iku6": iku6,
    "rasio": rasio,
    "iku9": iku9,
    "iku11b_predikat": iku11b_predikat,
    "iku12_penghasilan_minimum": iku12_penghasilan_minimum,
}


def hitung(fungsi: str, **argumen) -> dict:
    if fungsi not in REGISTRY:
        raise KeyError(f"Fungsi '{fungsi}' tidak ada di registry: {sorted(REGISTRY)}")
    return REGISTRY[fungsi](**argumen)


def daftar_rumus(ikuCode: str | None = None) -> list[dict]:
    """Metadata rumus dari spec, opsional disaring per IKU (mis. "IKU 001").
    Berguna untuk BE/FE atau untuk membatasi rumus sesuai cakupan halaman."""
    return [r for r in SPEC["rumus"] if ikuCode in (None, r["ikuCode"])]
