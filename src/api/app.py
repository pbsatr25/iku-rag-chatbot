"""
FastAPI server untuk RAG service IKU.

Endpoint:
  - POST /v1/answer: Jawab pertanyaan menggunakan RAG + kalkulator IKU
  - GET /health: Health check
"""

import os
import re
import sys
from pathlib import Path

import openai
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

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
        print("Initializing Chatbot...")
        bot = Chatbot()
        print(f"Chatbot ready (model: {bot.model})")
    return bot


def detect_intent(question: str) -> str:
    """
    Detect intent pertanyaan dengan keyword-based approach.
    Returns: "definisi", "formula", atau "data"
    
    Priority:
    1. "data" - jika menyebut "kampus saya", "data saya", "nilai IKU X kampus/pt"
    2. "formula" - jika tanya "rumus", "cara hitung"
    3. "definisi" - default (tanya arti/penjelasan IKU)
    """
    q_lower = question.lower()
    
    # Intent: DATA (prioritas tertinggi)
    # Pola: berapa + (nilai IKU | jumlah | data) + (kampus | pt | saya | kami)
    data_keywords = [
        "kampus saya", "kampus kami", "pt saya", "pt kami",
        "data saya", "data kami", "data kampus",
        "nilai iku", "capaian iku"
    ]
    
    if any(kw in q_lower for kw in data_keywords):
        # Pastikan ada "berapa" atau kata tanya numerik lainnya
        if any(word in q_lower for word in ["berapa", "jumlah", "total", "nilai", "capaian"]):
            return "data"
    
    # Intent: FORMULA
    formula_keywords = [
        "rumus", "formula", "cara hitung", "cara menghitung",
        "bagaimana menghitung", "bagaimana hitung", "langkah hitung"
    ]
    if any(kw in q_lower for kw in formula_keywords):
        return "formula"
    
    # Intent: DEFINISI (default)
    definisi_keywords = [
        "apa itu", "definisi", "pengertian", "maksud", "arti",
        "jelaskan", "penjelasan"
    ]
    if any(kw in q_lower for kw in definisi_keywords):
        return "definisi"
    
    # Jika ada "berapa" tapi tidak menyebut kampus -> tetap definisi
    # (mungkin tanya tentang rumus umum: "berapa bobot IKU 3?")
    return "definisi"


def format_response(hasil: dict, intent: str) -> dict:
    """
    Format response dari Chatbot.ask() ke format RAGResponse.
    - Jika intent == "data": return response tanpa sitasi (data dari spreadsheet)
    - Jika intent != "data": return response dengan sitasi
    """
    citations = []
    if intent != "data" and hasil.get("sitasi"):
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
        "action": None if intent != "data" else {"type": "fetch_data"},
    }


app = FastAPI(title="IKU RAG Service", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    """Inisialisasi Chatbot saat startup."""
    global bot
    if bot is None:
        print("Initializing Chatbot on startup...")
        bot = Chatbot()
        print(f"Chatbot ready (model: {bot.model})")


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
        raise HTTPException(
            status_code=500,
            detail="RAG_SERVICE_TOKEN tidak dikonfigurasi di environment",
        )

    if x_internal_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")

    # Parse request
    q = question.get("question", "")
    scope = question.get("scope")

    if not q:
        return JSONResponse(
            status_code=400,
            content={"error": "question is required"},
        )

    try:
        # DETEKSI INTENT dulu
        intent = detect_intent(q)
        print(f"Intent detected: {intent}")

        if intent == "data":
            # Untuk pertanyaan data, kembalikan instruksi untuk fetch data
            # TypeScript backend yang akan panggil executeTool()
            # Kemudian kirim ulang ke /v1/answer dengan data spreadsheet
            return {
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

        # Intent bukan "data" -> proses normal dengan RAG
        chatbot = get_chatbot()
        hasil = chatbot.ask(q)
        return format_response(hasil, intent)

    except openai.RateLimitError:
        return JSONResponse(
            status_code=503,
            content={"error": "LLM rate limit exceeded"},
        )
    except openai.APITimeoutError:
        return JSONResponse(
            status_code=504,
            content={"error": "LLM request timeout"},
        )
    except (openai.APIConnectionError, openai.APIStatusError) as e:
        return JSONResponse(
            status_code=502,
            content={"error": f"LLM service error: {str(e)}"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
