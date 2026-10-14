# LANGKAH B: HASIL TES BASELINE INTENT DETECTION

**Tanggal**: 2026-10-15  
**Dataset**: 48 kasus (tests/intent_cases.json)  
**Kategori**: data (13), definisi (8), formula (10), hybrid (7), general (10)

---

## RINGKASAN EKSEKUTIF

**Kedua implementasi memiliki akurasi keseluruhan yang sama (75%), tetapi dengan kelemahan yang berbeda dan 9 kasus konflik kritis yang menyebabkan perilaku endpoint tidak konsisten.**

### Masalah Kritis

1. **Inkonsistensi Routing**: 9 kasus di mana `app.py` memutuskan skip RAG tetapi `answer.py` tidak butuh spreadsheet (atau sebaliknya)
2. **Persyaratan Tahun**: `answer.py` wajib ada tahun (202X-203X) untuk detect data, tetapi dokumentasi menyatakan tahun opsional
3. **False Positive "data"**: `app.py` classify "berapa capaian IKU 3?" sebagai data (seharusnya formula)
4. **Tidak ada deteksi hybrid**: Keduanya tidak punya kategori hybrid, hanya map ke data atau definisi

---

## 1. AKURASI PER IMPLEMENTASI

### app.py (detect_intent)
```
Overall: 36/48 = 75.0%

Per kategori:
  data      :  8/13 =  61.5%  ← LEMAH
  definisi  :  8/ 8 = 100.0%  ← SEMPURNA
  formula   :  5/10 =  50.0%  ← LEMAH
  general   : 10/10 = 100.0%  ← SEMPURNA
  hybrid    :  5/ 7 =  71.4%
```

**Kelemahan utama**:
- Terlalu agresif classify "berapa" + "capaian/nilai" sebagai `data`, termasuk pertanyaan formula
- Formula hanya 50% karena salah classify sebagai data (2 kasus) atau definisi (3 kasus)

### answer.py (intent_butuh_spreadsheet)
```
Overall: 36/48 = 75.0%

Per kategori:
  data      :  4/13 =  30.8%  ← SANGAT LEMAH
  definisi  :  8/ 8 = 100.0%  ← SEMPURNA
  formula   : 10/10 = 100.0%  ← SEMPURNA
  general   : 10/10 = 100.0%  ← SEMPURNA
  hybrid    :  4/ 7 =  57.1%  ← LEMAH
```

**Kelemahan utama**:
- Data hanya 30.8% karena **wajib ada tahun (202X-203X)** di pertanyaan
- 9 dari 13 kasus data di-reject karena tidak ada tahun eksplisit

---

## 2. CONFUSION MATRIX

### app.py
```
Expected     | Predicted            | Count | Analisis
-------------|----------------------|-------|------------------
data         | data                 |   8   | Benar
data         | definisi             |   5   | Miss: tanpa tahun atau keyword lemah
formula      | data                 |   2   | False positive: "berapa capaian"
formula      | definisi             |   3   | Miss: tidak detect "cara hitung"
formula      | formula              |   5   | Benar
general      | definisi             |  10   | Toleransi: fallback ke definisi OK
hybrid       | data                 |   5   | Partial benar (butuh data)
hybrid       | definisi/formula     |   2   | Miss: tidak detect komponen data
```

### answer.py
```
Expected     | Predicted                 | Count | Analisis
-------------|---------------------------|-------|------------------
data         | butuh_spreadsheet         |   4   | Benar (ada tahun)
data         | tidak_butuh_spreadsheet   |   9   | Miss: TIDAK ADA TAHUN
hybrid       | butuh_spreadsheet         |   4   | Benar (ada tahun + data)
hybrid       | tidak_butuh_spreadsheet   |   3   | Miss: tidak ada tahun
```

---

## 3. KASUS KONFLIK KRITIS (9 kasus)

Kasus di mana routing `app.py` dan `answer.py` berbeda keputusan:

### Konflik Tipe A: app.py skip RAG, answer.py tidak butuh data (8 kasus)

