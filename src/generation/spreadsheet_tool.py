"""
spreadsheet_tool.py
Tool untuk mengambil data spreadsheet user dari Google Sheets.

Digunakan ketika pertanyaan memerlukan data internal kampus (misal: "berapa nilai IKU 3 kampus saya?").

Alur:
1. Ambil data_source_connection dari database (user email -> Google Sheets URL)
2. Fetch xlsx dari Google Sheets export URL
3. Parse → rows + columns
4. Return untuk LLM proses (dengan konteks IKU dari retrieval RAG)
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from prisma import Prisma
except ImportError:
    Prisma = None


# Mock data untuk development (bila Prisma belum terkonfigurasi)
MOCK_SPREADSHEET_DATA = [
    {"tahun": "2024", "fakultas": "Teknik", "jenjang": "S1", "mahasiswa": 150, "lulusan": 45, "dosen": 25},
    {"tahun": "2024", "fakultas": "Ekonomi", "jenjang": "S1", "mahasiswa": 200, "lulusan": 60, "dosen": 30},
    {"tahun": "2023", "fakultas": "Teknik", "jenjang": "S1", "mahasiswa": 140, "lulusan": 40, "dosen": 24},
]


def get_spreadsheet_data_for_user(user_email: str) -> dict:
    """
    Ambil data spreadsheet untuk user tertentu.
    
    For now: return mock data.
    In production: query Prisma → data_source_connections table.
    """
    if Prisma is None:
        # Development mode: return mock
        return {
            "status": "ok",
            "source": {"id": "mock", "name": "Spreadsheet Mock Data"},
            "columns": ["tahun", "fakultas", "jenjang", "mahasiswa", "lulusan", "dosen"],
            "rows": MOCK_SPREADSHEET_DATA,
            "truncated": False,
        }
    
    # Production: query database
    return _query_database(user_email)


def _query_database(user_email: str) -> dict:
    """Query Prisma untuk ambil data_source_connection user."""
    # Placeholder - implement bila Prisma tersedia
    return {
        "status": "error",
        "message": "Prisma belum terkonfigurasi. Gunakan mode mock data untuk development.",
    }


def format_spreadsheet_context(rows: list[dict], columns: list[str], max_rows: int = 200) -> str:
    """
    Format spreadsheet data menjadi konteks teks untuk LLM.
    
    Output format:
    - Header columns
    - Max max_rows rows
    - Instruksi untuk LLM bagaimana memakai data ini
    """
    lines = [
        "DATA SPREADSHEET USER (untuk jawab pertanyaan tentang nilai IKU kampus user):",
        f"Kolom: {', '.join(columns)}",
        "",
    ]
    
    rows_shown = rows[:max_rows]
    lines.append(f"Baris (max {max_rows} ditampilkan):")
    
    for i, row in enumerate(rows_shown, 1):
        row_str = " | ".join(f"{k}={v}" for k, v in row.items())
        lines.append(f"  [{i}] {row_str}")
    
    if len(rows) > max_rows:
        lines.append(f"  ... (dan {len(rows) - max_rows} baris lagi)")
    
    lines.extend([
        "",
        "PANDUAN untuk LLM:",
        "- Data ini untuk jawab pertanyaan tentang nilai IKU kampus user",
        "- Jangan mengarang data - hanya gunakan nilai yang ada di spreadsheet",
        "- Jika data tidak ada, katakan 'tidak ditemukan di spreadsheet user'",
        "- Untuk hitungan IKU, panggil alat hitung_iku dengan data dari spreadsheet ini",
    ])
    
    return "\n".join(lines)
