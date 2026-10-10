# Laporan Evaluasi Retrieval

- Waktu: 2026-10-11 01:59:56
- Test set: `data\evaluation\test_set_buku_iku.md` (44 soal, 43 dalam cakupan, 1 di luar cakupan)
- Model embedding: `BAAI/bge-m3` | Koleksi: `pmpt_qa_v2` (605 chunk)
- top_k: 5 | ambang di luar cakupan: distance ≥ 0.45
- Retriever: `{'candidates': 30, 'hybrid': True, 'iku_boost': True, 'dedupe': True, 'rerank': False, 'min_chars': 0, 'sambung_tabel': True}`
- Sitasi Buku yang berasal dari Lampiran: 0

Definisi: sebuah soal **HIT** jika ada chunk yang memuat semua *kata kunci bukti* soal tersebut di 5 hasil teratas `Retriever.search()`.

## Ringkasan

| Metrik | Nilai |
|---|---|
| Hit@1 | 30/43 (69.8%) |
| Hit@3 | 39/43 (90.7%) |
| Hit@5 | 41/43 (95.3%) |
| MRR@5 | 0.806 |
| Hit@5 gabungan (semua kata kunci ada di gabungan top-5) | 42/43 (97.7%) |
| Halaman sitasi benar (chunk bukti dari Buku) | 40/41 (97.6%) |
| Hasil #1 berasal dari PPT (bukan Buku) | 1/43 |
| Chunk bukti pertama berasal dari PPT | 0 soal |
| Bukti tidak ada di corpus (masalah chunking) | 1 ['D04'] |
| Nyaris kena (bukti di top-20 tapi tidak di top-5) | 1 ['H05'] |
| Soal di luar cakupan lolos | 0/1 |
| Rata-rata distance #1 (soal HIT / MISS) | 0.3742 / 0.311 |
| Distance #1 tertinggi soal dalam cakupan | 0.5783 |
| Distance #1 soal di luar cakupan | {'D12': 0.3988} |
| Rata-rata waktu per query | 0.058 s |

### Per tipe soal

| Tipe | n | Hit@1 | Hit@3 | Hit@5 | MRR |
|---|---|---|---|---|---|
| Definisi | 12 | 75.0% | 91.7% | 100.0% | 0.84 |
| Jebakan ⚠️ | 1 | 0.0% | 0.0% | 0.0% | 0.0 |
| Hitung | 30 | 70.0% | 93.3% | 96.7% | 0.819 |

### Per IKU

| IKU | n | Hit@1 | Hit@5 | MRR |
|---|---|---|---|---|
| 1 | 9 | 6/9 | 8/9 | 0.759 |
| 11b | 1 | 1/1 | 1/1 | 1.0 |
| 11c | 1 | 0/1 | 1/1 | 0.5 |
| 11d | 1 | 1/1 | 1/1 | 1.0 |
| 12 | 3 | 3/3 | 3/3 | 1.0 |
| 2 | 6 | 2/6 | 5/6 | 0.583 |
| 3 | 3 | 3/3 | 3/3 | 1.0 |
| 4 | 2 | 2/2 | 2/2 | 1.0 |
| 5 | 2 | 1/2 | 2/2 | 0.75 |
| 6 | 3 | 3/3 | 3/3 | 1.0 |
| 7 | 3 | 2/3 | 3/3 | 0.75 |
| 8 | 1 | 0/1 | 1/1 | 0.333 |
| 9 | 6 | 4/6 | 6/6 | 0.792 |
| Umum | 2 | 2/2 | 2/2 | 1.0 |

## Hasil per soal

| ID | IKU | Status | Sumber bukti | Hlm. bukti (Buku) | Hlm. benar | Rank mentah | Distance #1 | Sumber #1 |
|---|---|---|---|---|---|---|---|---|
| D01 | 1 | HIT @1 | Buku | 49 ✅ | 49 | 1 | 0.3565 | Buku |
| D02 | 1 | HIT @1 | Buku | 49 ✅ | 49 | 1 | 0.3376 | Buku |
| D03 | Umum | HIT @1 | Buku | 48–49 ✅ | 48 | 1 | 0.3311 | Buku |
| D04 | Umum | HIT @1 | Buku | 48–49 ✅ | 48 | - | 0.3565 | Buku |
| D05 | 2 | HIT @1 | Buku | 51 ✅ | 51, 52 | 1 | 0.4091 | Buku |
| D06 | 3 | HIT @1 | Buku | 53 ✅ | 53 | 1 | 0.2737 | Buku |
| D07 | 7 | HIT @1 | Buku | 58 ✅ | 58 | 1 | 0.2403 | Buku |
| D08 | 9 | HIT @1 | Buku | 59 ✅ | 59 | 1 | 0.3045 | Buku |
| D09 | 6 | HIT @1 | Buku | 63 ✅ | 63 | 2 | 0.4332 | Buku |
| D10 | 11c | HIT @2 | Buku | 67 ✅ | 67 | 3 | 0.2792 | Buku |
| D11 | 1 | MISS - bukti tidak masuk top-20 | - | - | 49, 51 | - | 0.3585 | Buku |
| D12 | — | GAGAL (di luar cakupan) | - | - | - | - | 0.3988 | Buku |
| H01 | 1 | HIT @1 | Buku | 49–50 ✅ | 49 | 2 | 0.4089 | Buku |
| H02 | 1 | HIT @1 | Buku | 49–50 ✅ | 49, 50 | 1 | 0.3536 | Buku |
| H03 | 1 | HIT @1 | Buku | 49 ✅ | 49 | 1 | 0.3883 | Buku |
| H04 | 2 | HIT @1 | Buku | 51 ✅ | 51, 52 | 1 | 0.3037 | Buku |
| H05 | 2 | MISS - bukti di rank mentah 2 | - | - | 51, 52 | 2 | 0.2634 | Buku |
| H06 | 2 | HIT @2 | Buku | 52 ✅ | 52 | 1 | 0.3801 | Buku |
| H07 | 3 | HIT @1 | Buku | 53–54 ✅ | 53, 54 | 1 | 0.3276 | Buku |
| H08 | 3 | HIT @1 | Buku | 53–54 ✅ | 54 | 1 | 0.3073 | Buku |
| H09 | 5 | HIT @2 | Buku | 57–58 ✅ | 57 | 2 | 0.308 | Buku |
| H10 | 6 | HIT @1 | Buku | 63 ✅ | 63 | 7 | 0.3271 | Buku |
| H11 | 6 | HIT @1 | Buku | 63 ✅ | 63 | 3 | 0.3226 | Buku |
| H12 | 7 | HIT @1 | Buku | 58 ✅ | 58 | 1 | 0.2928 | Buku |
| H13 | 9 | HIT @1 | Buku | 59 ✅ | 59 | 1 | 0.3208 | Buku |
| H14 | 4 | HIT @1 | Buku | 62–63 ✅ | 62 | 1 | 0.267 | Buku |
| H15 | 8 | HIT @3 | Buku | 64 ✅ | 64 | 6 | 0.2335 | Buku |
| H16 | 11b | HIT @1 | Buku | 87 ❌ | 66 | 1 | 0.433 | Buku |
| H17 | 11d | HIT @1 | Buku | 68 ✅ | 68 | 1 | 0.3472 | Buku |
| H18 | 12 | HIT @1 | Buku | 60 ✅ | 60 | 2 | 0.3951 | Buku |
| D13 | 1 | HIT @3 | Buku | 49 ✅ | 49 | 1 | 0.4306 | Buku |
| D14 | 9 | HIT @4 | Buku | 59 ✅ | 59 | 5 | 0.4138 | Buku |
| H19 | 1 | HIT @2 | Buku | 49–50 ✅ | 49 | 3 | 0.5783 | Buku |
| H20 | 1 | HIT @1 | Buku | 49–50 ✅ | 49, 50 | 1 | 0.4435 | Buku |
| H21 | 2 | HIT @2 | Buku | 52 ✅ | 52 | 19 | 0.5289 | Buku |
| H22 | 2 | HIT @2 | Buku | 52 ✅ | 52 | 4 | 0.4377 | Buku |
| H23 | 5 | HIT @1 | Buku | 57–58 ✅ | 57 | 1 | 0.389 | Buku |
| H24 | 7 | HIT @4 | Buku | 58 ✅ | 58 | 6 | 0.479 | Buku |
| H25 | 9 | HIT @2 | Buku | 59 ✅ | 59 | 18 | 0.4665 | PPT |
| H26 | 9 | HIT @1 | Buku | 59 ✅ | 59 | 1 | 0.4424 | Buku |
| H27 | 9 | HIT @1 | Buku | 59 ✅ | 59 | 7 | 0.4379 | Buku |
| H28 | 12 | HIT @1 | Buku | 60 ✅ | 60 | 10 | 0.4592 | Buku |
| H29 | 12 | HIT @1 | Buku | 60 ✅ | 60 | 2 | 0.4553 | Buku |
| H30 | 4 | HIT @1 | Buku | 62–63 ✅ | 62 | 1 | 0.3431 | Buku |