| ID | Pertanyaan | Impact di /v1/answer |
|----|-----------|----------------------|
| DATA-03 | "Bagaimana capaian IKU 5 universitas kami tahun lalu?" | app.py return action tanpa RAG, tapi sebenarnya butuh RAG untuk konteks IKU |
| DATA-06 | "Nilai IKU kampus saya?" | app.py skip RAG (tanpa tahun), tapi answer.py reject karena tidak ada tahun |
| DATA-07 | "Berapa total lulusan bekerja PT kami tahun 2025?" | app.py skip RAG, padahal butuh RAG untuk tahu "lulusan bekerja" = IKU 2 |
| DATA-08 | "Capaian IKU 7 kampus kami gimana?" | app.py skip RAG tanpa tahun, answer.py reject |
| FORM-03 | "Bagaimana menghitung capaian IKU 2?" | **FALSE POSITIVE**: app.py classify sebagai data karena kata "capaian", harusnya formula |
| HYB-06 | "Berapa capaian kampus saya dan bagaimana meningkatkannya?" | app.py skip RAG, tidak detect komponen "bagaimana meningkatkan" |
| EDGE-01 | "Berapa capaian IKU 3?" | **FALSE POSITIVE**: app.py classify data, harusnya formula (tidak ada "kampus saya") |
| EDGE-02 | "Nilai IKU kampus saya?" | Duplikat DATA-06 |

### Konflik Tipe B: app.py panggil RAG, answer.py butuh data (1 kasus)

| ID | Pertanyaan | Impact di /v1/answer |
|----|-----------|----------------------|
| DATA-04 | "data saya IKU 2 2023" | app.py classify definisi (miss keyword), answer.py detect tahun → butuh data, tapi RAG sudah dipanggil |

**Dampak di endpoint /v1/answer**:
- Tipe A: User tidak mendapat konteks IKU dari RAG, hanya diminta fetch data
- Tipe B: RAG dipanggil tanpa perlu (waste resource), lalu answer.py panggil spreadsheet tool juga

---

## 4. ANALISIS EDGE CASES

Total 8 edge cases, 6 salah klasifikasi:

| ID | Pertanyaan | Expected | app.py | answer.py | Analisis |
|----|-----------|----------|--------|-----------|----------|
| EDGE-01 | "Berapa capaian IKU 3?" | formula | data ✗ | False ✓ | **Kasus paling kritis**: "berapa capaian" tanpa "kampus saya" seharusnya formula, bukan data |
| EDGE-02 | "Nilai IKU kampus saya?" | data | data ✓ | False ✗ | Tanpa tahun: app.py detect, answer.py reject |
| EDGE-03 | "IKU 5 kampus kami" | data | definisi ✗ | False ✗ | Kedua gagal: keyword terlalu minimal |
| EDGE-06 | "IKU 3 kita di 2024 itu apa dan berapa?" | hybrid | definisi ✗ | False ✗ | Kata ganti "kita" tidak dikenali sebagai proxy "kampus kita" |
| EDGE-07 | "data IKU 1 2024 2025 2026" | data | definisi ✗ | False ✗ | Keyword "data" di awal tidak dikenali (hanya match "data saya/kampus") |
| EDGE-08 | "berapa bobot publikasi Q1 di IKU 6?" | formula | definisi ✗ | False ✓ | "Berapa" + istilah teknis harusnya formula, bukan data |

**Temuan**:
- "Berapa" + ukuran IKU **TANPA** "kampus saya/kami/pt" = pertanyaan tentang **rumus**, bukan data
- Kata ganti "kita" tidak dikenali
- Keyword "data" standalone tidak dikenali (harus "data saya/kampus")
- Multiple tahun tidak dihandle (expected: clarify)

---

## 5. ROOT CAUSE ANALYSIS

### app.py (detect_intent)

**Logika saat ini**:
```python
if any(kw in q_lower for kw in ["kampus saya", "data saya", "nilai iku", "capaian iku"]):
    if any(word in q_lower for word in ["berapa", "jumlah", "total", "nilai", "capaian"]):
        return "data"
```

**Masalah**:
1. **Prioritas salah**: Check "nilai iku" dan "capaian iku" DI DALAM data_keywords, jadi "berapa capaian IKU 3" match
2. **Tidak check konteks**: Seharusnya "berapa capaian" + "kampus/pt/saya" → data, tanpa itu → formula
3. **Tidak butuh tahun**: app.py tidak check tahun, tapi answer.py butuh → inkonsistensi

### answer.py (intent_butuh_spreadsheet)

**Logika saat ini**:
```python
keywords = ["kampus saya", "data saya", "nilai iku", "capaian iku", "berapa iku"]
tahun_pattern = r"\b(202[0-9]|203[0-9])\b"
return has_keyword and has_tahun
```

**Masalah**:
1. **Tahun wajib**: Dokumentasi bilang tahun opsional, tapi kode wajib ada tahun → 9/13 data di-reject
2. **Keyword terlalu spesifik**: Tidak match "data IKU", "IKU kampus", "kita" (proxy "kami")
3. **Boolean only**: Tidak bisa detect hybrid atau general

---

## 6. REKOMENDASI PERBAIKAN

### Priority 1: Satu Modul Intent (src/generation/intent.py)

