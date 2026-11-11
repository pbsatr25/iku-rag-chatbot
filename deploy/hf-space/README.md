---
title: IKU RAG Service
emoji: 🎓
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

Layanan RAG Asisten IKU (FastAPI). Dipanggil oleh dasbor Next.js lewat `POST /v1/answer`
dengan header `X-Internal-Token`. Cek status: `GET /health`.
