# Uji Jawaban Chatbot (retriever + LLM + kalkulator)

- Waktu: 2026-10-28 18:32:49
- Model LLM: `openai/gpt-oss-120b`
- Soal: 1 dari 1 dijalankan (hitungan 1, definisi & jebakan 0)
- Status run: selesai

## Ringkasan

| Metrik | Hasil |
|---|---|
| Lulus semua pemeriksaan otomatis | **1/1** |
| Hitungan: kalkulator dipanggil | 1/1 |
| Hitungan: hasil kalkulator = kunci | 1/1 |
| Hitungan: angka kunci ada di jawaban | 1/1 |
| Halaman sitasi benar (hitungan) | 1/1 |
| Halaman sitasi benar (definisi) | - |
| Soal error (API/kuota) | 0 |
| Jawaban dengan peringatan chatbot | 1 |

| ID | Status | Pemeriksaan yang gagal |
|---|---|---|
| H25 | ✅ | - |

Pemeriksaan otomatis hanya bantuan. Baca jawaban lengkap di bawah dan bandingkan dengan jawaban yang diharapkan.

## Detail per soal

### H25 — ✅ LULUS

**Pertanyaan:** total pendapatan PT 500 M. rinciannya ukt 300M, boptn 80 M, hibah riset 50M, konsultasi 40 M, unit bisnis 20M, hasil dana abadi 10 M. iku 9 brp?

**Jawaban chatbot:**

```text
IKU 9 – Persentase Pendapatan Non Pendidikan/UKT dihitung dengan rumus:

Capaian = (Jumlah pendapatan non-mahasiswa ÷ Total pendapatan PT dalam satu periode) × 100 %

Pendapatan non-mahasiswa yang termasuk (menurut kriteria) adalah:
- Hibah riset = 50 M  
- Konsultasi = 40 M  
- Unit bisnis = 20 M  
- Hasil dana abadi = 10 M  

Jumlah pendapatan non-mahasiswa = 50 M + 40 M + 20 M + 10 M = **120 M**.

Total pendapatan PT = **500 M**.

Menggunakan kalkulator IKU 9:

**Capaian = 120 M ÷ 500 M × 100 % = 24 %**【iku9】.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 9 – Kriteria & Formula, hlm. 59

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_pendapatan\": \"500 M\", \"rincian\": {\"hibah_riset\": \"50 M\", \"konsultasi\": \"40 M\", \"unit_bisnis\": \"20 M\", \"hasil_dana_abadi\": \"10 M\"}}","fungsi":"iku9"}` → 24,00

**Peringatan chatbot:**

- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **24,00**
- Halaman kunci: 59

**24%**.

*Catatan soal:* Ketahanan: satuan 'M' = miliar, ditulis rapat/berspasi ('300M', '80 M'). Argumen boleh dalam miliar asal konsisten. Sama dengan H13.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar
