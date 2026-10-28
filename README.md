# Chatbot RAG IKU Diktisaintek Berdampak

Chatbot *Retrieval-Augmented Generation* (RAG) untuk penjaminan mutu perguruan tinggi. Chatbot menjawab pertanyaan tentang **Indikator Kinerja Utama (IKU) Diktisaintek Berdampak**: definisi, kriteria, ketentuan, dan perhitungan rumus. Setiap jawaban disertai **sitasi halaman** dari dokumen resmi.

Sumber pengetahuan:

- `Buku IKU Diktisaintek Berdampak_V1.pdf` (143 halaman, sumber utama)
- `PPT IKU Diktisaintek Berdampak_PTS V2.pdf` (sumber pendukung)

> [!IMPORTANT]
> **Tim Backend / AI Ops:** mulai dari **[Untuk tim Backend](#untuk-tim-backend)** di bawah, lalu baca panduan lengkapnya di **[docs/02-desain/integrasi_backend.md](docs/02-desain/integrasi_backend.md)**. Kalian tidak perlu menjalankan pipeline RAG untuk mulai bekerja.

### Mulai dari sini sesuai peran

| Peran | Baca ini dulu | Lalu |
|---|---|---|
| **Backend / AI Ops** | [Untuk tim Backend](#untuk-tim-backend) | [Panduan integrasi backend](docs/02-desain/integrasi_backend.md) (kontrak API, tugas BE, batasan) |
| **Frontend** | [Kontrak API di panduan integrasi](docs/02-desain/integrasi_backend.md#4-kontrak-api) | `src/types/chat.ts` di repo FE |
| **AI Engineer / kontributor pipeline** | [Setup](#setup-langkah-demi-langkah) | [Menjalankan chatbot](#menjalankan-chatbot), [Alur kerja pengembangan](#alur-kerja-pengembangan) |
| **QA** | [Pengujian & evaluasi](#pengujian--evaluasi) | [Test set 44 soal](data/evaluation/test_set_buku_iku.md) |

## Daftar isi

1. [Status proyek](#status-proyek)
2. [**Untuk tim Backend**](#untuk-tim-backend)
3. [Arsitektur pipeline](#arsitektur-pipeline)
4. [Struktur repositori](#struktur-repositori)
5. [Prasyarat](#prasyarat)
6. [Setup (langkah demi langkah)](#setup-langkah-demi-langkah)
7. [Menjalankan chatbot](#menjalankan-chatbot)
8. [Menjalankan pipeline dari awal](#menjalankan-pipeline-dari-awal)
9. [Pengujian & evaluasi](#pengujian--evaluasi)
10. [Alur kerja pengembangan](#alur-kerja-pengembangan)
11. [Troubleshooting](#troubleshooting)
12. [Dokumentasi lanjutan](#dokumentasi-lanjutan)

## Status proyek

| Tahap | Status | Script utama |
|---|---|---|
| 1. Parsing PDF → Markdown (+ penanda halaman) | ✅ Selesai | `src/parsing/parse_pdf.py` |
| 2. Processing → JSON terstruktur + validasi | ✅ Selesai | `src/processing/` |
| 3. Chunking berbasis struktur (bge-m3, ≤ 512 token) | ✅ Selesai | `src/chunking/chunk_structured.py` |
| 4. Embedding `BAAI/bge-m3` | ✅ Selesai | `src/embedding/embed_chunks.py` |
| 5. Vector DB ChromaDB (cosine) | ✅ Selesai | `src/vectordb/build_chroma.py` |
| 6. Retrieval hybrid (dense + BM25 + RRF, IKU boost, dedupe, sambung tabel) | ✅ Selesai | `src/retrieval/retriever.py`, `src/retrieval/sambung_tabel.py` |
| 6b. Kalkulator rumus IKU (*formula registry*, pembacaan nominal uang) | ✅ Selesai | `src/calculator/iku_formulas.py` |
| 7. LLM + tool calling kalkulator + sitasi + pemeriksaan jawaban (generation) | ✅ Selesai, lulus **42/44** soal uji | `src/generation/answer.py`, `src/generation/chat_cli.py` |
| 7b. Evaluasi jawaban otomatis (44 soal) | ✅ Selesai | `src/evaluation/run_answer_tests.py` |
| 8. Layanan HTTP (FastAPI) untuk backend | ⬜ Belum. Rancangan: [docs/02-desain/integrasi_backend.md](docs/02-desain/integrasi_backend.md) | – |
| 9. Antarmuka chat di dasbor | ⬜ Belum (repo FE masih memakai data mock). Demo sementara: Streamlit, lihat [Demo web](#demo-web-untuk-dicoba-orang-lain-streamlit--tunnel) | `src/ui/app_streamlit.py` |

### Hasil evaluasi terakhir

Model `openai/gpt-oss-120b` (Groq, paket gratis), koleksi `pmpt_qa_v2` (605 chunk), test set 44 soal. Laporan lengkap, penjelasan tiap metrik, dan hasil per soal: **[docs/03-evaluasi/laporan_evaluasi_akhir.md](docs/03-evaluasi/laporan_evaluasi_akhir.md)**. Data mentah ada di [reports/evaluation/](reports/evaluation/).

**Jawaban chatbot (44 soal):**

| Metrik | Hasil |
|---|---|
| Lulus semua pemeriksaan otomatis | **42/44** |
| Kalkulator dipanggil (30 soal hitungan) | 30/30 |
| Hasil kalkulator = kunci | 30/30 |
| Halaman sitasi benar | hitungan 30/30; definisi 12/13 |
| Fakta kunci soal definisi | 10/12 |

Perkembangan jumlah soal lulus: 20/36 (8 Okt) → 36/44 (9 Okt) → 41/44 (10 Okt) → **42/44** (11 Okt, setelah bug nominal uang H28 diperbaiki). Dua soal belum lulus: **D03** (rujukan AI kadang berbentuk `[*1*]` sehingga sitasi tidak muncul) dan **D06** (syarat pendampingan dosen tidak disebut).

**Pencarian dokumen (43 soal dalam cakupan, retriever v2):**

| Metrik | Hasil |
|---|---|
| Hit@1 | 30/43 (69,8%) |
| Hit@3 | 39/43 (90,7%) |
| **Hit@5** | **41/43 (95,3%)** |
| MRR@5 | 0,806 |
| Hit@5 gabungan (bukti tersebar di beberapa chunk) | 42/43 (97,7%) |
| Halaman sitasi benar | 40/41 (97,6%) |
| Rata-rata waktu per query | 0,06 detik |

> [!NOTE]
> - **Soal uji belum independen.** Ke-44 soal sudah dipakai untuk menyetel sistem, jadi skor di atas cenderung lebih tinggi daripada performa nyata. Perlu 10–15 soal baru dari pengguna nyata (demo Streamlit mengumpulkan pertanyaan untuk ini).
> - **Reranker `bge-reranker-v2-m3` diuji dan tidak dipakai:** Hit@5 turun 41 → 40 dan waktu naik 0,05 → 15,7 detik per query.
> - **Belum tercakup:** 12 rumus sub-indikator IKU, pembatasan jawaban per halaman dasbor, dan ingatan percakapan (lihat [panduan integrasi](docs/02-desain/integrasi_backend.md)).
> - Hasil di atas memakai model gratis yang tidak selalu stabil (nama alat salah ketik, respons kosong, kadang LaTeX); semuanya ditangani dengan percobaan ulang dan perapian otomatis, tetapi perlu diuji ulang saat model diganti.

## Untuk tim Backend

Ringkasan untuk tim Backend dasbor Monev IKU (Next.js + Prisma). Detail lengkap, contoh JSON, dan alasannya ada di **[panduan integrasi backend](docs/02-desain/integrasi_backend.md)**.

**Kondisi sekarang:** inti chatbot (retrieval, kalkulator rumus, LLM + sitasi) sudah jalan dan lulus 42 dari 44 soal uji (lihat [hasil evaluasi](#hasil-evaluasi-terakhir)). **Layanan HTTP-nya belum ada**; UI chat di repo FE masih memakai data mock. Titik sambung yang akan dibungkus FastAPI adalah `Chatbot().ask(question)` di [`src/generation/answer.py`](src/generation/answer.py), yang mengembalikan jawaban, sitasi, hasil kalkulator, dan peringatan.

**Arsitektur yang diusulkan:**

```text
Panel chat (FE) ──POST /api/chat──► Next.js Route Handler  ← dikerjakan BE
                                        │  sesi, validasi, rate limit, log,
                                        │  + conversationId, messageId, disclaimer
                                        ▼
                         Layanan RAG Python (FastAPI)      ← dikerjakan tim AI
                         POST /v1/answer (internal saja)
                                        │
                                        ▼
                         Penyedia LLM (Groq/Gemini/OpenAI) ← API key hanya di layanan RAG
```

**Yang dikerjakan BE** (urut prioritas):

1. Sesi server dengan cookie `httpOnly`, agar `userEmail` tepercaya (saat ini sesi FE masih di `localStorage`).
2. `POST /api/chat`: validasi `question` (maks. 2.000 karakter) dan `scope` (`overview` atau `IKU 001/002/003/005/007/009`), panggil layanan RAG dengan timeout dan pembatalan, petakan error ke 400/401/429/502/503.
3. Batas laju **per pengguna dan global**: kuota LLM free tier dibagi seluruh aplikasi.
4. Tabel log percakapan di Prisma (`ChatConversation`, `ChatMessage`, `MessageCitation`).
5. Env server-only: `RAG_SERVICE_URL`, `RAG_SERVICE_TOKEN` (tanpa prefix `NEXT_PUBLIC_`).

Selama layanan RAG belum siap, `/api/chat` bisa dibangun dengan **stub** yang mengembalikan contoh respons di [bagian 4.2 panduan](docs/02-desain/integrasi_backend.md#42-be--layanan-rag-post-v1answer-usulan).

**Yang perlu disepakati dulu** (bagian 3 panduan): RAG tetap di Python atau di-port ke TypeScript, ChromaDB atau pgvector, dokumen yang di-index, dan siapa yang menambahkan `disclaimer`/`conversationId`.

**Batasan penting:**

| Hal | Artinya untuk BE |
|---|---|
| Kuota free tier kecil (Groq ±8.000 token/menit dan 200.000 token/hari per akun; satu soal ±7.000–10.000 token, jadi ±28 soal/hari) | Hanya cukup untuk demo satu pengguna; perlu rate limit global dan pesan 429 yang jelas. Untuk dipakai lebih luas perlu model berbayar |
| Layanan RAG memuat model `bge-m3` (±1,5 GB RAM) | Harus proses yang selalu hidup (container/VM), **bukan** serverless |
| Data free tier dapat dipakai penyedia LLM | Jangan kirim data internal kampus (isi spreadsheet, nama, NIM) |
| Rumus IKU dibutuhkan juga di dasbor | Pakai [`src/calculator/spec/buku_iku_v1.json`](src/calculator/spec/buku_iku_v1.json) + kasus uji [`test_inputs_hitung.json`](data/evaluation/test_inputs_hitung.json), jangan salin bobot manual |

## Arsitektur pipeline

```text
data/raw/*.pdf
   │  [1] parse_pdf.py          LlamaParse (butuh API key, berbayar kredit)
   ▼
data/parsed/*.md (+ .pages.json)
   │  [2] process_markdown.py   → validate_processed.py, validate_cross_source.py
   ▼
data/processed/*_processed.json
   │  [3] chunk_structured.py   → validate_chunks.py
   ▼
data/chunks/chunks.jsonl
   │  [4] embed_chunks.py       bge-m3, GPU disarankan
   ▼
data/embeddings/embeddings.npy + metadata.jsonl
   │  [5] build_chroma.py
   ▼
data/vectorstore/  (ChromaDB, koleksi pmpt_qa_v2)
   │  [6] retriever.py          dense + BM25 + RRF → IKU boost → dedupe → sambung tabel
   │                            (reranker tersedia tetapi tidak dipakai: hasilnya tidak lebih baik dan lambat)
   ▼
top-k chunk (bernomor [1]..[5]) ──► [7] answer.py  LLM (Groq/Gemini/Ollama/OpenAI lewat format OpenAI)
                                         │  ▲
                        alat hitung_iku  │  │  hasil + langkah + sumber halaman rumus
                                         ▼  │
                               [6b] iku_formulas.py   rumus dihitung deterministik, bukan oleh LLM
                                         │
                                         ▼
                      postproses.py: rapikan jawaban (LaTeX, rujukan), periksa angka vs kalkulator
                                         │
                                         ▼
                 jawaban + sitasi halaman (dari metadata chunk, bukan ditulis LLM) + PERINGATAN
```

Semua artefak tahap 1–4 **sudah di-commit**, jadi anggota tim tidak perlu mengulang parsing (berbayar) atau embedding (lama tanpa GPU). Hanya `data/vectorstore/` yang perlu dibangun sendiri karena berupa database biner (beberapa detik).

## Struktur repositori

```text
iku-rag-chatbot/
├── .github/
│   ├── workflows/ci.yml          # CI: cek sintaks + unit test di setiap push/PR
│   ├── ISSUE_TEMPLATE/           # template laporan bug, jawaban chatbot salah, usulan fitur
│   └── pull_request_template.md
├── data/                         # lihat data/README.md
│   ├── raw/                      # PDF sumber (input)
│   ├── parsed/                   # [1] Markdown hasil LlamaParse
│   ├── processed/                # [2] JSON terstruktur per dokumen
│   ├── chunks/                   # [3] chunks.jsonl
│   ├── embeddings/               # [4] vektor bge-m3 + metadata
│   ├── vectorstore/              # [5] ChromaDB (di-generate, tidak di-commit)
│   ├── metadata/                 # catatan cacat dokumen sumber (known_source_issues.json)
│   ├── evaluation/               # test set: 44 soal, input soal hitungan, fakta kunci soal definisi
│   ├── feedback/                 # log demo Streamlit (tidak di-commit)
│   └── legacy/v1/                # artefak pipeline v1 (baseline pembanding)
├── docs/                         # dokumentasi per fase SDLC, lihat docs/README.md
│   ├── 01-analisis/
│   ├── 02-desain/
│   └── 03-evaluasi/              # laporan evaluasi akhir chatbot (md, docx, pdf)
├── reports/
│   ├── validation/               # output script validasi
│   └── evaluation/               # laporan eval retrieval, uji hitungan, dan uji jawaban (bertanggal)
├── src/                          # satu folder = satu tahap pipeline
│   ├── parsing/  processing/  chunking/  embedding/
│   ├── vectordb/ retrieval/   calculator/ evaluation/
│   ├── generation/               # [7] chatbot: answer.py (retrieval ↔ LLM), llm_client, tools (hitung_iku),
│   │                             #     prompt, postproses, chat_cli.py
│   ├── ui/                       # demo web Streamlit
│   └── legacy/                   # script v1 yang sudah tidak dipakai
├── tests/                        # unit test (pytest), tanpa GPU
├── .env.example
├── requirements.txt              # dependency runtime
├── requirements-dev.txt          # dependency pengujian
├── CHANGELOG.md
├── CONTRIBUTING.md               # aturan branch, commit, PR
└── README.md
```

## Prasyarat

| Kebutuhan | Keterangan |
|---|---|
| **Python 3.13** | Versi yang sudah diuji: 3.13.5. Cek dengan `python --version` |
| **Git** | Untuk clone & kolaborasi |
| **GPU NVIDIA** (opsional, disarankan) | Diuji di RTX 4050 6 GB dengan CUDA 12.6. Tanpa GPU semua tetap jalan di CPU, hanya lebih lambat |
| **Ruang disk ±8 GB** | PyTorch CUDA ±3 GB, model `bge-m3` ±2,3 GB, reranker opsional ±2,3 GB (cache HuggingFace) |
| **Internet** | Saat pertama kali: unduh dependency & model dari HuggingFace |
| **LlamaCloud API key** (opsional) | Hanya untuk parsing ulang PDF. Hasil parsing sudah ada di repo |
| **API key LLM** (untuk chatbot) | Saat ini: Groq free tier dari [console.groq.com](https://console.groq.com). Alternatif: Gemini free tier, Ollama (lokal, tanpa key), atau OpenAI (berbayar). Lihat [Menjalankan chatbot](#menjalankan-chatbot) |

## Setup (langkah demi langkah)

Perintah di bawah memakai **PowerShell (Windows)**. Padanan Linux/macOS diberikan di bagian yang berbeda.

### 1. Clone repositori

```powershell
git clone https://github.com/<username>/iku-rag-chatbot.git
cd iku-rag-chatbot
```

### 2. Buat & aktifkan virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`

Jika muncul error *"running scripts is disabled on this system"*, jalankan sekali:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Pastikan prompt diawali `(.venv)` sebelum lanjut.

### 3. Pasang PyTorch (pilih salah satu)

PyTorch dipasang **sebelum** `requirements.txt` agar yang terpasang versi yang sesuai hardware.

```powershell
# GPU NVIDIA (CUDA 12.6)
pip install torch --index-url https://download.pytorch.org/whl/cu126

# CPU saja (tanpa GPU NVIDIA)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

Cek GPU terdeteksi (harus `True` jika memakai versi CUDA):

```powershell
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

### 4. Pasang dependency proyek

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt   # untuk menjalankan unit test
```

### 5. Konfigurasi environment

```powershell
Copy-Item .env.example .env
```

Isi `.env`:

| Variabel | Wajib untuk | Keterangan |
|---|---|---|
| `LLM_BASE_URL`, `LLM_MODEL` | Chatbot | Sudah terisi untuk Groq di `.env.example` (blok Gemini tersedia sebagai komentar); ganti bila memakai penyedia lain |
| `LLM_API_KEY` | Chatbot | API key penyedia yang dipilih: Groq ([console.groq.com](https://console.groq.com) → *API Keys*, diawali `gsk_`) atau Gemini ([Google AI Studio](https://aistudio.google.com) → *Get API key*) |
| `LLM_TIMEOUT`, `LLM_MAX_RETRIES` | Opsional | Batas tunggu per panggilan LLM (detik, default 60) dan percobaan ulang otomatis (default 2) |
| `LLAMA_CLOUD_API_KEY` | Parsing ulang PDF saja | Boleh dikosongkan; hasil parsing sudah ada di repo |

File `.env` sudah di-`.gitignore`, jadi jangan pernah di-commit, dan jangan menempel isinya di issue/PR/chat.

### 6. Bangun vector database

```powershell
python src/vectordb/build_chroma.py --reset
```

Hasil yang diharapkan: `Collection : pmpt_qa_v2`, `Distance : cosine`, `Jumlah data: 605`.

### 7. Verifikasi instalasi

```powershell
# a. Unit test kalkulator (cepat, tanpa GPU)
pytest

# b. Coba retriever secara interaktif (pertama kali mengunduh bge-m3 ±2,3 GB)
python src/retrieval/test_retrieval.py
#    Pertanyaan: Bagaimana rumus IKU 3?

# c. Evaluasi retrieval lengkap → angkanya harus sama dengan tabel di "Hasil evaluasi terakhir"
python src/evaluation/eval_retrieval.py
```

Setup selesai bila semua tes `pytest` lulus dan `eval_retrieval.py` menghasilkan Hit@1 30/43, Hit@5 41/43, serta MRR@5 0,806.

## Menjalankan chatbot

Chatbot memakai retriever v2 untuk mengambil 5 potongan dokumen, lalu LLM menyusun jawaban. Untuk soal hitungan, LLM **memanggil kalkulator IKU** (alat `hitung_iku`) dan tidak menghitung sendiri. Nomor halaman sitasi ditambahkan oleh kode dari metadata chunk, sehingga tidak bisa dikarang oleh LLM.

### Langkah menjalankan

1. Pastikan **setup langkah 1–6 selesai** (venv aktif, dependency terpasang, vector DB sudah dibangun).
2. Pastikan `LLM_BASE_URL`, `LLM_MODEL`, dan `LLM_API_KEY` di `.env` sudah terisi (setup langkah 5).
3. Jalankan dari root repo:

```powershell
python src/generation/chat_cli.py            # tanya-jawab di terminal
python src/generation/chat_cli.py --detail   # + argumen kalkulator & chunk yang dipakai (untuk debugging)
```

Ketik pertanyaan lalu Enter. Tekan **Enter kosong** untuk keluar. Saat pertama kali dijalankan, model `bge-m3` dimuat ke memori (beberapa detik; diunduh ±2,3 GB bila belum ada di cache).

### Contoh pertanyaan untuk mencoba

| Pertanyaan | Yang diuji | Yang diharapkan |
|---|---|---|
| `Apa itu IKU 3?` | Jawaban definisi + sitasi | Penjelasan dengan rujukan `[n]`, sumber Buku hlm. 53 |
| `Sebuah PT punya 1000 mahasiswa. 100 magang 20 SKS, 150 pertukaran 8 SKS, 50 riset 4 SKS, 5 juara 1 nasional, 10 finalis internasional. Berapa capaian IKU 3?` | Tool calling kalkulator | Kalkulator dipanggil, hasil **21,5%**, sumber rumus hlm. 53–54 |
| `Tracer study 400 responden, 280 bekerja. Berapa capaian IKU 2?` | Tanya balik bila data kurang | Menanyakan masa tunggu dan gaji lulusan |
| `Lulusan 400, yang bekerja 280, berapa capaian IKU 1?` | Meluruskan premis keliru | Menjelaskan bahwa itu IKU 2, bukan IKU 1 |
| `Berapa UKT di UGM tahun 2026?` | Menolak di luar dokumen | "Tidak ditemukan di dokumen IKU" |

### Membaca output

```text
<jawaban LLM dengan rujukan [1], [2], ...>

Sumber:
  [1] Buku IKU Diktisaintek Berdampak V1, hlm. 53–54 (IKU 3, Formula); juga di PPT hlm. 50; ...
Sumber rumus (kalkulator):
  Buku IKU Diktisaintek Berdampak V1, IKU 3 – Formula & Ketentuan Bobot, hlm. 53–54

PERINGATAN:
  - ...
```

- **Sumber**: rujukan `[n]` di jawaban diubah menjadi halaman dari metadata chunk. "Juga di …" menunjukkan salinan isi yang sama di Lampiran atau PPT.
- **Sumber rumus (kalkulator)**: muncul bila kalkulator dipanggil; halaman rumus ini selalu dari Bab V Buku.
- **PERINGATAN**: pemeriksaan otomatis menemukan masalah, misalnya rujukan `[n]` yang tidak ada di konteks, angka hasil kalkulator yang tidak muncul di jawaban, soal hitungan yang dijawab tanpa kalkulator, atau jawaban tanpa rujukan. Jawaban dengan peringatan perlu dicek manual; laporkan lewat template issue *Jawaban chatbot salah*.

### Mengganti penyedia LLM

Kode memakai library `openai` dengan format OpenAI, sehingga penyedia cukup diganti lewat `.env` tanpa mengubah kode:

| Penyedia | `LLM_BASE_URL` | `LLM_MODEL` (contoh) | `LLM_API_KEY` | Catatan |
|---|---|---|---|---|
| **Groq** (dipakai saat ini) | `https://api.groq.com/openai/v1` | `openai/gpt-oss-120b` | Dari [console.groq.com](https://console.groq.com), diawali `gsk_` | Free tier tanpa kartu: cepat (±3 detik/panggilan), tetapi dibatasi ±8.000 token/menit. Biaya di menu *Usage* hanya simulasi selama belum *upgrade* |
| Gemini | `https://generativelanguage.googleapis.com/v1beta/openai/` | `gemini-3.5-flash-lite` | Dari Google AI Studio | Free tier: ±20 request/hari per model, model flash sering 503 saat ramai; **data free tier dapat dipakai Google untuk meningkatkan produknya**, jadi jangan kirim data pribadi/internal |
| Ollama (lokal) | `http://localhost:11434/v1` | `qwen2.5:7b` | `ollama` (isi bebas) | Gratis & offline; pasang Ollama lalu `ollama pull qwen2.5:7b`. Model kecil, kualitas di bawah Gemini |
| OpenAI | `https://api.openai.com/v1` | model pilihan | Dari platform OpenAI | Berbayar per token |

Setelah mengganti penyedia, coba ulang contoh pertanyaan di atas untuk membandingkan kualitasnya.

### Demo web untuk dicoba orang lain (Streamlit + tunnel)

Demo ini berjalan **di laptop sendiri** (memakai GPU dan model yang sudah ada), lalu dibuka ke internet lewat tunnel. Tujuannya mengumpulkan pertanyaan nyata dan penilaian 👍/👎, **bukan** produk akhir (produk akhir: chatbot di dasbor, lihat [panduan integrasi backend](docs/02-desain/integrasi_backend.md)).

1. Isi `DEMO_PASSWORD` di `.env` (wajib bila link dibagikan). Disarankan memakai API key LLM terpisah, karena jatah free tier dibagi dengan evaluasi.
2. Jalankan aplikasi:

   ```powershell
   streamlit run src/ui/app_streamlit.py
   ```

   Buka `http://localhost:8501` untuk mencoba sendiri.
3. Di terminal kedua, buka tunnel lalu bagikan link `https://...` yang muncul beserta kata sandinya:

   ```powershell
   ngrok http 8501                                     # butuh akun ngrok + authtoken
   # atau tanpa akun:
   cloudflared tunnel --url http://localhost:8501      # link *.trycloudflare.com
   ```

Demo hanya bisa diakses selama laptop dan kedua terminal menyala. Setiap pengguna dibatasi `DEMO_MAKS_PERTANYAAN` pertanyaan per sesi, dan pertanyaan diproses bergantian. Semua tanya-jawab dan penilaian dicatat ke `data/feedback/demo_log.jsonl` (tidak di-commit), sebagai bahan soal baru untuk test set.

## Menjalankan pipeline dari awal

Pipeline penuh hanya perlu dijalankan bila **dokumen sumber atau logika suatu tahap berubah**. Jalankan dari root repo, berurutan. Cukup mulai dari tahap yang berubah.

| # | Perintah | Output | Hasil yang diharapkan |
|---|---|---|---|
| 1 | `python src/parsing/parse_pdf.py` | `data/parsed/` | Dokumen yang sudah punya hasil di-SKIP (tidak memakai kredit) |
| 2 | `python src/processing/process_markdown.py` | `data/processed/` | Buku ±815 blok, PPT ±601 blok |
| 2a | `python src/processing/validate_processed.py` | `reports/validation/` | `number_coverage_pct: 100.0`, `table_row_mismatches: 0` |
| 2b | `python src/processing/validate_cross_source.py` | `reports/validation/` | Selisih angka Buku vs PPT; yang sudah dikenal ditandai |
| 3 | `python src/chunking/chunk_structured.py` | `data/chunks/chunks.jsonl` | 605 chunk, `> max_tokens: 0` |
| 3a | `python src/chunking/validate_chunks.py` | `reports/validation/` | `HASIL AKHIR: SEMUA OK` |
| 4 | `python src/embedding/embed_chunks.py` | `data/embeddings/` | `Shape: (605, 1024)` |
| 5 | `python src/vectordb/build_chroma.py --reset` | `data/vectorstore/` | `Jumlah data: 605` |
| 6 | `python src/evaluation/eval_retrieval.py` | `reports/evaluation/` | Bandingkan dengan laporan sebelumnya |

> **Jangan lanjut ke tahap berikutnya bila validasi (2a atau 3a) tidak OK.**

Opsi penting:

```powershell
# Parsing
python src/parsing/parse_pdf.py --rebuild   # susun ulang .md dari .pages.json (gratis, tanpa API)
python src/parsing/parse_pdf.py --force     # parsing ulang semua PDF (memakai kredit LlamaCloud)

# Chunking: ukuran chunk
python src/chunking/chunk_structured.py --max-tokens 384 --min-tokens 64

# Embedding: GPU kehabisan memori
python src/embedding/embed_chunks.py --batch-size 4

# Inspeksi chunk
python src/chunking/show_chunks.py --iku 3 --bagian Formula
python src/chunking/show_chunks.py --cari "NUPTK" --maks 3
```

## Pengujian & evaluasi

| Jenis | Perintah | Butuh GPU/model? | Kapan dijalankan |
|---|---|---|---|
| Unit test kalkulator | `pytest` | Tidak | Setiap perubahan; otomatis di CI |
| Validasi data | `validate_processed.py`, `validate_chunks.py` | Tidak | Setelah processing / chunking |
| Evaluasi retrieval | `python src/evaluation/eval_retrieval.py` | bge-m3 | Setelah chunking / embedding / retriever berubah |
| Uji soal hitungan + sitasi | `python src/evaluation/run_calc_tests.py` | bge-m3 | Setelah kalkulator / retriever berubah |
| Uji chatbot manual | `python src/generation/chat_cli.py --detail` + [contoh pertanyaan](#contoh-pertanyaan-untuk-mencoba) | bge-m3 + API key LLM | Setelah prompt / alat / model LLM berubah |
| Evaluasi jawaban LLM otomatis (44 soal) | `python src/evaluation/run_answer_tests.py` | bge-m3 + API key LLM | Setelah prompt / alat / postproses / model / data berubah |

Variasi evaluasi:

```powershell
python src/evaluation/eval_retrieval.py --rerank            # + reranker (unduh ±2,3 GB sekali)
python src/evaluation/eval_retrieval.py --no-sambung-tabel  # tanpa penyambungan tabel, untuk perbandingan
python src/evaluation/run_calc_tests.py --id H07            # satu soal saja

# Baseline v1, untuk perbandingan (bangun koleksinya dulu)
python src/vectordb/build_chroma.py --embeddings-dir data/legacy/v1/embeddings --collection pmpt_qa --reset
python src/evaluation/eval_retrieval.py --preset lama --collection pmpt_qa --metadata data/legacy/v1/embeddings/metadata.jsonl --oos-threshold 0.9
```

### Evaluasi jawaban LLM (44 soal)

`run_answer_tests.py` menjalankan soal ke chatbot sungguhan (retriever + LLM + kalkulator), lalu memeriksa otomatis: kalkulator dipanggil, hasilnya sama dengan kunci, angka kunci ada di jawaban, halaman sitasi cocok, dan fakta kunci soal definisi muncul. Pemeriksaan otomatis hanya bantuan; baca juga jawaban lengkap di laporannya.

```powershell
python src/evaluation/run_answer_tests.py                       # semua 44 soal
python src/evaluation/run_answer_tests.py --tipe hitung         # 30 soal hitungan saja
python src/evaluation/run_answer_tests.py --id H07,D11          # soal tertentu
python src/evaluation/run_answer_tests.py --set inti            # kelompok soal (data/evaluation/test_sets.json)
python src/evaluation/run_answer_tests.py --jeda 30             # jeda antar-soal (detik), disarankan di Groq free tier
python src/evaluation/run_answer_tests.py --model <nama-model>  # model lain, penyedia sama (.env)
python src/evaluation/run_answer_tests.py --lanjut reports/evaluation/answer_test_<...>.json   # lanjutkan run yang terhenti
```

Satu soal memakai ±7.000–10.000 token, jadi jatah harian Groq free tier (200.000 token/akun) hanya cukup ±28 soal. Laporan ditulis ulang setiap selesai satu soal. Bila jatah harian habis, run berhenti dan laporan tersimpan; lanjutkan sisanya dengan `--lanjut` (besok, atau dengan API key lain di `.env`). Batas per menit (429) ditunggu otomatis. **Jangan pakai data internal kampus** pada free tier, karena penyedia dapat memakainya.

Evaluasi penuh sebaiknya diulang setiap kali model, prompt, kalkulator, atau data berubah. Jalankan juga `pytest` dan `eval_retrieval.py` untuk memastikan tidak ada yang turun.

### Test set

Test set ada di [data/evaluation/test_set_buku_iku.md](data/evaluation/test_set_buku_iku.md): 12 soal definisi & jebakan, 18 soal hitungan, dan 14 soal ketahanan (typo, bahasa santai, format angka/uang tidak baku). Setiap run menulis laporan bertanggal ke `reports/evaluation/`. Bandingkan metrik Hit@k, MRR, dan halaman sitasi. Jangan membandingkan angka *distance* antar-koleksi, karena koleksi v1 memakai L2 sedangkan v2 memakai cosine.

## Alur kerja pengembangan

Ringkasnya (detail di [CONTRIBUTING.md](CONTRIBUTING.md)):

1. **Rencanakan**: buat issue (template *Usulan fitur / eksperimen*) dengan target metrik.
2. **Branch**: `git switch develop && git switch -c feat/nama-fitur`.
3. **Implementasi**: ubah **satu hal** per eksperimen.
4. **Uji**: `pytest` + validasi + `eval_retrieval.py`.
5. **Pull request** ke `develop`, isi tabel metrik sebelum/sesudah di template PR.
6. **Rilis**: merge `develop` → `main`, perbarui [CHANGELOG.md](CHANGELOG.md), beri tag versi (`v0.3.0`).

## Troubleshooting

| Gejala | Penyebab & solusi |
|---|---|
| `Collection [pmpt_qa_v2] does not exist` | Vector DB belum dibangun. Jalankan `python src/vectordb/build_chroma.py --reset` |
| `torch.cuda.is_available()` = `False` padahal ada GPU | Terpasang torch versi CPU. `pip uninstall torch`, lalu pasang ulang dengan `--index-url .../cu126`. Pastikan driver NVIDIA terbaru |
| `CUDA out of memory` saat embedding / rerank | Tambahkan `--batch-size 4` (embedding), atau tutup aplikasi lain yang memakai GPU |
| `LLAMA_CLOUD_API_KEY belum ditemukan` | Hanya muncul saat parsing. Isi `.env`, atau pakai `--rebuild` bila hanya ingin menyusun ulang `.md` |
| Unduhan model HuggingFace lambat / terputus | Jalankan ulang; unduhan dilanjutkan dari cache `%USERPROFILE%\.cache\huggingface` |
| `Activate.ps1 cannot be loaded` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Hasil eval berbeda dari tabel di atas | Pastikan `data/chunks` dan `data/embeddings` tidak berubah (`git status`) dan vector DB dibangun ulang dengan `--reset` |
| `can't open file ... chat_cli.py` | Nama file harus persis `chat_cli.py` (garis bawah, bukan titik), dan perintah dijalankan dari root repo |
| Pesan error menyebut `C:\Python313\python.exe` / `ModuleNotFoundError` | venv belum aktif: jalankan `.venv\Scripts\Activate.ps1` hingga prompt diawali `(.venv)` |
| `ModuleNotFoundError: No module named 'openai'` | `pip install -r requirements.txt` (atau `pip install openai`) di venv yang aktif |
| `Isi LLM_BASE_URL, ... di file .env` | Tiga variabel `LLM_*` belum diisi di `.env` root repo (lihat setup langkah 5) |
| `401` / `API key not valid` | Key salah atau terpotong; salin ulang dari Google AI Studio |
| `404` / model tidak ditemukan | Nama `LLM_MODEL` tidak tersedia untuk akunmu; cek daftar model di AI Studio |
| `429` / kuota habis | Batas free tier tercapai; tunggu lalu coba lagi (klien mencoba ulang otomatis sebanyak `LLM_MAX_RETRIES`, default 2). Untuk evaluasi panjang di Groq, pakai `--jeda 30` |
| Evaluasi berhenti dengan pesan jatah harian (`tokens per day`) | Jatah 200.000 token/hari per akun habis. Laporan tersimpan; lanjutkan dengan `run_answer_tests.py --lanjut <laporan.json>` setelah jatah pulih atau dengan API key lain |
| Jawaban kosong, atau nama alat aneh (mis. `hitung_iku_`) di PERINGATAN | Perilaku model gratis (`gpt-oss`). Sudah ditangani dengan percobaan ulang otomatis dan dicatat di PERINGATAN; bukan berarti jawabannya salah |
| Peringatan `.env` baris tertentu tidak terbaca | Baris di `.env` harus berformat `NAMA=nilai`; beri `#` di depan baris catatan atau akun yang tidak dipakai |
| `503` / *high demand* | Server penyedia sedang penuh; coba lagi nanti atau ganti `LLM_MODEL` ke model lain |
| Error 400 tentang *thought signature* / function call | Pesan asisten yang meminta alat harus dikirim balik apa adanya; jangan ubah baris `message.model_dump(exclude_none=True)` di `answer.py` |

## Dokumentasi lanjutan

- [docs/README.md](docs/README.md): indeks dokumentasi per fase SDLC
- [docs/01-analisis/inventaris_formula.md](docs/01-analisis/inventaris_formula.md): inventaris 41 rumus IKU di Buku
- [docs/02-desain/panduan_chunking.md](docs/02-desain/panduan_chunking.md): desain chunking v2 dan alasannya
- [docs/02-desain/skema_embedding.md](docs/02-desain/skema_embedding.md): best practice embedding & retrieval, beserta status penerapannya
- [docs/02-desain/integrasi_backend.md](docs/02-desain/integrasi_backend.md): **untuk tim Backend**: arsitektur, kontrak API, dan daftar tugas integrasi ke dasbor Monev IKU
- [docs/03-evaluasi/laporan_evaluasi_akhir.md](docs/03-evaluasi/laporan_evaluasi_akhir.md): laporan evaluasi akhir chatbot (metrik, hasil per soal, kendala, langkah berikutnya). Versi Word/PDF ada di folder yang sama
- [data/README.md](data/README.md): penjelasan setiap folder data
