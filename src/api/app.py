"""
FastAPI server untuk RAG service IKU.

Endpoint:
  - POST /v1/answer: Jawab pertanyaan menggunakan RAG + kalkulator IKU
  - GET /health: Health check
"""

import os
import re
import sys
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

    return {
        "answer": hasil.get("jawaban", ""),
        "citations": citations,
        "grounded": grounded,
        "outOfScope": None,
        "action": None if intent != "data" and not hasil.get("chunks") else None,
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
async def answer(
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