## Detail per soal

<details><summary>✅ <b>D01</b> — HIT @1 — Apa itu IKU 1?</summary>

**Pertanyaan:** Apa itu IKU 1?

**Kata kunci bukti:** `tepat waktu`, `masa studi standar`

**Halaman benar:** 49 | **Chunk bukti di corpus:** 3 (Buku hlm.49, Buku hlm.100, PPT hlm.45)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 49 | 0.3565 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 |  | Buku | 49–50 | 0.3949 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 49–50 | 0.405 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 49 | 0.3858 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 49 | 0.3727 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |

</details>

<details><summary>✅ <b>D02</b> — HIT @1 — Berapa masa tempuh kurikulum dan AEE ideal untuk program Sarjana dan Diploma Tiga?</summary>

**Pertanyaan:** Berapa masa tempuh kurikulum dan AEE ideal untuk program Sarjana dan Diploma Tiga?

**Kata kunci bukti:** `aee ideal`, `8 semester`, `25%`

**Halaman benar:** 49 | **Chunk bukti di corpus:** 3 (Buku hlm.49, Buku hlm.100–101, PPT hlm.45)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 49 | 0.3376 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 |  | Buku | 49 | 0.4676 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 49–50 | 0.4265 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 49–50 | 0.4837 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 51 | 0.5127 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>✅ <b>D03</b> — HIT @1 — Berapa jumlah IKU wajib, IKU pilihan, dan IKU partisipatif?</summary>

**Pertanyaan:** Berapa jumlah IKU wajib, IKU pilihan, dan IKU partisipatif?

**Kata kunci bukti:** `sebanyak 7 (tujuh)`, `partisipatif`

**Halaman benar:** 48 | **Chunk bukti di corpus:** 1 (Buku hlm.48–49)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 48–49 | 0.3311 | …BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak / hlm. 48] / No / Sasaran / Indikator Kinerja Utama /  |
| 2 |  | Buku | 69 | 0.3509 | …isaintek Berdampak > 5.3.3. Indikator Kinerja Utama (IKU) Partisipatif | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.3. Indikator Kinerja Utama (IKU) Partisipatif /  |
| 3 |  | Buku | 61 | 0.3453 | … Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan / hlm.  |
| 4 |  | Buku | 58 | 0.3561 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 5 |  | Buku | 58 | 0.405 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |

</details>

<details><summary>✅ <b>D04</b> — HIT @1 — Sebutkan IKU yang bersifat wajib.</summary>

**Pertanyaan:** Sebutkan IKU yang bersifat wajib.

**Kata kunci bukti:** `angka efisiensi edukasi`, `kesejahteraan dosen`, `pendapatan non pendidikan`

**Halaman benar:** 48 | **Chunk bukti di corpus:** 0 

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 48–49 | 0.3565 | …BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak / hlm. 48] / No / Sasaran / Indikator Kinerja Utama /  |
| 2 |  | Buku | 49 | 0.3476 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 53 | 0.3538 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 4 |  | Buku | 55 | 0.3756 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 5 |  | Buku | 58 | 0.3895 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |

</details>

<details><summary>✅ <b>D05</b> — HIT @1 — Dari mana data IKU 2 diperoleh, dan bagaimana menentukan jumlah responden minimum?</summary>

**Pertanyaan:** Dari mana data IKU 2 diperoleh, dan bagaimana menentukan jumlah responden minimum?

**Kata kunci bukti:** `tracer study`, `slovin`

**Halaman benar:** 51, 52 | **Chunk bukti di corpus:** 3 (Buku hlm.51, Buku hlm.104, PPT hlm.48)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 51 | 0.4091 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 2 |  | Buku | 52 | 0.4173 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 3 |  | Buku | 51 | 0.4552 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 4 |  | Buku | 51 | 0.4577 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 5 |  | Buku | 51 | 0.4591 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>✅ <b>D06</b> — HIT @1 — Kegiatan di luar program studi apa saja yang diakui untuk IKU 3?</summary>

**Pertanyaan:** Kegiatan di luar program studi apa saja yang diakui untuk IKU 3?

**Kata kunci bukti:** `magang`, `pertukaran mahasiswa`, `dosen pembimbing`

**Halaman benar:** 53 | **Chunk bukti di corpus:** 5 (Buku hlm.53, Buku hlm.53, Buku hlm.105–106, Buku hlm.106–107, PPT hlm.49)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 53 | 0.2737 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 2 | ✅ | Buku | 53 | 0.2754 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 3 |  | Buku | 53 | 0.314 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 4 |  | Buku | 53–54 | 0.3557 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 5 |  | Buku | 61–62 | 0.4246 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |

</details>

<details><summary>✅ <b>D07</b> — HIT @1 — SDG apa saja yang wajib dan pilihan dalam IKU 7?</summary>

**Pertanyaan:** SDG apa saja yang wajib dan pilihan dalam IKU 7?

**Kata kunci bukti:** `sdg 17`, `2 (dua) tujuan sdgs lain`

**Halaman benar:** 58 | **Chunk bukti di corpus:** 3 (Buku hlm.58, Buku hlm.120–121, PPT hlm.55)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 58 | 0.2403 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 2 |  | Buku | 58 | 0.2886 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 3 |  | Buku | 58 | 0.3026 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 4 |  | Buku | 58 | 0.2726 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 5 |  | Buku | 58 | 0.3032 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |

</details>

<details><summary>✅ <b>D08</b> — HIT @1 — Pendapatan apa saja yang tidak termasuk dalam perhitungan IKU 9?</summary>

**Pertanyaan:** Pendapatan apa saja yang tidak termasuk dalam perhitungan IKU 9?

**Kata kunci bukti:** `boptn`, `iuran pengembangan institusi`

**Halaman benar:** 59 | **Chunk bukti di corpus:** 3 (Buku hlm.59, Buku hlm.122–123, PPT hlm.56)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 59 | 0.3045 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 2 |  | Buku | 59 | 0.3208 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 3 |  | Buku | 59 | 0.3296 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 4 |  | Buku | 59 | 0.339 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 5 |  | Buku | 79 | 0.3628 | …an/UKT > 1. Persentase Pendapatan terhadap Total Aset Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.5. Sub Indikator (IKU 9): Persentase Pendapatan Non Pendidikan/UKT  |

</details>

<details><summary>✅ <b>D09</b> — HIT @1 — Penerbit apa yang tidak diperhitungkan dalam IKU 6?</summary>

**Pertanyaan:** Penerbit apa yang tidak diperhitungkan dalam IKU 6?

**Kata kunci bukti:** `mdpi`, `hindawi`

**Halaman benar:** 63 | **Chunk bukti di corpus:** 9 (Buku hlm.63, Buku hlm.73, Buku hlm.74, Buku hlm.75, Buku hlm.118–119, PPT hlm.61–62)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 63 | 0.4332 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 2 |  | Buku | 63 | 0.441 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 3 |  | Buku | 63 | 0.4589 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 4 |  | Buku | 63 | 0.4319 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 5 |  | Buku | 62 | 0.4709 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |

</details>

<details><summary>✅ <b>D10</b> — HIT @2 — Bagaimana arah penilaian IKU 11c (pelanggaran integritas akademik)?</summary>

**Pertanyaan:** Bagaimana arah penilaian IKU 11c (pelanggaran integritas akademik)?

**Kata kunci bukti:** `semakin rendah semakin baik`

**Halaman benar:** 67 | **Chunk bukti di corpus:** 3 (Buku hlm.67, Buku hlm.126–130, PPT hlm.67)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 67 | 0.2792 | … IKU 11: (c) Pencegahan dan Penanganan Pelanggaran Integritas Akademik | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 2 | ✅ | Buku | 67 | 0.2892 | … IKU 11: (c) Pencegahan dan Penanganan Pelanggaran Integritas Akademik | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 3 |  | Buku | 67 | 0.288 | … IKU 11: (c) Pencegahan dan Penanganan Pelanggaran Integritas Akademik | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 4 |  | Buku | 67 | 0.3294 | … IKU 11: (c) Pencegahan dan Penanganan Pelanggaran Integritas Akademik | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 5 | ✅ | PPT | 67 | 0.3376 | …K/WBBM > IKU 11.1 : Hasil audit atas Laporan Keuangan Perguruan Tinggi | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - V > 5.3. INDIKATOR KINERJA UTAMA (IKU) DIKTISAINTEK BERDAMPAK > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > 4  |

</details>

<details><summary>❌ <b>D11</b> — MISS - bukti tidak masuk top-20 — Lulusan 400, yang bekerja 280, berapa capaian IKU 1?</summary>

**Pertanyaan:** Lulusan 400, yang bekerja 280, berapa capaian IKU 1?

**Kata kunci bukti:** `tepat waktu`, `masa studi standar`

**Halaman benar:** 49, 51 | **Chunk bukti di corpus:** 3 (Buku hlm.49, Buku hlm.100, PPT hlm.45)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 49–50 | 0.3585 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 |  | Buku | 49–50 | 0.3813 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 49 | 0.3449 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 49 | 0.3712 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 51 | 0.3666 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>❌ <b>D12</b> — GAGAL (di luar cakupan) — Berapa besaran UKT di Universitas Gadjah Mada tahun 2026?</summary>

**Pertanyaan:** Berapa besaran UKT di Universitas Gadjah Mada tahun 2026?

**Kata kunci bukti:** — (di luar cakupan)

**Halaman benar:** - | **Chunk bukti di corpus:** 0 

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 41 | 0.3988 | …BAB - IV > 4.8. QS WORLD UNIVERSIY RANKING | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.8. QS WORLD UNIVERSIY RANKING / hlm. 41] / / QS World University Ranking: Ranked Indonesian Universities / /  |
| 2 |  | PPT | 28 | 0.3783 | …3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada / hlm. 28] / Tahun 2025 / Target IK |
| 3 |  | Buku | 43 | 0.3939 | …BAB - IV > 4.10. DANA ABADI > Latar Belakang | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.10. DANA ABADI > Latar Belakang / hlm. 43] **Dana Abadi Top 7 PTN-BH 2024** (Dalam Miliar Rp) / PERGURUAN TIN |
| 4 |  | Buku | 36 | 0.4134 | …BAB - IV > 4.5. PUBLIKASI > Tabel Publikasi Top 5 PT Indonesia | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.5. PUBLIKASI > Tabel Publikasi Top 5 PT Indonesia / hlm. 36] / Nama Universitas / Baseline Publikasi PTN 2024 |
| 5 |  | Buku | 33 | 0.3902 | …BAB - IV > 4.3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 / hlm. 33] Sebagai ilustrasi implementasi kebijakan peningkatan  |

</details>

<details><summary>✅ <b>H01</b> — HIT @1 — Prodi S1 memiliki 200 mahasiswa dalam satu tahun akademik. Sebanyak 40 mahasiswa lulus tep</summary>

**Pertanyaan:** Prodi S1 memiliki 200 mahasiswa dalam satu tahun akademik. Sebanyak 40 mahasiswa lulus tepat 8 semester. Berapa AEE realisasi dan tingkat pencapaian AEE prodi tersebut?

**Kata kunci bukti:** `aee ideal`, `tingkat pencapaian aee`

**Halaman benar:** 49 | **Chunk bukti di corpus:** 5 (Buku hlm.49–50, Buku hlm.49–50, Buku hlm.101–102, Buku hlm.101–102, PPT hlm.46)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 49–50 | 0.4089 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 | ✅ | Buku | 49–50 | 0.4701 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 49 | 0.4029 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 49 | 0.4882 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 33 | 0.4677 | …3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada / hlm. 33] / Tahun 2025 / Target IKU U |

</details>

<details><summary>✅ <b>H02</b> — HIT @1 — Sebuah PT memiliki 3 program pendidikan: D3 dengan AEE realisasi 30%, S1 dengan 22,5%, dan</summary>

**Pertanyaan:** Sebuah PT memiliki 3 program pendidikan: D3 dengan AEE realisasi 30%, S1 dengan 22,5%, dan S2 dengan 40%. Berapa AEE PT?

**Kata kunci bukti:** `aee pt`, `tingkat pencapaian`

**Halaman benar:** 49, 50 | **Chunk bukti di corpus:** 7 (Buku hlm.49–50, Buku hlm.49–50, Buku hlm.100, Buku hlm.101–102, Buku hlm.101–102, PPT hlm.46)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 49–50 | 0.3536 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 | ✅ | Buku | 49–50 | 0.3623 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 49 | 0.4934 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 25 | 0.3505 | …EMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK PERGURUAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 / BAB - III > 3.7. KETERKAITAN IKU DIKTISAINTEK BERDAMPAK DENGAN IKU KEMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK  |
| 5 |  | Buku | 25 | 0.3495 | …EMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK PERGURUAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 / BAB - III > 3.7. KETERKAITAN IKU DIKTISAINTEK BERDAMPAK DENGAN IKU KEMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK  |

</details>

<details><summary>✅ <b>H03</b> — HIT @1 — Prodi S1 mencatat 250 mahasiswa pada satu tahun akademik, termasuk 10 mahasiswa pindah dan</summary>