**Label**: `data`, `definisi`, `formula`, `hybrid`, `general`

**Rules**:
```
1. GENERAL (prioritas tertinggi):
   - Sapaan: "halo", "terima kasih", "siapa kamu"
   - Out-of-scope: tidak menyebut IKU atau topik terkait

2. DATA:
   - (keyword_kampus OR keyword_data) AND keyword_numerik
   - keyword_kampus: "kampus|pt|universitas" + "saya|kami|kita"
   - keyword_data: "data saya/kampus", "nilai iku", "capaian iku"
   - keyword_numerik: "berapa", "jumlah", "total", "nilai", "capaian", "gimana" (informal)
   - Tahun OPSIONAL: extract bila ada, kirim null bila tidak ada

3. FORMULA:
   - Eksplisit: "rumus", "formula", "cara hitung", "bagaimana hitung", "dihitung"
   - Implisit: "berapa" + ukuran_iku TANPA keyword_kampus
   - Contoh: "berapa capaian IKU 3" (tanpa "kampus saya") → formula

4. DEFINISI:
   - "apa itu", "definisi", "pengertian", "maksud", "arti", "jelaskan"
   - Atau default bila tidak match lainnya dan menyebut IKU

5. HYBRID:
   - Gabungan eksplisit: "... dan ..." atau "..., jelaskan ..."
   - DATA AND (FORMULA OR DEFINISI)
```

**Ekstraksi Parameter**:
- `tahun`: regex `\b(202[0-9]|203[0-9])\b` → return list atau null
- `iku`: regex `IKU\s*(\d{1,2})` → return string atau null
- `unit`: extract "fakultas", "prodi", "universitas" (future)

### Priority 2: Dua Tahap di Endpoint

**Tahap 1**: Request tanpa data
```python
intent, params = detect_intent_and_params(question)
if intent in ["data", "hybrid"] and "data" not in request:
    return {
        "answer": "Memproses permintaan data...",
        "action": {"type": "fetch_data", "params": params},
        "intent": intent,
    }
```

**Tahap 2**: Request dengan data (dari TypeScript)
```python
# RAG selalu dipanggil (untuk konteks IKU)
chunks = retriever.search(question)

# Gabung data dari frontend dengan konteks RAG
context = build_context(chunks)
if request.get("pageFacts"):  # nama field sesuai integrasi_backend.md
    context += format_data_context(request["pageFacts"])

# LLM jawab
hasil = llm.ask(context, question)
```

### Priority 3: Field "intent" di Response

Tanpa merusak kontrak lama:
```json
{
  "answer": "...",
  "citations": [...],
  "grounded": true,
  "intent": "data",           // BARU
  "params": {"tahun": "2024", "iku": "3"},  // BARU
  "action": null
}
```

---

## 7. METRIK TARGET SETELAH PERBAIKAN

| Metrik | Baseline | Target |
|--------|----------|--------|
| Overall Accuracy | 75% | **≥90%** |
| Data Category | 30.8% (answer.py) / 61.5% (app.py) | **≥90%** |
| Formula Category | 50% (app.py) | **≥90%** |
| Hybrid Detection | 57-71% (partial) | **≥85%** |
| Konflik app vs answer | 9 kasus | **0 kasus** |
| False Positive "berapa capaian" | 2 kasus | **0 kasus** |

---

## 8. FILE TERLIBAT

**Baseline saat ini**:
- `src/api/app.py` - detect_intent() (belum commit)
- `src/generation/answer.py` - intent_butuh_spreadsheet()
- `tests/intent_cases.json` - dataset 48 kasus
- `tests/test_intent_baseline.py` - script test
- `reports/intent_baseline_test.json` - hasil lengkap

**Akan dibuat**:
- `src/generation/intent.py` - modul tunggal, sumber kebenaran
- `tests/test_intent_module.py` - unit test per rule
- `tests/test_endpoint_two_phase.py` - test tahap 1 & 2

---

## 9. KESIMPULAN

**Baseline menunjukkan dua implementasi yang tidak konsisten dengan 9 kasus konflik kritis. Implementasi baru dengan OPSI C (dua tahap) akan menyelesaikan masalah ini dengan:**

1. **Satu modul intent** sebagai sumber kebenaran
2. **Tahun opsional** dengan ekstraksi parameter
3. **Deteksi hybrid dan general** yang eksplisit
4. **RAG selalu dipanggil** (sesuai dokumentasi)
5. **Data dari TypeScript** (privasi + two-phase)

**Next Steps**: Commit baseline → Implementasi perbaikan → Test ulang dengan dataset yang sama → Bandingkan metrik.
