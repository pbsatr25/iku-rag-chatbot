"""
tools.py
Alat (tool) yang boleh dipanggil LLM:
- `hitung_iku`: untuk menghitung IKU dari rumus resmi
- `query_spreadsheet`: untuk mengambil data spreadsheet user

Daftar kunci (kategori IKU 2, bobot prestasi, jenis publikasi, dst.) diambil
langsung dari kalkulator, jadi petunjuk untuk LLM selalu sama dengan kodenya.
"""
import inspect
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "calculator"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "generation"))

import iku_formulas as calc  # noqa: E402
from spreadsheet_tool import format_spreadsheet_context, get_spreadsheet_data_for_user  # noqa: E402


def _daftar(items) -> str:
    return ", ".join(f'"{x}"' for x in items)


def panduan_argumen() -> str:
    """Contoh format argumen untuk setiap fungsi kalkulator."""
    tingkat = sorted({t for t, _ in calc.BOBOT_PRESTASI})
    peringkat = sorted({p for _, p in calc.BOBOT_PRESTASI})
    return "\n".join([
        '- iku1_aee_prodi: {"jenjang": "S1", "lulus_tepat_waktu": 40, "total_mahasiswa": 200, '
        '"pindah": 0, "drop_out": 0, "cuti_lebih": 0}  (jenjang: ' + _daftar(calc.AEE_IDEAL) + ")",
        '- iku1_aee_pt: {"realisasi_per_jenjang": {"D3": 30, "S1": 22.5}}  (nilai AEE realisasi dalam persen)',
        '- iku2: {"total_responden": 500, "kategori": {"<kunci>": jumlah, ...}}  (kunci: '
        + _daftar(calc.BOBOT_IKU2) + ")",
        '- iku2_responden_minimum: {"jumlah_lulusan": 2000}',
        '- iku3: {"total_mahasiswa": 1000, "kegiatan": [{"jumlah": 100, "sks": 20}], '
        '"prestasi": [{"jumlah": 5, "tingkat": "nasional", "peringkat": "juara1"}]}  '
        f"(tingkat: {_daftar(tingkat)}; peringkat: {_daftar(peringkat)})",
        '- iku6: {"total_publikasi": 200, "publikasi": {"q1": 40}, "kolaborasi": {"q1": 4}}  (jenis: '
        + _daftar(calc.BOBOT_PUBLIKASI) + "; kolaborasi = publikasi dengan penulis luar negeri)",
        '- rasio: {"kode": "iku5", "pembilang": 30, "penyebut": 120}  (kode: '
        + "; ".join(f'"{k}" = {a} / {b}' for k, (a, b, _) in calc.RASIO.items()) + ")",
        # contoh sengaja memakai angka yang TIDAK ada di test set agar evaluasi tetap jujur
        '- iku9: {"total_pendapatan": "3 milyar", "rincian": {"hibah_riset": "450 jt", "pelatihan": "0,1 M", '
        '"ukt": "2,45 M"}}  (masukkan SEMUA pos yang disebut, termasuk yang tidak dihitung; pos yang dihitung: '
        + _daftar(sorted(calc.PENDAPATAN_DIAKUI)) + "; pos yang tidak dihitung: "
        + _daftar(sorted(calc.PENDAPATAN_TIDAK_DIAKUI)) + ")",
        '- iku11b_predikat: {"nilai_akhir": 82}',
        '- iku12_penghasilan_minimum: {"ump": "Rp2.900.000", "jabatan": ["lektor"]}  (jabatan: '
        + _daftar(calc.KELIPATAN_UMP) + ")",
        "PENTING untuk nominal uang (iku9, iku12): tulis sebagai teks PERSIS seperti di pertanyaan, "
        'misalnya "Rp1.750.000.000", "650jt", "0,3 M", "4 milyar". JANGAN mengubah satuannya sendiri; '
        "kalkulator yang mengubah ke rupiah (M = miliar, jt = juta).",
    ])


TOOL_HITUNG_IKU = {
    "type": "function",
    "function": {
        "name": "hitung_iku",
        "description": (
            "Menghitung capaian IKU dengan rumus resmi Buku IKU Diktisaintek Berdampak. "
            "WAJIB dipakai untuk setiap perhitungan angka; jangan menghitung sendiri. "
            "Mengembalikan hasil, langkah perhitungan, dan sumber halaman rumus.\n"
            "Format argumen per fungsi:\n" + panduan_argumen()
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "fungsi": {
                    "type": "string",
                    "enum": sorted(calc.REGISTRY),
                    "description": "Nama fungsi kalkulator yang dipakai.",
                },
                # argumen dikirim sebagai teks JSON agar skemanya sederhana dan diterima
                # semua penyedia (Gemini, Ollama, OpenAI)
                "argumen_json": {
                    "type": "string",
                    "description": "Argumen fungsi dalam bentuk teks JSON, sesuai contoh format di atas.",
                },
            },
            "required": ["fungsi", "argumen_json"],
        },
    },
}


NAMA_ALAT = TOOL_HITUNG_IKU["function"]["name"]


def arahkan_dari_rasio(fungsi: str | None, argumen: dict) -> str | None:
    """LLM kadang memakai fungsi umum 'rasio' untuk IKU yang punya fungsi sendiri
    (kasus H11/H26/H27: rasio kode 'iku6'/'iku9'), lalu menyerah saat ditolak. Beri tahu
    fungsi yang benar beserta format argumennya agar LLM bisa langsung mengulang."""
    kode = str(argumen.get("kode", "")).strip().lower()
    if fungsi != "rasio" or not kode or kode in calc.RASIO:
        return None
    pengganti = [f for f in sorted(calc.REGISTRY) if f == kode or f.startswith(kode + "_")]
    if not pengganti:
        return None
    format_argumen = [b for b in panduan_argumen().splitlines()
                      if any(b.startswith(f"- {f}:") for f in pengganti)]
    return (f"'{kode}' bukan kode rasio: IKU ini punya fungsi sendiri ({', '.join(pengganti)}). "
            f"Panggil ulang {NAMA_ALAT} dengan fungsi tersebut dan data asli dari pertanyaan "
            f"(jangan dihitung dulu). Format: " + " ".join(format_argumen))