**Pertanyaan:** Prodi S1 mencatat 250 mahasiswa pada satu tahun akademik, termasuk 10 mahasiswa pindah dan 15 mahasiswa *drop out*. Sebanyak 45 mahasiswa lulus tepat 8 semester. Berapa AEE realisasi dan tingkat pencapaiannya?

**Kata kunci bukti:** `drop out`, `mahasiswa pindah`

**Halaman benar:** 49 | **Chunk bukti di corpus:** 3 (Buku hlm.49, Buku hlm.100–101, PPT hlm.45)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 49 | 0.3883 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 |  | Buku | 49–50 | 0.3915 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 49–50 | 0.4607 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | PPT | 28 | 0.4261 | …3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada / hlm. 28] / Tahun 2025 / Target IK |
| 5 |  | Buku | 33 | 0.4364 | …3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.3. PROYEKSI PERTUMBUHAN MAHASISWA ASING 2030 > Universitas Gadjah Mada / hlm. 33] / Tahun 2025 / Target IKU U |

</details>

<details><summary>✅ <b>H04</b> — HIT @1 — Tracer study mengumpulkan 400 responden lulusan S1. Sebanyak 280 lulusan bekerja dengan ma</summary>

**Pertanyaan:** Tracer study mengumpulkan 400 responden lulusan S1. Sebanyak 280 lulusan bekerja dengan masa tunggu < 6 bulan dan gaji > 1,2× UMP; sisanya belum bekerja. Berapa capaian IKU 2?

**Kata kunci bukti:** `masa tunggu`, `1.2x ump`

**Halaman benar:** 51, 52 | **Chunk bukti di corpus:** 9 (Buku hlm.51, Buku hlm.103–104, Buku hlm.103–104, PPT hlm.47, PPT hlm.47, PPT hlm.47)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 51 | 0.3037 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 2 |  | Buku | 51 | 0.3379 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 3 |  | Buku | 51 | 0.3445 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 4 |  | Buku | 51 | 0.3336 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 5 |  | Buku | 52 | 0.3471 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>❌ <b>H05</b> — MISS - bukti di rank mentah 2 — Tracer study mengumpulkan 500 responden lulusan. Rinciannya: - 200 bekerja, masa tunggu < </summary>

**Pertanyaan:** Tracer study mengumpulkan 500 responden lulusan. Rinciannya: - 200 bekerja, masa tunggu < 6 bulan, gaji > 1,2× UMP - 100 bekerja, masa tunggu < 1 tahun, gaji > 1,2× UMP - 50 bekerja, masa tunggu < 1 tahun, gaji < 1,2× UMP - 30 melanjutkan studi (surat penerimaan < 12 bulan) - 20 *founder*, < 6 bulan, penghasilan > 1,2× UMP - 10 *freelancer*, > 6 bulan, penghasilan < 1,2× UMP - 90 belum bekerja/studi/wirausaha Berapa capaian IKU 2?

**Kata kunci bukti:** `freelancer`, `bobot = 0,8`

**Halaman benar:** 51, 52 | **Chunk bukti di corpus:** 2 (PPT hlm.47, PPT hlm.47)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 51 | 0.2634 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 2 |  | Buku | 51 | 0.3056 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 3 |  | Buku | 51 | 0.3091 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 4 |  | Buku | 51 | 0.3158 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 5 |  | Buku | 52 | 0.3289 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>✅ <b>H06</b> — HIT @2 — Jumlah lulusan suatu PT adalah 2.000 orang. Berapa jumlah responden minimum tracer study u</summary>

**Pertanyaan:** Jumlah lulusan suatu PT adalah 2.000 orang. Berapa jumlah responden minimum tracer study untuk IKU 2?

**Kata kunci bukti:** `responden minimum`, `galat`

**Halaman benar:** 52 | **Chunk bukti di corpus:** 3 (Buku hlm.52, Buku hlm.104–105, PPT hlm.48–49)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 51 | 0.3801 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 2 | ✅ | Buku | 52 | 0.384 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 3 |  | Buku | 51 | 0.4108 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 4 |  | Buku | 51 | 0.4117 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 5 |  | Buku | 51 | 0.4033 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>✅ <b>H07</b> — HIT @1 — Sebuah PT memiliki 1.000 mahasiswa S1/Diploma. Rinciannya: - 100 mahasiswa magang 20 SKS -</summary>

**Pertanyaan:** Sebuah PT memiliki 1.000 mahasiswa S1/Diploma. Rinciannya: - 100 mahasiswa magang 20 SKS - 150 mahasiswa pertukaran 8 SKS - 50 mahasiswa riset 4 SKS - 5 mahasiswa juara 1 lomba nasional - 10 mahasiswa finalis lomba internasional Berapa capaian IKU 3?

**Kata kunci bukti:** `5 sks, bobot = 0,4`, `finalis, bobot = 0,2`

**Halaman benar:** 53, 54 | **Chunk bukti di corpus:** 3 (Buku hlm.53–54, Buku hlm.107–108, PPT hlm.50)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 53–54 | 0.3276 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 2 |  | Buku | 53 | 0.3311 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 3 |  | Buku | 53 | 0.3301 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 4 |  | Buku | 53 | 0.3679 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 5 |  | Buku | 49 | 0.3528 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |

</details>

<details><summary>✅ <b>H08</b> — HIT @1 — Dari 500 mahasiswa, prestasi yang tercatat adalah 2 juara 1 internasional, 4 juara 2 tingk</summary>

**Pertanyaan:** Dari 500 mahasiswa, prestasi yang tercatat adalah 2 juara 1 internasional, 4 juara 2 tingkat provinsi, dan 20 finalis tingkat provinsi. Tidak ada kegiatan SKS di luar prodi. Berapa capaian IKU 3?

**Kata kunci bukti:** `juara harapan`, `finalis, bobot = 0,05`

**Halaman benar:** 54 | **Chunk bukti di corpus:** 3 (Buku hlm.53–54, Buku hlm.107–108, PPT hlm.50)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 53–54 | 0.3073 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 2 |  | Buku | 53 | 0.3358 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 3 |  | Buku | 53 | 0.3403 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 4 |  | Buku | 53 | 0.3499 | …a S1 dan D4/D3/D2/D1 Berkegiatan/Meraih Prestasi di Luar Program Studi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 3 IKU 3 |
| 5 |  | Buku | 25 | 0.3739 | …EMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK PERGURUAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 / BAB - III > 3.7. KETERKAITAN IKU DIKTISAINTEK BERDAMPAK DENGAN IKU KEMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK  |

</details>

<details><summary>✅ <b>H09</b> — HIT @2 — PT memiliki 120 kerja sama. Dari kerja sama itu dihasilkan 30 karya (judul) yang telah dim</summary>

**Pertanyaan:** PT memiliki 120 kerja sama. Dari kerja sama itu dihasilkan 30 karya (judul) yang telah dimanfaatkan oleh mitra, melibatkan total 90 dosen. Berapa capaian IKU 5?

**Kata kunci bukti:** `total kerjasama perguruan tinggi`, `bukan jumlah dosen`

**Halaman benar:** 57 | **Chunk bukti di corpus:** 3 (Buku hlm.57–58, Buku hlm.117, PPT hlm.53)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 56–57 | 0.308 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 2 | ✅ | Buku | 57–58 | 0.3089 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 3 |  | Buku | 55–56 | 0.3214 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 4 |  | Buku | 55–56 | 0.3102 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 5 |  | Buku | 55–56 | 0.3313 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |

</details>

