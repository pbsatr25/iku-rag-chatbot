# Layanan RAG IKU untuk Hugging Face Spaces (SDK Docker, CPU basic gratis).
# Rahasia (LLM_API_KEY, RAG_SERVICE_TOKEN, dst.) diisi di Settings Space, bukan di file .env.
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/home/user/.cache/huggingface

# Spaces menjalankan container sebagai user UID 1000
RUN useradd -m -u 1000 user
WORKDIR /home/user/app

COPY requirements.txt .
RUN pip install torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu \
 && pip install -r requirements.txt

USER user

# Unduh bge-m3 saat build agar startup tidak menunggu unduhan ~2 GB
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"

# ChromaDB menulis ke folder vectorstore, jadi harus milik user
COPY --chown=user src ./src
COPY --chown=user data ./data

EXPOSE 7860
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "7860"]
