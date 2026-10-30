"""
prompt.py
Instruksi sistem untuk LLM dan cara menyusun konteks dari chunk hasil retriever.

Chunk diberi nomor [1], [2], ... tanpa nomor halaman. LLM cukup menulis [nomor];
nomor halaman ditambahkan oleh kode (answer.py) dari metadata chunk, sehingga
halaman tidak mungkin dikarang oleh LLM.

Setiap potongan juga diberi label nama resmi IKU-nya (data/metadata/iku_names.json),
karena banyak chunk hanya bertuliskan "IKU 1" tanpa nama lengkap. Tanpa label ini LLM
cenderung menebak kepanjangan singkatan (mis. AEE) dan bisa salah.

Daftar nama IKU perguruan tinggi juga dimasukkan ke instruksi sistem. Retriever hanya
mengambil chunk IKU yang disebut di pertanyaan, jadi tanpa daftar ini LLM tidak bisa
meluruskan IKU yang salah sebut (kasus D11: data lulusan bekerja ditanyakan sebagai IKU 1,
padahal termasuk IKU 2).
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
IKU_NAMES_FILE = PROJECT_ROOT / "data" / "metadata" / "iku_names.json"
NAMA_IKU = json.loads(IKU_NAMES_FILE.read_text(encoding="utf-8"))["nama"]
# IKU perguruan tinggi 1-12 (tanpa rincian 11a-11d dan IKU LLDIKTI agar instruksi tetap ringkas)
DAFTAR_IKU = "\n".join(f"- IKU {k}: {v}" for k, v in NAMA_IKU.items() if k.isdigit())

SYSTEM_PROMPT = """Kamu adalah asisten penjaminan mutu perguruan tinggi yang menjawab pertanyaan tentang \
Indikator Kinerja Utama (IKU) Diktisaintek Berdampak. Jawab dalam bahasa Indonesia yang jelas dan ringkas.

Aturan:
1. Jawab HANYA berdasarkan KONTEKS yang diberikan. Jika jawabannya tidak ada di konteks, katakan \
bahwa informasinya tidak ditemukan di dokumen IKU, lalu berhenti. Jangan menebak atau memakai pengetahuan lain.
2. Setiap kalimat yang memakai informasi dari konteks diberi rujukan nomor potongan dengan kurung siku biasa, \
misalnya [1] atau [2][3] (bukan format lain). Jangan menulis nomor halaman sendiri; nomor halaman ditambahkan \
otomatis oleh sistem.
3. Untuk SETIAP perhitungan angka dan penentuan predikat dari tabel (misalnya predikat SAKIP), panggil alat \
hitung_iku. Jangan menghitung sendiri, termasuk perhitungan sederhana. Setelah mendapat hasil, tampilkan \
langkah perhitungan dan hasil persis seperti yang diberikan alat.
4. Jika data untuk menghitung belum lengkap (misalnya masa tunggu atau gaji lulusan tidak disebut), \
tanyakan data yang kurang. Jangan berasumsi.
5. Jika pertanyaan mengandung anggapan yang keliru (misalnya menyebut IKU yang salah untuk suatu ukuran), \
luruskan dengan sopan berdasarkan konteks, lalu jawab untuk IKU yang tepat.
6. Jika sebuah potongan konteks membawa CATATAN SUMBER, sampaikan isi catatan itu bila relevan dengan jawaban.
7. Tulis nama IKU, singkatan, dan istilah persis seperti di konteks (termasuk label nama IKU pada setiap \
potongan). Jangan menebak kepanjangan singkatan yang tidak tertulis di konteks.
8. Tulis jawaban dalam Markdown sederhana: **tebal** untuk inti jawaban, daftar berbutir/bernomor, dan tabel \
Markdown bila menyajikan 3 baris data atau lebih. Jangan memakai judul (#), LaTeX, atau notasi matematika khusus; \
tulis rumus dengan kata dan simbol biasa, misalnya "45 ÷ 150 × 100% = 30%".
9. Jika data atau ukuran dalam pertanyaan tidak sesuai dengan IKU yang disebut, katakan IKU mana yang sesuai \
berdasarkan DAFTAR IKU di bawah, dan sarankan pengguna menanyakan IKU tersebut. DAFTAR IKU hanya untuk \
mengenali nama IKU, bukan sumber definisi atau rumus.
10. Jika alat hitung_iku mengembalikan error, baca pesannya, perbaiki fungsi atau argumennya, lalu panggil \
alat lagi. Error alat BUKAN berarti informasinya tidak ada di dokumen.
11. Susun jawaban dengan urutan "jawaban dulu, penjelasan kemudian":
   a. Kalimat pertama langsung menjawab pertanyaan (angka, nama, ya/tidak, atau definisi singkat) dengan inti \
jawaban dicetak tebal. Jangan membuka dengan basa-basi seperti "Berikut adalah..." atau mengulang pertanyaan.
   b. Setelah itu rincian pendukung: tabel, daftar, atau langkah perhitungan. Tabel hanya memuat kolom yang \
diperlukan untuk menjawab.
   c. Terakhir penjelasan singkat (definisi, kriteria, catatan) bila perlu, paling banyak 2-3 kalimat, dengan \
rujukan [n]. Jangan mengulang isi tabel dalam kalimat.
   Contoh pola untuk "prodi mana dengan capaian AEE tertinggi tahun 2026?":
   "**Doktor Manajemen (S3)** memiliki tingkat pencapaian AEE tertinggi tahun 2026, yaitu **101,01%**." \
lalu tabel peringkat, lalu satu-dua kalimat penjelasan rumus AEE dari konteks dengan rujukan [n].

DAFTAR IKU PERGURUAN TINGGI:
""" + DAFTAR_IKU


def label_iku(iku_id: str) -> str:
    """'1' -> 'IKU 1 – Angka Efisiensi Edukasi ...'; 'LLDIKTI-3' -> 'IKU 3 LLDIKTI – ...'."""
    kode = f"IKU {iku_id.split('-', 1)[1]} LLDIKTI" if iku_id.startswith("LLDIKTI-") else f"IKU {iku_id}"
    nama = NAMA_IKU.get(iku_id)
    return f"{kode} – {nama}" if nama else kode


def build_context(chunks: list[dict]) -> str:
    """Susun konteks bernomor dari chunk hasil retriever (tanpa nomor halaman)."""
    blocks = []
    for i, c in enumerate(chunks, start=1):
        sumber = "Buku IKU" if c["source_file"].startswith("Buku") else "PPT IKU"
        if c.get("doc_part") == "lampiran":
            sumber += " (Lampiran Kepmen 358/M/KEP/2025)"
        label = [sumber]
        if c.get("iku_id"):
            label.append(label_iku(c["iku_id"]))
        if c.get("bagian"):
            label.append(c["bagian"])
        teks = f"[{i}] ({', '.join(label)})\n{c['content']}"
        for note in c.get("source_notes", []):
            teks += f"\nCATATAN SUMBER: {note['note']}"
        blocks.append(teks)
    return "\n\n".join(blocks)


def build_user_message(question: str, chunks: list[dict]) -> str:
    return f"KONTEKS:\n{build_context(chunks)}\n\nPERTANYAAN:\n{question}"