<details><summary>✅ <b>H10</b> — HIT @1 — Total publikasi PT dalam satu periode adalah 200, terdiri atas 10 jurnal Top Tier, 40 Q1, </summary>

**Pertanyaan:** Total publikasi PT dalam satu periode adalah 200, terdiri atas 10 jurnal Top Tier, 40 Q1, 50 Q2, 30 Q3, 20 Q4, dan 50 publikasi tidak terindeks Scopus/WoS. Berapa capaian IKU 6?

**Kata kunci bukti:** `top tier`, `bobot 1,2`, `q4`

**Halaman benar:** 63 | **Chunk bukti di corpus:** 3 (Buku hlm.63, Buku hlm.117–118, PPT hlm.61)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 63 | 0.3271 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 2 |  | Buku | 63 | 0.3443 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 3 |  | Buku | 63 | 0.3568 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 4 |  | Buku | 63 | 0.3544 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 5 |  | Buku | 73 | 0.3249 | …reputasi Internasional (Scopus/WoS) > a. Total Publikasi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.3. Sub Indikator (IKU 6): Persentase Publikasi Bereputasi Internasi |

</details>

<details><summary>✅ <b>H11</b> — HIT @1 — Total publikasi 20, terdiri atas 4 artikel Q1 hasil kolaborasi dengan penulis luar negeri,</summary>

**Pertanyaan:** Total publikasi 20, terdiri atas 4 artikel Q1 hasil kolaborasi dengan penulis luar negeri, 6 artikel Q1 tanpa kolaborasi, dan 10 prosiding internasional terindeks Scopus. Berapa capaian IKU 6?

**Kata kunci bukti:** `kolaborasi internasional`, `prosiding internasional`

**Halaman benar:** 63 | **Chunk bukti di corpus:** 6 (Buku hlm.63, Buku hlm.63, Buku hlm.117–118, Buku hlm.118–119, PPT hlm.61, PPT hlm.61–62)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 63 | 0.3226 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 2 | ✅ | Buku | 63 | 0.3302 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 3 |  | Buku | 63 | 0.353 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 4 |  | Buku | 63 | 0.3704 | …an > IKU 6: Persentase Publikasi Bereputasi Internasional (Scopus/WoS) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 6 |
| 5 |  | Buku | 76 | 0.3096 | …al (Scopus/WoS) > d. Persentase Penelitian Berkolaborasi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.3. Sub Indikator (IKU 6): Persentase Publikasi Bereputasi Internasi |

</details>

<details><summary>✅ <b>H12</b> — HIT @1 — Dari 60 program SDGs PT, 45 program berkontribusi pada SDG 1, 4, 17, dan 2 SDG pilihan. Be</summary>

**Pertanyaan:** Dari 60 program SDGs PT, 45 program berkontribusi pada SDG 1, 4, 17, dan 2 SDG pilihan. Berapa capaian IKU 7?

**Kata kunci bukti:** `total program sdg`

**Halaman benar:** 58 | **Chunk bukti di corpus:** 3 (Buku hlm.58, Buku hlm.121, PPT hlm.55)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 58 | 0.2928 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 2 |  | Buku | 58 | 0.3109 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 3 |  | Buku | 58 | 0.3238 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 4 |  | Buku | 58 | 0.2937 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 5 |  | Buku | 58 | 0.3169 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |

</details>

<details><summary>✅ <b>H13</b> — HIT @1 — Total pendapatan PT dalam satu tahun anggaran adalah Rp500 miliar, terdiri atas: - UKT Rp3</summary>

**Pertanyaan:** Total pendapatan PT dalam satu tahun anggaran adalah Rp500 miliar, terdiri atas: - UKT Rp300 miliar - BOPTN Rp80 miliar - hibah riset kompetitif Rp50 miliar - jasa konsultasi dan pelatihan Rp40 miliar - unit bisnis (hotel, penerbitan) Rp20 miliar - hasil investasi dana abadi Rp10 miliar Berapa capaian IKU 9?

**Kata kunci bukti:** `boptn`, `dana abadi`

**Halaman benar:** 59 | **Chunk bukti di corpus:** 3 (Buku hlm.59, Buku hlm.122–123, PPT hlm.56)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 59 | 0.3208 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 2 |  | Buku | 59 | 0.3669 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 3 |  | Buku | 59 | 0.3472 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 4 |  | Buku | 59 | 0.37 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 5 |  | PPT | 11 | 0.362 | …BAB - II > 2.2. KONTRAK KINERJA PERGURUAN TINGGI > Ilustrasi: | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - II > 2.2. KONTRAK KINERJA PERGURUAN TINGGI > Ilustrasi: / hlm. 11] / Sumber Dana / Entitas / Nilai / Setara / Nil |

</details>

<details><summary>✅ <b>H14</b> — HIT @1 — PT memiliki 300 dosen dalam satu tahun terakhir; 45 dosen ber-NUPTK mendapat rekognisi int</summary>

**Pertanyaan:** PT memiliki 300 dosen dalam satu tahun terakhir; 45 dosen ber-NUPTK mendapat rekognisi internasional. Berapa capaian IKU 4?

**Kata kunci bukti:** `nuptk`, `rekognisi internasional`

**Halaman benar:** 62 | **Chunk bukti di corpus:** 3 (Buku hlm.62–63, Buku hlm.112, PPT hlm.60–61)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 62–63 | 0.267 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 2 |  | Buku | 61 | 0.3057 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 3 |  | Buku | 62 | 0.3345 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 4 |  | Buku | 61–62 | 0.3528 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 5 |  | Buku | 61–62 | 0.3704 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |

</details>

<details><summary>✅ <b>H15</b> — HIT @3 — Dari 400 SDM PT (dosen/peneliti), 12 orang terlibat langsung dalam penyusunan kebijakan na</summary>

**Pertanyaan:** Dari 400 SDM PT (dosen/peneliti), 12 orang terlibat langsung dalam penyusunan kebijakan nasional/daerah/industri, dibuktikan dengan SK atau undangan resmi. Berapa capaian IKU 8?

**Kata kunci bukti:** `penyusunan kebijakan`, `total sdm pt`

**Halaman benar:** 64 | **Chunk bukti di corpus:** 3 (Buku hlm.64, Buku hlm.122, PPT hlm.63)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 64 | 0.2335 | …erlibat Langsung dalam Penyusunan Kebijakan (Nasional/Daerah/Industri) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 8 |
| 2 |  | Buku | 64 | 0.2346 | …erlibat Langsung dalam Penyusunan Kebijakan (Nasional/Daerah/Industri) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 8 |
| 3 | ✅ | Buku | 64 | 0.2466 | …erlibat Langsung dalam Penyusunan Kebijakan (Nasional/Daerah/Industri) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 8 |
| 4 |  | Buku | 64 | 0.2648 | …erlibat Langsung dalam Penyusunan Kebijakan (Nasional/Daerah/Industri) | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 8 |
| 5 |  | PPT | 20 | 0.2837 | …EMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK PERGURUAN TINGGI | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - III > 3.7. KETERKAITAN IKU DIKTISAINTEK BERDAMPAK DENGAN IKU KEMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMP |

</details>

<details><summary>✅ <b>H16</b> — HIT @1 — Nilai akhir evaluasi SAKIP sebuah PT adalah 82. Apa predikatnya?</summary>

**Pertanyaan:** Nilai akhir evaluasi SAKIP sebuah PT adalah 82. Apa predikatnya?

**Kata kunci bukti:** `sakip`, `sangat baik`

