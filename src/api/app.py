"""
FastAPI server untuk RAG service IKU.

Endpoint:
  - POST /v1/answer: Jawab pertanyaan menggunakan RAG + kalkulator IKU
  - GET /health: Health check
"""

import os
import re
import sys
import json
import logging
from pathlib import Path

import openai
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load .env file (call this in endpoints too for reload)
def load_env():
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)

# Setup path untuk import internal modules
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "retrieval"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "generation"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "calculator"))

load_env()

from answer import Chatbot  # noqa: E402
from tools import jalankan_spreadsheet_tool  # noqa: E402
import iku_formulas as calc  # noqa: E402

# Inisialisasi Chatbot sekali saat startup (bukan per-request)
bot: Chatbot | None = None


def get_chatbot() -> Chatbot:
    """Lazy initialization Chatbot."""
    global bot
    if bot is None:
        logger.info("Initializing Chatbot...")
        bot = Chatbot()
        logger.info(f"Chatbot ready (model: {bot.model})")
    return bot


def detect_intent(question: str) -> str:
    """
    Detect intent pertanyaan dengan keyword-based pattern matching.
    Returns: "definisi", "formula", atau "data"

    Priority:
    1. "data" - jika menyebut data kampus (dengan/tanpa kata "saya"),
                atau menanyakan nilai/angka/capaian/realisasi/target IKU
    2. "formula" - jika tanya "rumus", "cara hitung"
    3. "definisi" - default (tanya konsep/penjelasan IKU)

    CATATAN: Semua intent "data" akan di-return sebagai fetch_data ke Next.js.
    Next.js yang mengambil spreadsheet user dari DB dan mengirim konteks ke sini.
    jalankan_spreadsheet_tool() dengan email dummy TIDAK dipakai lagi.
    """
    q_lower = question.lower()

    # Intent: DATA
    # Grup A: eksplisit menyebut kepemilikan user ("saya", "kampus saya", dll)
    data_patterns_personal = [
        r"\biku\s+\d+\s+saya\b",             # "IKU 1 saya"
        r"\bnilai\s+(iku\s+\d+\s+)?saya\b",  # "nilai IKU 1 saya", "nilai saya"
        r"\bkampus\s+saya\b",
        r"\bpt\s+saya\b",
        r"\bdata\s+(kampus|saya|kami)\b",
        r"\bcapaian\s+(iku\s+\d+\s+)?saya\b",
        r"\bberapa\s+(nilai\s+)?iku\s+\d+\s+saya\b",
        r"\buniversitas\s+saya\b",
        r"\binstitusi\s+saya\b",
    ]

    # Grup B: menanyakan nilai/angka/capaian IKU tanpa kata "saya"
    # (pertanyaan yang memerlukan data spreadsheet, bukan definisi/rumus)
    data_patterns_numeric = [
        r"\b(berapa|tampilkan|lihat|tunjukkan|cek|periksa)\b.{0,40}\biku\s*\d+\b",
        r"\biku\s*\d+\b.{0,40}\b(berapa|nilai|angka|capaian|skor|persentase|realisasi|target)\b",
        r"\b(nilai|capaian|skor|realisasi|target|persentase)\b.{0,40}\biku\s*\d+\b",
        r"\bdata\b.{0,30}\biku\s*\d+\b",
        r"\b(berapa|nilai|capaian)\s+(iku\s+\d+|mahasiswa|lulusan|dosen|prodi|fakultas)\b",
    ]

    if any(re.search(p, q_lower) for p in data_patterns_personal):
        return "data"

    if any(re.search(p, q_lower) for p in data_patterns_numeric):
        return "data"

    # Intent: FORMULA
    formula_keywords = ["rumus", "formula", "cara hitung", "cara menghitung", "bagaimana menghitung"]
    if any(kw in q_lower for kw in formula_keywords):
        return "formula"

    # Intent: DEFINISI (default)
    return "definisi"