def baca_permintaan(argumen_teks: str) -> tuple[str | None, dict]:
    """Ambil (fungsi, argumen) dari teks argumen LLM. Toleran terhadap variasi format
    yang sering muncul pada model berbeda:
    - argumen_json berupa teks JSON (format resmi) atau sudah berupa objek
    - kunci 'argumen' alih-alih 'argumen_json'
    - argumen ditaruh langsung di tingkat atas: {"fungsi": "rasio", "kode": "iku5", ...}"""
    permintaan = json.loads(argumen_teks or "{}")
    if not isinstance(permintaan, dict):
        raise ValueError("argumen alat harus berupa objek JSON")
    fungsi = permintaan.get("fungsi")
    argumen = permintaan.get("argumen_json", permintaan.get("argumen"))
    if argumen is None:
        argumen = {k: v for k, v in permintaan.items() if k != "fungsi"}
    if isinstance(argumen, str):
        argumen = json.loads(argumen or "{}")
    if not isinstance(argumen, dict):
        raise ValueError("argumen_json harus berupa objek JSON, mis. {\"kode\": \"iku5\", ...}")
    return fungsi, argumen


def jalankan_alat(nama: str, argumen_teks: str) -> dict:
    """Jalankan alat yang diminta LLM. Kesalahan dikembalikan sebagai pesan, bukan crash,
    supaya LLM bisa memperbaiki argumennya di putaran berikutnya.

    Nama alat yang tidak baku (terpotong 'hit...', salah ketik 'hitung-iku') tetap diterima
    bila isinya jelas permintaan kalkulator (ada 'fungsi' yang terdaftar): alatnya hanya satu."""
    try:
        fungsi, argumen = baca_permintaan(argumen_teks)
    except json.JSONDecodeError as e:
        return {"error": f"argumen_json bukan JSON yang valid: {e}"}
    except ValueError as e:
        return {"error": str(e)}

    if nama != NAMA_ALAT and fungsi not in calc.REGISTRY:
        return {"error": f"Alat '{nama}' tidak dikenal. Alat yang tersedia: {NAMA_ALAT}."}
    if fungsi not in calc.REGISTRY:
        return {"error": f"Fungsi '{fungsi}' tidak ada. Pilihan: {', '.join(sorted(calc.REGISTRY))}"}
    arahan = arahkan_dari_rasio(fungsi, argumen)
    if arahan:
        return {"error": arahan}
    try:
        return calc.hitung(fungsi, **argumen)
    except TypeError as e:
        # biasanya nama parameter salah; beri tahu parameter yang benar agar LLM bisa memperbaiki
        return {"error": f"TypeError: {e}. Parameter yang benar untuk {fungsi}: "
                         f"{inspect.signature(calc.REGISTRY[fungsi])}"}
    except (KeyError, ValueError, ZeroDivisionError) as e:
        return {"error": f"{type(e).__name__}: {e}. Periksa nama fungsi dan format argumen."}


# ==============================================================================
# SPREADSHEET TOOL
# ==============================================================================

TOOL_QUERY_SPREADSHEET = {
    "type": "function",
    "function": {
        "name": "query_spreadsheet",
        "description": (
            "Ambil data spreadsheet user untuk menjawab pertanyaan tentang nilai IKU kampus. "
            "Panggil ini BILA PERTANYAAN menyebut 'kampus saya', 'data saya', atau butuh data internal "
            "untuk menghitung nilai IKU. Jangan panggil untuk pertanyaan definisi/rumus IKU.\n"
            "Mengembalikan kolom dan baris data dari spreadsheet user (max 200 baris)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "filter_json": {
                    "type": "string",
                    "description": (
                        "Filter data dalam bentuk JSON (opsional). Contoh: "
                        '{"tahun": "2024", "fakultas": "Teknik"}. '
                        "Kosongkan string kosong jika tidak perlu filter."
                    ),
                }
            },
            "required": [],
        },
    },
}

NAMA_ALAT_SPREADSHEET = TOOL_QUERY_SPREADSHEET["function"]["name"]


def jalankan_spreadsheet_tool(filter_json: str = "{}") -> dict:
    """
    Jalankan query spreadsheet tool.
    
    Args:
        filter_json: Filter dalam format JSON string (contoh: '{"tahun": "2024"}')
    
    Returns:
        dict dengan keys: status, source, columns, rows, truncated, data_context
    """
    try:
        # Ambil data user (untuk MVP, gunakan email dummy atau user context)
        # Dalam production, ini akan menggunakan user_email dari auth context
        # TODO: Ganti hardcoded email untuk production
        user_email = "demo@kampus.example.com"  # placeholder
        
        result = get_spreadsheet_data_for_user(user_email)
        
        if result["status"] != "ok":
            return result
        
        # Format konteks untuk LLM
        context_text = format_spreadsheet_context(
            rows=result["rows"],
            columns=result["columns"],
            max_rows=200
        )
        
        return {
            "status": "ok",
            "source": result["source"],
            "columns": result["columns"],
            "rows": result["rows"],
            "truncated": result.get("truncated", False),
            "data_context": context_text,
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error mengambil spreadsheet: {type(e).__name__}: {e}",
        }