**Halaman benar:** 66 | **Chunk bukti di corpus:** 6 (Buku hlm.66, Buku hlm.87, Buku hlm.125–130, Buku hlm.134, Buku hlm.135, PPT hlm.66)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 87 | 0.433 | …Tinggi > IKU 3: Tata kelola LLDIKTI yang berkualitas dan berintegritas | [Buku IKU Diktisaintek Berdampak V1 / BAB - VI > 5.5. Indikator Kinerja Utama (IKU) Lembaga Layanan Pendidikan Tinggi > IKU 3: Tata kelola LLDIKTI yang berkuali |
| 2 | ✅ | Buku | 66 | 0.4065 | …tem Akuntabilitas Kinerja Instansi Pemerintah (SAKIP) Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 3 | ✅ | Buku | 135 | 0.396 | … Kepmen 358/M/KEP/2025 > 2. IKU BAGI LEMBAGA LAYANAN PENDIDIKAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 (Lampiran Kepmen 358/M/KEP/2025) / LAMPIRAN Kepmen 358/M/KEP/2025 > 2. IKU BAGI LEMBAGA LAYANAN PENDIDIKAN TINGGI / hlm. 135 |
| 4 | ✅ | PPT | 66 | 0.4592 | …K/WBBM > IKU 11.1 : Hasil audit atas Laporan Keuangan Perguruan Tinggi | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - V > 5.3. INDIKATOR KINERJA UTAMA (IKU) DIKTISAINTEK BERDAMPAK > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > 4  |
| 5 |  | Buku | 66 | 0.4374 | …tem Akuntabilitas Kinerja Instansi Pemerintah (SAKIP) Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |

</details>

<details><summary>✅ <b>H17</b> — HIT @1 — PT merencanakan 24 kegiatan pencegahan dan penanganan kekerasan, narkoba, dan korupsi; 18 </summary>

**Pertanyaan:** PT merencanakan 24 kegiatan pencegahan dan penanganan kekerasan, narkoba, dan korupsi; 18 kegiatan terlaksana. Berapa capaian IKU 11d?

**Kata kunci bukti:** `total kegiatan yang direncanakan`

**Halaman benar:** 68 | **Chunk bukti di corpus:** 3 (Buku hlm.68, Buku hlm.126–131, PPT hlm.69)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 68 | 0.3472 | …ka dan Bahan Adiktif berbahaya lainnya (narkoba); dan (3) Anti Korupsi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 2 |  | Buku | 68 | 0.3553 | …ka dan Bahan Adiktif berbahaya lainnya (narkoba); dan (3) Anti Korupsi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 3 |  | Buku | 68 | 0.351 | …ka dan Bahan Adiktif berbahaya lainnya (narkoba); dan (3) Anti Korupsi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 4 |  | Buku | 68 | 0.3584 | …ka dan Bahan Adiktif berbahaya lainnya (narkoba); dan (3) Anti Korupsi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |
| 5 |  | Buku | 68 | 0.3496 | …ka dan Bahan Adiktif berbahaya lainnya (narkoba); dan (3) Anti Korupsi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 1 |

</details>

<details><summary>✅ <b>H18</b> — HIT @1 — UMP di provinsi tempat PT berada adalah Rp3.000.000. Berapa penghasilan minimum dosen deng</summary>

**Pertanyaan:** UMP di provinsi tempat PT berada adalah Rp3.000.000. Berapa penghasilan minimum dosen dengan jabatan Lektor dan Profesor menurut IKU 12?

**Kata kunci bukti:** `lektor kepala`, `ump`

**Halaman benar:** 60 | **Chunk bukti di corpus:** 3 (Buku hlm.60, Buku hlm.131, PPT hlm.57)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 60 | 0.3951 | …12: Ketersediaan perencanaan strategis peningkatan kesejahteraan dosen | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 12: |
| 2 |  | Buku | 60 | 0.4745 | …12: Ketersediaan perencanaan strategis peningkatan kesejahteraan dosen | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 12: |
| 3 |  | Buku | 60 | 0.4715 | …12: Ketersediaan perencanaan strategis peningkatan kesejahteraan dosen | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 12: |
| 4 |  | Buku | 132 | 0.4783 | …LAMPIRAN Kepmen 358/M/KEP/2025 > 1. IKU BAGI PERGURUAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 (Lampiran Kepmen 358/M/KEP/2025) / LAMPIRAN Kepmen 358/M/KEP/2025 > 1. IKU BAGI PERGURUAN TINGGI > IKU 12. Ketersediaan pere |
| 5 |  | Buku | 51 | 0.5136 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>✅ <b>D13</b> — HIT @3 — aee tu apaan sih? ngukur apa?</summary>

**Pertanyaan:** aee tu apaan sih? ngukur apa?

**Kata kunci bukti:** `tepat waktu`, `masa studi standar`

**Halaman benar:** 49 | **Chunk bukti di corpus:** 3 (Buku hlm.49, Buku hlm.100, PPT hlm.45)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 49–50 | 0.4306 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 |  | Buku | 49–50 | 0.4607 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 | ✅ | Buku | 49 | 0.4376 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 49 | 0.5507 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 49 | 0.617 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |

</details>

<details><summary>✅ <b>D14</b> — HIT @4 — pendptan apa aj yg ga diitung di iku9?</summary>

**Pertanyaan:** pendptan apa aj yg ga diitung di iku9?

**Kata kunci bukti:** `boptn`, `iuran pengembangan institusi`

**Halaman benar:** 59 | **Chunk bukti di corpus:** 3 (Buku hlm.59, Buku hlm.122–123, PPT hlm.56)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 59 | 0.4138 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 2 |  | Buku | 59 | 0.4159 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 3 |  | Buku | 59 | 0.4198 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 4 | ✅ | Buku | 59 | 0.4209 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 5 |  | Buku | 79 | 0.4481 | …an/UKT > 1. Persentase Pendapatan terhadap Total Aset Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.5. Sub Indikator (IKU 9): Persentase Pendapatan Non Pendidikan/UKT  |

</details>

<details><summary>✅ <b>H19</b> — HIT @2 — brp aee s1 klo yg lulus tepat wktu cm 40 org dr 200 mhs?</summary>

**Pertanyaan:** brp aee s1 klo yg lulus tepat wktu cm 40 org dr 200 mhs?

**Kata kunci bukti:** `aee ideal`, `tingkat pencapaian aee`

**Halaman benar:** 49 | **Chunk bukti di corpus:** 5 (Buku hlm.49–50, Buku hlm.49–50, Buku hlm.101–102, Buku hlm.101–102, PPT hlm.46)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 49 | 0.5783 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 | ✅ | Buku | 49–50 | 0.5502 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 | ✅ | Buku | 49–50 | 0.5565 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 4 |  | Buku | 49 | 0.5286 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 49 | 0.5983 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |

</details>

<details><summary>✅ <b>H20</b> — HIT @1 — realisasi aee kampus kmi: D3 30%, S1 22,5%, S2 40%. aee pt nya jd brp ya?</summary>

**Pertanyaan:** realisasi aee kampus kmi: D3 30%, S1 22,5%, S2 40%. aee pt nya jd brp ya?

**Kata kunci bukti:** `aee pt`, `tingkat pencapaian`

**Halaman benar:** 49, 50 | **Chunk bukti di corpus:** 7 (Buku hlm.49–50, Buku hlm.49–50, Buku hlm.100, Buku hlm.101–102, Buku hlm.101–102, PPT hlm.46)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 49–50 | 0.4435 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 2 | ✅ | Buku | 49–50 | 0.4124 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 3 |  | Buku | 25 | 0.449 | …EMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK PERGURUAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 / BAB - III > 3.7. KETERKAITAN IKU DIKTISAINTEK BERDAMPAK DENGAN IKU KEMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK  |
| 4 |  | Buku | 49 | 0.5552 | …U) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 1 / |
| 5 |  | Buku | 25 | 0.4517 | …EMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK PERGURUAN TINGGI | [Buku IKU Diktisaintek Berdampak V1 / BAB - III > 3.7. KETERKAITAN IKU DIKTISAINTEK BERDAMPAK DENGAN IKU KEMENTERIAN > INDIKATOR KINERJA DIKTISAINTEK BERDAMPAK  |

</details>

<details><summary>✅ <b>H21</b> — HIT @2 — lulusan kampus kami 1.341 org, minimal responden tracer study nya brp?</summary>

**Pertanyaan:** lulusan kampus kami 1.341 org, minimal responden tracer study nya brp?

**Kata kunci bukti:** `responden minimum`, `galat`

**Halaman benar:** 52 | **Chunk bukti di corpus:** 3 (Buku hlm.52, Buku hlm.104–105, PPT hlm.48–49)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 51 | 0.5289 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 2 | ✅ | Buku | 52 | 0.5297 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 3 |  | Buku | 17 | 0.4576 | …BAB - III > 3.1. KINERJA SAAT INI – 2025 > Aspek Lulusan | [Buku IKU Diktisaintek Berdampak V1 / BAB - III > 3.1. KINERJA SAAT INI – 2025 > Aspek Lulusan / hlm. 17] Pada periode yang sama, total lulusan mengalami pening |
| 4 |  | Buku | 30 | 0.3804 | ….1. MAHASISWA PASCASARJANA > Profil Jumlah Mahasiswa Postgraduate 2024 | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.1. MAHASISWA PASCASARJANA > Profil Jumlah Mahasiswa Postgraduate 2024 / hlm. 30] * Target yang ingin dicapai  |
| 5 |  | PPT | 34 | 0.4299 | …- IV > 4.7. POSTDOCTORALPROGRAM > Target Penerima Postdoctoral program | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.7. POSTDOCTORALPROGRAM > Target Penerima Postdoctoral program / hlm. 34] / <br>**1.000**<br>**Orang** / PT |