def clean_formula_lines(text: str) -> list[str]:
    r"""
    Membersihkan teks rumus mentah dari chunk dokumen:
    - Menghapus pembatas tabel pipa (| Formula | ... |)
    - Mengonversi \frac{A}{B} -> (A) / (B)
    - Menghapus \(, \), \[, \], $, \text{...}, dsb.
    - Menghapus teks contoh angka atau tabel perhitungan manual
    - Memisahkan sub-formula berurutan (misal: a. ... b. ...)
    """
    s = text.strip()
    s = re.sub(r"^\|\s*(?:formula)?\s*\|\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^\|\s*", "", s)
    s = re.sub(r"\s*\|\s*$", "", s)

    # Abaikan baris header tabel atau metadata
    if s.lower().startswith("satuan") or s.startswith("---") or not s:
        return []

    # Konversi \frac{A}{B} -> (A) / (B)
    while r"\frac" in s:
        match = re.search(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", s)
        if not match:
            break
        num, denom = match.group(1).strip(), match.group(2).strip()
        s = s[:match.start()] + f"({num}) / ({denom})" + s[match.end():]

    # Bersihkan LaTeX formatting
    s = re.sub(r"\\text\{([^{}]+)\}", r"\1", s)
    s = s.replace(r"\(", "").replace(r"\)", "").replace(r"\[", "").replace(r"\]", "").replace("$", "")
    s = s.replace(r"\ ", " ")
    s = re.sub(r"\\sum(?:_\{[^}]*\})?(?:\^\{[^}]*\})?", "Σ", s)

    # Pisahkan sebelum 'Contoh Perhitungan' agar tidak membawa tabel angka contoh
    if "contoh perhitungan" in s.lower():
        idx = s.lower().find("contoh perhitungan")
        s = s[:idx].strip()

    # Potong jika ada 'Dimana:' di akhir
    if "dimana:" in s.lower():
        idx = s.lower().find("dimana:")
        s = s[:idx].strip()

    # Pisahkan jika ada sub-formula berurutan (misal: a. ... b. ... c. ...)
    parts = re.split(r"\s+(?=[a-d]\.\s+)", s)
    res = []
    for p in parts:
        p_clean = re.sub(r"[ \t]+", " ", p).strip()
        # Abaikan baris contoh / nilai diketahui
        if any(k in p_clean.lower() for k in ["realisasi =", "diketahui"]):
            continue
        if p_clean and any(sym in p_clean for sym in ["=", "÷", "×", "x", "%", "/", "+", "Σ"]):
            res.append(p_clean)
    return res


def extract_blocks(hasil: dict) -> list[dict] | None:
    """
    Ekstrak field blocks: Array<{ type: 'formula' | 'note' | 'metric', lines: string[] }>
    secara deterministik dari kalkulator resmi dan metadata dokumen.
    """
    blocks = []

    # 1. METRIC: Ekstrak ringkasan utama dari hasil kalkulator
    metric_lines = []
    seen_metrics = set()
    kalkulator = hasil.get("kalkulator") or []
    for item in kalkulator:
        hasil_dict = item.get("hasil")
        if not isinstance(hasil_dict, dict) or "error" in hasil_dict:
            continue

        argumen = item.get("argumen", {})
        if isinstance(argumen, str):
            try:
                argumen = json.loads(argumen)
            except Exception:
                argumen = {}

        thn = argumen.get("tahun")
        fak = argumen.get("fakultas")
        jnj = argumen.get("jenjang")

        nilai = hasil_dict.get("hasil")
        if nilai is None:
            nilai = hasil_dict.get("aee_pt")

        satuan = hasil_dict.get("satuan", "")
        if satuan:
            satuan = f" {satuan}".replace(" %", "%")

        if nilai is not None:
            if thn and not fak and not jnj:
                line = f"Capaian Agregat Kampus ({thn}): {nilai}{satuan}"
            elif fak and thn:
                line = f"Fakultas {fak} ({thn}): {nilai}{satuan}"
            elif jnj and thn:
                line = f"Jenjang {jnj} ({thn}): {nilai}{satuan}"
            elif thn:
                line = f"Tahun {thn}: {nilai}{satuan}"
            else:
                fungsi = argumen.get("fungsi", "Kalkulasi")
                line = f"{fungsi}: {nilai}{satuan}"

            if line not in seen_metrics:
                seen_metrics.add(line)
                metric_lines.append(line)

    if metric_lines:
        blocks.append({
            "type": "metric",
            "lines": metric_lines[:15],
        })

    # 2. FORMULA: Ekstrak baris rumus
    formula_lines = []
    seen_formulas = set()

    # Prioritas 1: Dari kalkulator resmi (calc.RUMUS) jika tersedia
    for item in kalkulator:
        argumen = item.get("argumen", {})
        if isinstance(argumen, str):
            try:
                argumen = json.loads(argumen)
            except Exception:
                argumen = {}
        fungsi = argumen.get("fungsi")
        if fungsi and hasattr(calc, "RUMUS") and fungsi in calc.RUMUS:
            for ft in calc.RUMUS[fungsi].get("formula_teks", []):
                cleaned = str(ft).strip()
                if cleaned and cleaned not in seen_formulas:
                    seen_formulas.add(cleaned)
                    formula_lines.append(cleaned)

    # Prioritas 2: HANYA jika calc.RUMUS belum menghasilkan formula, ekstrak & bersihkan dari chunks
    if not formula_lines:
        chunks = hasil.get("chunks") or []
        for c in chunks:
            bagian = str(c.get("bagian") or "").lower()
            if "formula" in bagian or c.get("sectionType") == "formula":
                content = c.get("content", "")
                for raw_line in content.splitlines():
                    for cleaned_line in clean_formula_lines(raw_line):
                        if cleaned_line not in seen_formulas:
                            seen_formulas.add(cleaned_line)
                            formula_lines.append(cleaned_line)

    # Prioritas 3: Fallback ke sumber_rumus jika masih kosong
    if not formula_lines and hasil.get("sumber_rumus"):
        for sr in hasil.get("sumber_rumus", []):
            sr_str = str(sr).strip()
            if sr_str and sr_str not in seen_formulas:
                seen_formulas.add(sr_str)
                formula_lines.append(sr_str)

    if formula_lines:
        blocks.append({
            "type": "formula",
            "lines": formula_lines[:10],
        })

    # 3. NOTE: Ekstrak catatan sumber atau catatan tafsir
    note_lines = []
    seen_notes = set()
    chunks = hasil.get("chunks") or []
    for c in chunks:
        for sn in c.get("source_notes", []):
            note_text = sn.get("note", "").strip() if isinstance(sn, dict) else str(sn).strip()
            if note_text and note_text not in seen_notes:
                seen_notes.add(note_text)
                note_lines.append(note_text)

        catatan = c.get("catatan")
        if catatan and str(catatan).strip() not in seen_notes:
            seen_notes.add(str(catatan).strip())
            note_lines.append(str(catatan).strip())

    if note_lines:
        blocks.append({
            "type": "note",
            "lines": note_lines[:10],
        })

    return blocks if blocks else None


def format_response(hasil: dict, intent: str, include_citations: bool = True) -> dict:
    """
    Format response dari Chatbot.ask() ke format RAGResponse.
    """
    citations = []
    if include_citations and hasil.get("sitasi"):
        for sitasi in hasil.get("sitasi", []):
            match = re.search(
                r"\[(\d+)\]\s*(.+?),\s*hlm\.\s*(\d+)(?:–(\d+))?\s*(?:\((.+)\))?",
                sitasi,
            )
            if match:
                chunk_num = match.group(1)
                doc_title = match.group(2).strip()
                page_start = int(match.group(3))
                page_end = int(match.group(4)) if match.group(4) else page_start
                iku_id = match.group(5)
                citations.append({
                    "id": f"CHUNK_{chunk_num}",
                    "documentTitle": doc_title,
                    "documentVersion": "V1",
                    "page": page_start,
                    "page_end": page_end,
                    "ikuCode": iku_id if iku_id and iku_id != "" else None,
                })

    grounded = len(citations) > 0
    blocks = extract_blocks(hasil)

    return {
        "answer": hasil.get("jawaban", ""),
        "citations": citations,
        "blocks": blocks,
        "grounded": grounded,
        "outOfScope": None,
        "action": None,
    }


app = FastAPI(title="IKU RAG Service", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    """Inisialisasi Chatbot saat startup."""
    global bot
    if bot is None:
        logger.info("Initializing Chatbot on startup...")
        bot = Chatbot()
        logger.info(f"Chatbot ready (model: {bot.model})")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/v1/answer")
def answer(
    question: dict,
    x_internal_token: str | None = Header(default=None, alias="X-Internal-Token"),
):
    """
    Jawab pertanyaan menggunakan RAG + kalkulator IKU.

    Body:
        - question: string
        - scope: object atau null (opsional)

    Response:
        - answer: string
        - citations: list (dari sitasi)
        - grounded: boolean
        - outOfScope: boolean atau null
        - action: {type: "fetch_data"} jika butuh data spreadsheet
    """
    # Load .env (in case of reload)
    load_env()
    
    # Cek token autentikasi
    expected_token = os.getenv("RAG_SERVICE_TOKEN")
    if expected_token is None:
        logger.error("RAG_SERVICE_TOKEN not configured in environment")
        raise HTTPException(
            status_code=500,
            detail="RAG_SERVICE_TOKEN tidak dikonfigurasi di environment",
        )

    if x_internal_token != expected_token:
        logger.warning("Invalid token received")
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

    # Parse request
    q = question.get("question", "")
    scope = question.get("scope")
    spreadsheet_context = question.get("spreadsheet_context")  # optional: dari Next.js saat 2nd call
    
    logger.info(f"Spreadsheet context received: {len(spreadsheet_context) if spreadsheet_context else 0} chars")

    if not q:
        return JSONResponse(
            status_code=400,
            content={"error": "question is required"},
        )

    try:
        # DETEKSI INTENT dengan LLM
        chatbot = get_chatbot()

        # Jika sudah ada spreadsheet_context (second call dari Next.js), langsung proses dengan RAG
        if spreadsheet_context:
            hasil = chatbot.ask_with_spreadsheet(q, spreadsheet_context)
            # Izinkan format_response memproses sitasi yang ditemukan dari RAG chunks
            response = format_response(hasil, "data", include_citations=True)
            response["action"] = None  
            return response

        intent = detect_intent(q)

        if intent == "data":
            # Untuk pertanyaan data, kembalikan instruksi untuk fetch data
            # TypeScript backend yang akan panggil executeTool()
            # Kemudian kirim ulang ke /v1/answer dengan data spreadsheet
            response = {
                "answer": "Memproses permintaan data kampus Anda...",
                "citations": [],
                "blocks": None,
                "grounded": True,
                "outOfScope": None,
                "action": {
                    "type": "fetch_data",
                    "payload": {
                        "needsSpreadsheet": True,
                        "question": q,
                    }
                },
            }
            return response

        # Intent bukan "data" -> proses normal dengan RAG
        hasil = chatbot.ask(q)
        response = format_response(hasil, intent)
        return response


    except openai.RateLimitError as e:
        logger.error(f"Rate limit error: {e}")
        return JSONResponse(
            status_code=503,
            content={"error": "LLM rate limit exceeded"},
        )
    except openai.APITimeoutError as e:
        logger.error(f"Timeout error: {e}")
        return JSONResponse(
            status_code=504,
            content={"error": "LLM request timeout"},
        )
    except (openai.APIConnectionError, openai.APIStatusError) as e:
        logger.error(f"LLM API error: {e}")
        return JSONResponse(
            status_code=502,
            content={"error": f"LLM service error: {str(e)}"},
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
