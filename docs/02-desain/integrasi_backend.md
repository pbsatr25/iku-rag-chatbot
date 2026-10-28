# Integrasi Chatbot RAG ke Backend Dasbor Monev IKU

Dokumen ini untuk **tim Backend** (dan AI Ops) yang akan menyambungkan chatbot RAG di repo ini ke dasbor Monev IKU (Next.js). Isinya: apa yang sudah ada, arsitektur yang diusulkan, kontrak API, daftar tugas BE, dan batasan yang perlu diketahui sebelum deployment.

Acuan kebutuhan: [PRD Asisten IKU — Chatbot RAG per Halaman Dasbor](../../PRD%20Asisten%20IKU%20—%20Chatbot%20RAG%20per%20Halaman%20Dasbor.md). Kontrak data UI: `src/types/chat.ts` di repo FE (`dikti-indicator`, branch `FE-dikti-indicator`).

> **Status singkat:** inti chatbot (retrieval, kalkulator rumus, LLM + sitasi) sudah jalan dan teruji di terminal. **Layanan API-nya belum ada.** Bagian bertanda *(usulan)* di bawah adalah rancangan yang perlu disepakati bersama sebelum dikerjakan.

## Daftar isi

1. [Apa yang sudah ada](#1-apa-yang-sudah-ada)
2. [Arsitektur yang diusulkan](#2-arsitektur-yang-diusulkan)
3. [Keputusan yang perlu disepakati](#3-keputusan-yang-perlu-disepakati)
4. [Kontrak API](#4-kontrak-api)
5. [Tugas Backend](#5-tugas-backend)
6. [Tugas AI Engineer (agar BE tahu yang akan datang)](#6-tugas-ai-engineer-agar-be-tahu-yang-akan-datang)
7. [Rumus IKU untuk TypeScript](#7-rumus-iku-untuk-typescript)
8. [Batasan & risiko](#8-batasan--risiko)
9. [Menjalankan chatbot secara lokal](#9-menjalankan-chatbot-secara-lokal)

## 1. Apa yang sudah ada

| Komponen | Status | Lokasi |
|---|---|---|
| Knowledge base Buku IKU V1 (605 chunk, bermetadata IKU & halaman) | ✅ | `data/chunks/`, `data/embeddings/` |
| Retrieval hybrid (bge-m3 + BM25), Hit@5 26/29, sitasi halaman benar 25/26 | ✅ | `src/retrieval/retriever.py` |
| Kalkulator rumus IKU deterministik (LLM tidak menghitung sendiri) | ✅ | `src/calculator/` |
| LLM + tool calling kalkulator + sitasi halaman dari metadata | ✅ (terminal) | `src/generation/answer.py` |
| Penyedia LLM bisa diganti lewat `.env` (Groq, Gemini, Ollama, OpenAI) | ✅ | `src/generation/llm_client.py` |
| Evaluasi otomatis 44 soal (definisi, hitungan, typo, format uang) | ✅ | `src/evaluation/run_answer_tests.py` |
| **Cakupan per halaman** (gerbang aturan sebelum LLM, filter retrieval `iku_id`, instruksi prompt) | ✅ (tanpa fallback semantik) | `src/generation/cakupan.py`, `tests/test_cakupan.py` |
| **Layanan HTTP** yang mengembalikan format `ChatAnswer` | ⬜ belum | – |
| Multi-turn (riwayat percakapan) | ⬜ belum, saat ini tiap pertanyaan berdiri sendiri | – |
| Streaming SSE | ⬜ tahap 2 | – |

Output chatbot saat ini (`Chatbot.ask(question)`) berupa dict Python:

```python
{
  "pertanyaan": "...",
  "jawaban": "Capaian IKU 5 adalah 25% [1].",       # teks LLM, rujukan [n] menunjuk chunk ke-n
  "sitasi": ["[1] Buku IKU ... hlm. 57"],
  "sumber_rumus": ["Buku IKU ..., IKU 5 – Formula & Keterangan, hlm. 57"],
  "kalkulator": [{"argumen": "...", "hasil": {...}}],  # hasil hitung + formula_teks + halaman
  "peringatan": ["..."],                              # temuan pemeriksa otomatis (untuk log, bukan untuk user)
  "chunks": [{"chunk_id", "content", "page_start", "page_end", "iku_id", "bagian", ...}],
}
```

Format ini **belum** sama dengan `ChatAnswer` milik FE. Pemetaannya ada di [bagian 4.3](#43-pemetaan-output-chatbot--chatanswer); adapternya dikerjakan tim AI.

## 2. Arsitektur yang diusulkan

*(usulan)* RAG tetap di **Python** sebagai layanan internal terpisah. Next.js tidak memanggil LLM langsung.

```text
Browser (panel chat FE)
   │  POST /api/chat  { question, scope, conversationId? }
   ▼
Next.js Route Handler /api/chat                         ← TUGAS BE
   - verifikasi sesi (userEmail dari cookie httpOnly)
   - validasi input & scope, batas laju (rate limit)
   - simpan log percakapan, tambah conversationId/messageId/disclaimer
   │  POST {RAG_SERVICE_URL}/v1/answer  + header X-Internal-Token
   ▼
Layanan RAG (Python, FastAPI)                            ← TUGAS AI
   - gerbang cakupan → retrieval terfilter → LLM + kalkulator → adapter ChatAnswer
   │
   ▼
Penyedia LLM (Groq / Gemini / OpenAI)   ← API key hanya ada di layanan RAG
```

Alasan tidak di-port ke TypeScript: model embedding `bge-m3`, BM25, dan kalkulator yang sudah teruji semuanya Python. Porting berarti mengulang pekerjaan dan menguji ulang dari nol.

Konsekuensi untuk BE: ada **satu proses tambahan** yang harus di-deploy (lihat [bagian 8](#8-batasan--risiko)).

## 3. Keputusan yang perlu disepakati

| # | Pertanyaan | Pilihan | Usulan AI |
|---|---|---|---|
| 1 | Di mana RAG berjalan? | (a) layanan Python terpisah, (b) port ke TypeScript | **(a)** |
| 2 | Penyimpanan vektor | (a) ChromaDB (sudah jalan, file lokal), (b) pgvector di PostgreSQL dasbor (sesuai PRD) | **(a) untuk MVP**, pindah ke (b) bila tim ingin satu database. bge-m3 = 1024 dimensi, muat di pgvector |
| 3 | Dokumen yang di-index | (a) Buku IKU V1 saja (sesuai PRD), (b) Buku + PPT | **(a)** untuk versi ini |
| 4 | Chunk IKU tanpa halaman dasbor (IKU 4, 6, 8, 10–12, LLDIKTI) | (a) tidak pernah muncul, (b) muncul di cakupan Overview | perlu keputusan PO; **sementara diterapkan (b)** di `cakupan.py` (`chunk_boleh`, `tab_untuk`) |
| 5 | Siapa menambahkan `disclaimer`, `conversationId`, `messageId` | (a) BE, (b) layanan RAG | **(a) BE**, karena BE yang menyimpan percakapan |

## 4. Kontrak API

### 4.1 FE → BE: `POST /api/chat`

Sumber kebenaran: `src/types/chat.ts` di repo FE. Ringkasan:

**Request**

```json
{
  "conversationId": "opsional",
  "question": "Hitung capaian AEE PT kami",
  "scope": { "id": "IKU 001", "kind": "iku", "ikuCode": "IKU 001" }
}
```

- `question`: wajib, maks. 2.000 karakter setelah di-trim.
- `scope`: wajib. `{ "id": "overview", "kind": "overview" }` atau `{ "id": "IKU 00x", "kind": "iku", "ikuCode": "IKU 00x" }` dengan `x` ∈ {1, 2, 3, 5, 7, 9}.
- `conversationId` harus milik `scope` yang sama; jika berbeda → `400`.

**Response 200 (`ChatAnswer`)**: `conversationId`, `messageId`, `answer`, `blocks?`, `citations`, `grounded`, `confidence?`, `action?`, `outOfScope?`, `disclaimer`. Detail per field ada di PRD bagian *Kontrak API chat*.

**Error**: selalu `{ "error": "<pesan Bahasa Indonesia>" }`.

| Status | Kapan |
|---|---|
| 400 | input tidak valid, `scope` tidak dikenal, `conversationId` beda cakupan |
| 401 | tanpa sesi |
| 429 | batas laju pengguna atau kuota LLM habis |
| 502 / 503 | layanan RAG atau penyedia LLM tidak tersedia / timeout |

### 4.2 BE → layanan RAG: `POST /v1/answer` *(usulan)*

Endpoint internal, **tidak boleh** diakses dari browser.

**Request**

```json
{
  "question": "brp capaian iku 5 klo luaran 30 dr 120 kerjasama",
  "scope": { "kind": "iku", "ikuCode": "IKU 005" },
  "history": [
    { "role": "user", "text": "..." },
    { "role": "assistant", "text": "..." }
  ]
}
```

Header: `X-Internal-Token: <RAG_SERVICE_TOKEN>`, `X-Request-Id: <uuid>` (untuk menelusuri log di dua sisi).

`history` opsional dan baru dipakai setelah fitur multi-turn selesai. Kirim maksimal beberapa giliran terakhir dari percakapan yang sama.

**Response 200**: semua field `ChatAnswer` **kecuali** `conversationId`, `messageId`, dan `disclaimer` (ditambahkan BE), ditambah blok `debug` untuk log:

```json
{
  "answer": "Capaian IKU 5 adalah 25% [1].",
  "blocks": [{ "type": "formula", "lines": ["Jumlah luaran ... ÷ Total kerja sama PT × 100%"] }],
  "citations": [{
    "id": "BUKU_0213",
    "documentTitle": "Buku IKU Diktisaintek Berdampak",
    "documentVersion": "V1",
    "section": "IKU 5 · Formula",
    "page": 57,
    "ikuCode": "IKU 005",
    "snippet": "potongan teks sumber"
  }],
  "grounded": true,
  "outOfScope": null,
  "action": null,
  "debug": {
    "model": "openai/gpt-oss-120b",
    "chunkIds": ["BUKU_0213", "BUKU_0214"],
    "warnings": [],
    "llmCalls": 2,
    "durationMs": 4200
  }
}
```

`debug` **tidak** diteruskan ke browser; simpan ke log (kebutuhan *Ketertelusuran* di PRD).

**Error dari layanan RAG** (usulan): `{ "error": "...", "code": "..." }` dengan `code` ∈ `invalid_request`, `llm_rate_limited`, `llm_unavailable`, `llm_timeout`, `internal`. BE memetakannya ke tabel status di 4.1 (mis. `llm_rate_limited` → 429, `llm_unavailable`/`llm_timeout` → 503).

### 4.3 Pemetaan output chatbot → `ChatAnswer`

Dikerjakan tim AI di layanan RAG; dicantumkan agar BE tahu asal setiap field.

| Field `ChatAnswer` | Diambil dari |
|---|---|
| `answer` | `jawaban` (rujukan `[n]` tetap ada di teks; nomornya sama dengan urutan `citations`) |
| `citations[]` | chunk yang benar-benar dirujuk `[n]` di jawaban: `chunk_id` → `id`, `page_start` → `page`, `iku_id` "5" → `ikuCode` "IKU 005", `bagian` → `section`, potongan `content` → `snippet` |
| `blocks` `formula` | `formula_teks` dari hasil kalkulator |
| `blocks` `note` | catatan tafsir rumus (`catatan`) dan catatan cacat dokumen sumber |
| `blocks` `metric` | butuh `target` dari tabel `iku_targets`, jadi baru tersedia setelah data dasbor tersambung (tahap 2) |
| `grounded` | `false` bila chatbot menyatakan informasi tidak ditemukan atau tidak ada konteks yang relevan |
| `outOfScope` | dari gerbang cakupan `periksa_cakupan()` (`src/generation/cakupan.py`): `{ suggestedTab }`, dijawab tanpa memanggil LLM |
| `debug.warnings` | `peringatan` (tidak ditampilkan ke user) |

## 5. Tugas Backend

Urutan disarankan; nomor 1–4 dibutuhkan agar FE bisa mematikan mock (`NEXT_PUBLIC_CHAT_MOCK=false`).

1. **Sesi server** dengan cookie `httpOnly`, agar `userEmail` tepercaya. Saat ini sesi masih di `localStorage` (`AUTH NOT READY` di FE). Tanpa ini, `/api/chat` hanya boleh menjawab dari dokumen, tidak boleh membaca data dasbor pengguna.
2. **Route Handler `POST /api/chat`** (`runtime = "nodejs"`):
   - validasi `question` dan `scope` (lihat 4.1), tolak dengan pesan Bahasa Indonesia;
   - panggil layanan RAG dengan **timeout** (usulan 45 detik) dan teruskan `AbortSignal`: bila user menekan *Hentikan* atau menutup panel, batalkan request ke RAG;
   - tambahkan `conversationId` (buat baru bila kosong), `messageId`, dan `disclaimer` tetap: `"Dibuat AI dari Buku IKU V1 & data modul. Periksa sebelum pelaporan."`;
   - petakan error RAG ke status HTTP (4.2).
3. **Batas laju**, dua lapis:
   - per pengguna (usulan PRD: 20 pertanyaan/menit);
   - **global untuk seluruh aplikasi**, karena kuota LLM free tier dibagi semua pengguna (lihat [bagian 8](#8-batasan--risiko)). Saat kuota habis, kembalikan 429 dengan pesan yang jelas.
4. **Tabel log percakapan** (Prisma), sesuai kebutuhan skema di dokumen API FE:
   - `ChatConversation`: `id`, `userId`, `scopeId`, `createdAt`
   - `ChatMessage`: `id`, `conversationId`, `role`, `text`, `blocks` (Json), `grounded`, `createdAt`, plus `debug` (Json: model, chunkIds, warnings, durationMs)
   - `MessageCitation`: `messageId`, `chunkId`, `documentVersion`, urutan
5. **Env & rahasia**: `RAG_SERVICE_URL`, `RAG_SERVICE_TOKEN` hanya di server (tanpa prefix `NEXT_PUBLIC_`). Key LLM **tidak** perlu ada di Next.js; cukup di layanan RAG.
6. **Deployment layanan RAG** bersama AI Ops (kebutuhan sumber daya di [bagian 8](#8-batasan--risiko)).
7. *(tahap 2)* Snapshot data dasbor (`iku_data_snapshots`) atau `pageFacts` dari FE untuk pertanyaan kuantitatif, dan streaming SSE.

## 6. Tugas AI Engineer (agar BE tahu yang akan datang)

| Pekerjaan | Hasil untuk BE |
|---|---|
| Normalisasi metadata chunk `iku_id` → `ikuCode` (`"IKU 001"`) dan penanda chunk umum | filter cakupan bisa dipakai |
| Retrieval wajib difilter per `scope` | jawaban tidak bocor ke IKU lain |
| Gerbang di luar cakupan (kode IKU lain, topik khas IKU lain) | `outOfScope.suggestedTab` terisi, tanpa memanggil LLM |
| Layanan FastAPI `POST /v1/answer` + adapter `ChatAnswer` | endpoint yang bisa dipanggil `/api/chat` |
| Contoh request/response nyata + skrip uji kontrak | BE bisa menguji integrasi tanpa menunggu LLM |
| Evaluasi per cakupan (7 halaman) bersama QA | angka kriteria penerimaan PRD |

Sampai layanan RAG siap, BE bisa mulai dari nomor 1, 3, dan 4 di [bagian 5](#5-tugas-backend), lalu membuat `/api/chat` yang memanggil **stub** dengan respons contoh di 4.2.

## 7. Rumus IKU untuk TypeScript

Bila dasbor atau BE perlu menghitung rumus IKU yang sama dengan chatbot, **jangan menyalin angka bobot secara manual**. Gunakan dua file ini:

| File | Isi |
|---|---|
| [`src/calculator/spec/buku_iku_v1.json`](../../src/calculator/spec/buku_iku_v1.json) | sumber kebenaran: konstanta (AEE ideal, bobot IKU 2/3/6, pos pendapatan IKU 9, ...) dan metadata tiap rumus (`ikuCode`, `pola`, `formula_teks`, halaman, `status`) |
| [`data/evaluation/test_inputs_hitung.json`](../../data/evaluation/test_inputs_hitung.json) | kasus uji bersama: input → hasil yang diharapkan. Implementasi TypeScript dianggap benar bila lolos semua kasus ini |

Rumus berpola `rasio` cukup satu fungsi untuk semua entri:

```ts
import spec from "./buku_iku_v1.json";

export function rasio(id: string, pembilang: number, penyebut: number) {
  const rumus = spec.rumus.find((r) => r.id === id && r.pola === "rasio");
  if (!rumus) throw new Error(`Kode rasio '${id}' tidak dikenal`);
  if (pembilang < 0) throw new Error("Pembilang tidak boleh negatif");
  if (penyebut <= 0) throw new Error("Penyebut harus lebih dari 0");
  return { hasil: Math.round((pembilang / penyebut) * 100 * 100) / 100, satuan: "%", rumus };
}
```

Entri ber-`status` `ada_tafsir` punya `catatan` tentang keputusan tafsir dokumen yang ambigu; tampilkan catatan itu bila rumusnya dipakai.

## 8. Batasan & risiko

| Hal | Dampak ke BE | Mitigasi |
|---|---|---|
| **Kuota LLM free tier sangat kecil.** Groq `gpt-oss-120b`: 8.000 token/menit untuk seluruh akun; satu soal hitungan ±8.000–10.000 token (perkiraan, 2 panggilan LLM). Gemini free: ±20 request/hari per model dan sering 503 saat ramai | Free tier hanya cukup untuk **demo satu pengguna**, bukan dipakai bersamaan | batas laju global; pesan 429 yang jelas; layanan berbayar untuk produksi (sedang diajukan di RAB) |
| **Privasi**: data yang dikirim ke free tier dapat dipakai penyedia | jangan kirim data internal kampus (isi spreadsheet, nama, NIM) selama memakai free tier | hanya teks pertanyaan + potongan Buku IKU yang dikirim; data dasbor menunggu layanan berbayar |
| **Latensi**: satu panggilan Groq ±3 detik; soal hitungan butuh 2–4 panggilan. End-to-end belum diukur | NFR PRD (token pertama ≤ 5 detik) belum terjamin tanpa streaming | timeout di BE; streaming SSE di tahap 2 |
| **Layanan RAG butuh proses yang selalu hidup**: model `bge-m3` dimuat ke memori (±1,5 GB RAM terpantau saat berjalan) dan butuh waktu untuk dimuat | **tidak cocok** di-deploy sebagai fungsi serverless | container/VM dengan proses tetap; GPU tidak wajib |
| Sesi masih di `localStorage` | siapa pun bisa mengaku sebagai email lain | tugas BE nomor 1 sebelum fitur data dasbor dibuka |
| Rumus LLDIKTI IKU 8 (hlm. 91) janggal di dokumen sumber | angka bisa dipertanyakan | ditandai, menunggu konfirmasi PO |

## 9. Menjalankan chatbot secara lokal

Untuk mencoba perilaku chatbot sebelum layanan API ada:

1. Ikuti [Setup di README](../../README.md#setup-langkah-demi-langkah) (Python 3.13, venv, dependency, vector DB).
2. Isi `.env` sesuai [`.env.example`](../../.env.example) (cukup blok Groq untuk testing).
3. Jalankan:

```powershell
$env:HF_HUB_OFFLINE="1"
python src/generation/chat_cli.py --detail
```

`--detail` menampilkan argumen kalkulator dan chunk yang dipakai, berguna untuk memahami asal setiap field di 4.3.

Pertanyaan atau usulan perubahan kontrak: buat issue di repo ini (template *Usulan fitur / eksperimen*), atau ubah `src/types/chat.ts` di repo FE lebih dulu sesuai aturan PRD, lalu kabari tim AI.