</details>

<details><summary>✅ <b>H22</b> — HIT @2 — klo lulusannya 2rb orang, responden minimum tracer studi brp</summary>

**Pertanyaan:** klo lulusannya 2rb orang, responden minimum tracer studi brp

**Kata kunci bukti:** `responden minimum`, `galat`

**Halaman benar:** 52 | **Chunk bukti di corpus:** 3 (Buku hlm.52, Buku hlm.104–105, PPT hlm.48–49)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 51 | 0.4377 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 2 | ✅ | Buku | 52 | 0.4419 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 3 |  | PPT | 34 | 0.4043 | …- IV > 4.7. POSTDOCTORALPROGRAM > Target Penerima Postdoctoral program | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.7. POSTDOCTORALPROGRAM > Target Penerima Postdoctoral program / hlm. 34] / <br>**1.000**<br>**Orang** / PT |
| 4 |  | Buku | 51 | 0.4534 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |
| 5 |  | Buku | 51 | 0.4586 | …Berikutnya/ Berwirausaha dalam Jangka Waktu 1 Tahun Setelah Kelulusan. | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 2 IKU 2 |

</details>

<details><summary>✅ <b>H23</b> — HIT @1 — kerjsama PT kita ada 120, luaran nya 30 judul. capaian iku5 brp persen?</summary>

**Pertanyaan:** kerjsama PT kita ada 120, luaran nya 30 judul. capaian iku5 brp persen?

**Kata kunci bukti:** `total kerjasama perguruan tinggi`, `bukan jumlah dosen`

**Halaman benar:** 57 | **Chunk bukti di corpus:** 3 (Buku hlm.57–58, Buku hlm.117, PPT hlm.53)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 57–58 | 0.389 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 2 |  | Buku | 55–56 | 0.4116 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 3 |  | Buku | 55–56 | 0.4106 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 4 |  | Buku | 55–56 | 0.4183 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |
| 5 |  | Buku | 55–56 | 0.42 | … Hasil Kerjasama Antara Perguruan Tinggi dan Start-Up/Industri/Lembaga | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 4 IKU 5 |

</details>

<details><summary>✅ <b>H24</b> — HIT @4 — dr 50 progam sdgs, 25 yg kontribusi ke sdg 1,4,17 + 2 sdg pilihan. capaian iku 7 brapa</summary>

**Pertanyaan:** dr 50 progam sdgs, 25 yg kontribusi ke sdg 1,4,17 + 2 sdg pilihan. capaian iku 7 brapa

**Kata kunci bukti:** `total program sdg`

**Halaman benar:** 58 | **Chunk bukti di corpus:** 3 (Buku hlm.58, Buku hlm.121, PPT hlm.55)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | Buku | 58 | 0.479 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 2 |  | Buku | 58 | 0.4934 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 3 |  | Buku | 58 | 0.4748 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 4 | ✅ | Buku | 58 | 0.4672 | …Berkualitas), SDG17 (Kemitraan), dan 2(dua)SDGs Lain Sesuai Keunggulan | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 7:  |
| 5 |  | Buku | 47 | 0.4594 | … V > 5.2. Ruang Lingkup Indikator Kinerja Utama Diktisaintek Berdampak | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.2. Ruang Lingkup Indikator Kinerja Utama Diktisaintek Berdampak / hlm. 47] %% Indicators for 2b Kontribusi I7( |

</details>

<details><summary>✅ <b>H25</b> — HIT @2 — total pendapatan PT 500 M. rinciannya ukt 300M, boptn 80 M, hibah riset 50M, konsultasi 40</summary>

**Pertanyaan:** total pendapatan PT 500 M. rinciannya ukt 300M, boptn 80 M, hibah riset 50M, konsultasi 40 M, unit bisnis 20M, hasil dana abadi 10 M. iku 9 brp?

**Kata kunci bukti:** `boptn`, `dana abadi`

**Halaman benar:** 59 | **Chunk bukti di corpus:** 3 (Buku hlm.59, Buku hlm.122–123, PPT hlm.56)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 |  | PPT | 40 | 0.4665 | …BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: / hlm. 40] **Rata-Rata Dana Masyarakat Top 5 PTNBH = Rp 1 |
| 2 | ✅ | Buku | 59 | 0.4978 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 3 |  | Buku | 79 | 0.5115 | …an/UKT > 1. Persentase Pendapatan terhadap Total Aset Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.5. Sub Indikator (IKU 9): Persentase Pendapatan Non Pendidikan/UKT  |
| 4 |  | Buku | 79–80 | 0.5317 | …entase DIPA/APBN Pemerintah terhadap Total Pendapatan Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.5. Sub Indikator (IKU 9): Persentase Pendapatan Non Pendidikan/UKT  |
| 5 |  | Buku | 81 | 0.4878 | …an/UKT > c) Persentase Dana Abadi Terhadap Total Aset Perguruan Tinggi | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.5. Sub Indikator (IKU 9): Persentase Pendapatan Non Pendidikan/UKT  |

</details>

<details><summary>✅ <b>H26</b> — HIT @1 — pendapatan total Rp1.250.000.000, terdiri dr ukt rp 900jt, kontrak riset 150 juta, royalti</summary>

**Pertanyaan:** pendapatan total Rp1.250.000.000, terdiri dr ukt rp 900jt, kontrak riset 150 juta, royalti Rp50.000.000, sisanya 150jt dari boptn. capaian iku 9?

**Kata kunci bukti:** `boptn`, `dana abadi`

**Halaman benar:** 59 | **Chunk bukti di corpus:** 3 (Buku hlm.59, Buku hlm.122–123, PPT hlm.56)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 59 | 0.4424 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 2 |  | Buku | 59 | 0.5077 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 3 |  | Buku | 59 | 0.4946 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 4 |  | Buku | 59 | 0.5321 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 5 |  | PPT | 23 | 0.4461 | …BAB - III > 3.8. PROFIL DAN DAMPAK PT INDONESIA > Kontribusi ekonomi | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - III > 3.8. PROFIL DAN DAMPAK PT INDONESIA > Kontribusi ekonomi / hlm. 23] **±Rp. 390 T*** (exc. riset dan pengmas |

</details>

<details><summary>✅ <b>H27</b> — HIT @1 — total pendapatan 2 milyar: hibah riset 300 jt, konsultasi 0,2 M, ukt 1,5 M. hitung iku 9 n</summary>

**Pertanyaan:** total pendapatan 2 milyar: hibah riset 300 jt, konsultasi 0,2 M, ukt 1,5 M. hitung iku 9 nya

**Kata kunci bukti:** `boptn`, `dana abadi`

**Halaman benar:** 59 | **Chunk bukti di corpus:** 3 (Buku hlm.59, Buku hlm.122–123, PPT hlm.56)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 59 | 0.4379 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 2 |  | Buku | 59 | 0.4765 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 3 |  | Buku | 59 | 0.5179 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 4 |  | Buku | 59 | 0.5256 | … Utama (IKU) Wajib > 6 IKU 9: Persentase Pendapatan Non Pendidikan/UKT | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > 6 IKU 9 |
| 5 |  | PPT | 40 | 0.3966 | …BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: / hlm. 40] **Rata-Rata Dana Masyarakat Top 5 PTNBH = Rp 1 |

</details>

<details><summary>✅ <b>H28</b> — HIT @1 — ump disini 3,5jt, penghasilan minimal dosen lektor kepala brp?</summary>

**Pertanyaan:** ump disini 3,5jt, penghasilan minimal dosen lektor kepala brp?

**Kata kunci bukti:** `lektor kepala`, `ump`

**Halaman benar:** 60 | **Chunk bukti di corpus:** 3 (Buku hlm.60, Buku hlm.131, PPT hlm.57)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 60 | 0.4592 | …12: Ketersediaan perencanaan strategis peningkatan kesejahteraan dosen | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 12: |
| 2 |  | PPT | 40 | 0.4446 | …BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: / hlm. 40] **Rata-Rata Dana Masyarakat Top 5 PTNBH = Rp 1 |
| 3 |  | Buku | 44 | 0.4768 | …B - IV > 4.11. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh Perhitungan | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.11. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh Perhitungan / hlm. 44] **Contoh:** Rata-Rata Dana Masyarakat  |
| 4 |  | Buku | 72 | 0.4845 | …apatkan Rekognisi Internasional > a. Persentase Dosen Berpendidikan S3 | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.4. Sub Indikator Kinerja Utama (IKU) > 5.4.2. Sub Indikator (IKU 4): Jumlah Dosen Perguruan Tinggi yang Mendap |
| 5 |  | PPT | 23 | 0.4044 | …BAB - III > 3.8. PROFIL DAN DAMPAK PT INDONESIA > Kontribusi ekonomi | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - III > 3.8. PROFIL DAN DAMPAK PT INDONESIA > Kontribusi ekonomi / hlm. 23] **±Rp. 390 T*** (exc. riset dan pengmas |

</details>

<details><summary>✅ <b>H29</b> — HIT @1 — UMP prov kami Rp 4.250.000 , brp penghasilan min dosen asisten ahli sm profesor?</summary>

**Pertanyaan:** UMP prov kami Rp 4.250.000 , brp penghasilan min dosen asisten ahli sm profesor?

**Kata kunci bukti:** `lektor kepala`, `ump`

**Halaman benar:** 60 | **Chunk bukti di corpus:** 3 (Buku hlm.60, Buku hlm.131, PPT hlm.57)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 60 | 0.4553 | …12: Ketersediaan perencanaan strategis peningkatan kesejahteraan dosen | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.1. Indikator Kinerja Utama (IKU) Wajib > IKU 12: |
| 2 |  | PPT | 23 | 0.4074 | …BAB - III > 3.8. PROFIL DAN DAMPAK PT INDONESIA > Kontribusi ekonomi | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - III > 3.8. PROFIL DAN DAMPAK PT INDONESIA > Kontribusi ekonomi / hlm. 23] **±Rp. 390 T*** (exc. riset dan pengmas |
| 3 |  | Buku | 35 | 0.4443 | …BAB - IV > 4.4. PENINGKATAN DOSEN BERKUALIFIKASI DOKTOR > Asumsi: | [Buku IKU Diktisaintek Berdampak V1 / BAB - IV > 4.4. PENINGKATAN DOSEN BERKUALIFIKASI DOKTOR > Asumsi: / hlm. 35] * Apabila di alokasikan dana dari Dana Masyar |
| 4 |  | PPT | 40 | 0.4587 | …BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: | [PPT IKU Diktisaintek Berdampak PTS V2 / BAB - IV > 4.12. ALOKASI PENDAPATAN DANA MASYARAKAT > Contoh: / hlm. 40] **Rata-Rata Dana Masyarakat Top 5 PTNBH = Rp 1 |
| 5 |  | Buku | 90 | 0.4809 | …ggi > IKU 5: Pencegahan dan penanganan kekerasan, narkoba, dan korupsi | [Buku IKU Diktisaintek Berdampak V1 / BAB - VI > 5.5. Indikator Kinerja Utama (IKU) Lembaga Layanan Pendidikan Tinggi > IKU 5: Pencegahan dan penanganan kekeras |

</details>

<details><summary>✅ <b>H30</b> — HIT @1 — dosen kami 250 org setahun terakhir, yg ber-NUPTK & dpt rekognisi internasional 18 org. ca</summary>

**Pertanyaan:** dosen kami 250 org setahun terakhir, yg ber-NUPTK & dpt rekognisi internasional 18 org. capaiannya brp?

**Kata kunci bukti:** `nuptk`, `rekognisi internasional`

**Halaman benar:** 62 | **Chunk bukti di corpus:** 3 (Buku hlm.62–63, Buku hlm.112, PPT hlm.60–61)

| # | Bukti | Sumber | Hlm. | Distance | Section | Cuplikan |
|---|---|---|---|---|---|---|
| 1 | ✅ | Buku | 62–63 | 0.3431 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 2 |  | Buku | 61 | 0.3787 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 3 |  | Buku | 61–62 | 0.4168 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 4 |  | Buku | 61–62 | 0.4481 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |
| 5 |  | Buku | 61–62 | 0.4006 | …entase Dosen Perguruan Tinggi yang Mendapatkan Rekognisi Internasional | [Buku IKU Diktisaintek Berdampak V1 / BAB - V > 5.3. Indikator Kinerja Utama (IKU) Diktisaintek Berdampak > 5.3.2. Indikator Kinerja Utama (IKU) Pilihan > IKU 4 |

</details>
