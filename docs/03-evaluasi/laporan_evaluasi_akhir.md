# Laporan Evaluasi Chatbot RAG IKU

Tanggal evaluasi: 10-11 Oktober 2026. Model AI: `openai/gpt-oss-120b` (Groq, paket gratis). Sumber data:
`reports/evaluation/answer_test_openai-gpt-oss-120b_20261010_160510.json` (jawaban) dan
`reports/evaluation/retrieval_eval_pmpt_qa_v2_20261011_015956.json` (pencarian dokumen).

## 1. Ringkasan

Chatbot lulus **41 dari 44 soal uji (93%)** dan bukti yang benar masuk 5 potongan teratas pada **41 dari 43 soal (95,3%)**. Layak untuk demo terbatas; belum layak dibuka luas sebelum bug H28 diperbaiki dan model berbayar tersedia.

| Perkembangan | Soal lulus |
|---|---|
| 8 Oktober 2026 | 20 dari 36 |
| 9 Oktober 2026 | 36 dari 44 |
| 10 Oktober 2026 | **41 dari 44** |

Tiga soal belum lulus: **H28** (bug pembacaan nominal uang, paling penting), **D03** (format rujukan rusak), **D06** (syarat pendampingan dosen tidak disebut).

## 2. Penjelasan metrik

Chatbot dinilai dua kali: seberapa benar **jawaban akhirnya** (bagian A) dan seberapa baik **pencarian dokumennya** (bagian B).

### A. Metrik jawaban chatbot (44 soal)

| Metrik | Artinya | Hasil |
|---|---|---|
| Lulus semua pemeriksaan otomatis | Satu soal lulus bila semua pemeriksaan di bawah terpenuhi. Pemeriksaan otomatis hanya bantuan; jawaban tetap perlu dibaca manual | **41/44** |
| Kalkulator dipanggil (soal hitungan) | AI wajib memakai kalkulator untuk setiap angka dan tidak boleh menghitung sendiri | 30/30 |
| Hasil kalkulator = kunci | Angka dari kalkulator sama dengan jawaban resmi di test set (selisih maksimal 0,01) | 29/30 (gagal: H28) |
| Angka kunci ada di jawaban | Angka yang benar tertulis di jawaban yang dibaca pengguna. Tidak cukup sendirian: H28 lulus di sini padahal angkanya tidak berasal dari kalkulator | 30/30 |
| Halaman sitasi benar | Halaman Buku yang dicantumkan chatbot cocok dengan halaman bukti | Hitungan 30/30; definisi 12/13 (gagal: D03) |
| Fakta kunci (soal definisi) | Setiap fakta wajib, misalnya "tepat waktu", muncul di jawaban dalam salah satu bentuk penulisannya | 10/12 soal definisi (gagal: D03, D06) |
| Soal error | Soal yang tidak terjawab karena gangguan API atau kuota habis | 0 |
| Jawaban dengan peringatan | Chatbot mencatat kejadian seperti respons kosong yang diulang, nama alat ditolak server, atau jawaban tanpa rujukan. Bukan berarti jawabannya salah | 21 dari 44 |

### B. Metrik pencarian dokumen (43 soal)

Satu **potongan bukti** adalah potongan Buku atau PPT yang memuat semua kata kunci bukti untuk soal itu. D12 (di luar cakupan) tidak punya bukti, jadi dihitung terpisah.

| Metrik | Artinya | Hasil |
|---|---|---|
| Hit@1 | Potongan bukti ada di urutan pertama | 30/43 (69,8%) |
| Hit@3 | Potongan bukti ada di 3 urutan teratas | 39/43 (90,7%) |
| **Hit@5** | Potongan bukti ada di 5 urutan teratas. **Yang terpenting**, karena 5 potongan inilah yang dibaca AI | **41/43 (95,3%)** |
| MRR@5 | Rata-rata ketepatan urutan: 1 jika bukti selalu urutan pertama, 0,5 jika urutan kedua, dan seterusnya | 0,806 |
| Hit@5 gabungan | Semua kata kunci terpenuhi oleh gabungan 5 potongan, untuk bukti yang tersebar di beberapa potongan (mis. tabel panjang) | 42/43 (97,7%) |
| Halaman sitasi benar | Dari potongan bukti Buku yang ditemukan, halamannya sama dengan halaman kunci | 40/41 |
| Hasil urutan 1 dari PPT | Hasil teratas berasal dari PPT, bukan Buku. Lebih sedikit lebih baik (Buku adalah sumber utama) | 1/43 |
| Di luar cakupan lolos | Untuk soal di luar cakupan: jarak hasil teratas minimal 0,45, sehingga bisa dikenali tanpa bantuan AI | 0/1 (D12) |
| Jarak hasil teratas (d#1) | Seberapa jauh pertanyaan dari potongan teratas (0 = identik, makin kecil makin mirip). Soal bahasa santai dan salah ketik berjarak lebih besar dari soal biasa | per soal di laporan asli |

**Status per soal:** "Urutan n" berarti bukti ada di urutan ke-n; "Tidak masuk 5 teratas" berarti bukti tidak terambil; "Tidak dikenali" berarti pencarian tidak mengenali soal di luar cakupan.

## 3. Hasil per soal

| ID | Kelompok | Soal | Pencarian: bukti | Jawaban | Catatan |
|---|---|---|---|---|---|
| D01 | Definisi | Apa itu IKU 1? | Urutan 1 | Lulus |  |
| D02 | Definisi | Berapa masa tempuh kurikulum dan AEE ideal untuk program Sarja... | Urutan 1 | Lulus |  |
| D03 | Definisi | Berapa jumlah IKU wajib, IKU pilihan, dan IKU partisipatif? | Urutan 1 | Gagal | Isi benar, tetapi AI menulis rujukan [*1*] sehingga halaman sitasi tidak muncul; catatan IKU 6 wajib bagi PTN-BH tidak disebut |
| D04 | Definisi | Sebutkan IKU yang bersifat wajib. | Urutan 1 | Lulus | Sebelumnya gagal: tabel IKU wajib terpotong dua. Sekarang disambung saat pencarian |
| D05 | Definisi | Dari mana data IKU 2 diperoleh, dan bagaimana menentukan jumla... | Urutan 1 | Lulus |  |
| D06 | Definisi | Kegiatan di luar program studi apa saja yang diakui untuk IKU ... | Urutan 1 | Gagal | Semua jenis kegiatan disebut, tetapi syarat didampingi dosen pembimbing tidak disebut |
| D07 | Definisi | SDG apa saja yang wajib dan pilihan dalam IKU 7? | Urutan 1 | Lulus |  |
| D08 | Definisi | Pendapatan apa saja yang tidak termasuk dalam perhitungan IKU ... | Urutan 1 | Lulus |  |
| D09 | Definisi | Penerbit apa yang tidak diperhitungkan dalam IKU 6? | Urutan 1 | Lulus |  |
| D10 | Definisi | Bagaimana arah penilaian IKU 11c (pelanggaran integritas akade... | Urutan 2 | Lulus |  |
| D11 | Definisi | Lulusan 400, yang bekerja 280, berapa capaian IKU 1? | Tidak masuk 5 teratas | Lulus | Pencarian tidak menemukan bukti IKU 2, tetapi AI sudah meluruskan berkat daftar nama IKU di instruksi |
| D12 | Definisi | Berapa besaran UKT di Universitas Gadjah Mada tahun 2026? | Tidak dikenali (di luar cakupan) | Lulus | Pencarian tidak mengenali soal di luar cakupan; AI menolak menjawab dengan benar |
| H01 | Hitungan | Prodi S1 memiliki 200 mahasiswa dalam satu tahun akademik. Seb... | Urutan 1 | Lulus |  |
| H02 | Hitungan | Sebuah PT memiliki 3 program pendidikan: D3 dengan AEE realisa... | Urutan 1 | Lulus |  |
| H03 | Hitungan | Prodi S1 mencatat 250 mahasiswa pada satu tahun akademik, term... | Urutan 1 | Lulus |  |
| H04 | Hitungan | Tracer study mengumpulkan 400 responden lulusan S1. Sebanyak 2... | Urutan 1 | Lulus |  |
| H05 | Hitungan | Tracer study mengumpulkan 500 responden lulusan. Rinciannya: -... | Tidak masuk 5 teratas | Lulus | Kata kunci uji hanya ada di slide PPT, sedangkan sistem mendahulukan Buku; jawaban tetap benar |
| H06 | Hitungan | Jumlah lulusan suatu PT adalah 2.000 orang. Berapa jumlah resp... | Urutan 2 | Lulus |  |
| H07 | Hitungan | Sebuah PT memiliki 1.000 mahasiswa S1/Diploma. Rinciannya: - 1... | Urutan 1 | Lulus |  |
| H08 | Hitungan | Dari 500 mahasiswa, prestasi yang tercatat adalah 2 juara 1 in... | Urutan 1 | Lulus |  |
| H09 | Hitungan | PT memiliki 120 kerja sama. Dari kerja sama itu dihasilkan 30 ... | Urutan 2 | Lulus |  |
| H10 | Hitungan | Total publikasi PT dalam satu periode adalah 200, terdiri atas... | Urutan 1 | Lulus |  |
| H11 | Hitungan | Total publikasi 20, terdiri atas 4 artikel Q1 hasil kolaborasi... | Urutan 1 | Lulus |  |
| H12 | Hitungan | Dari 60 program SDGs PT, 45 program berkontribusi pada SDG 1, ... | Urutan 1 | Lulus |  |
| H13 | Hitungan | Total pendapatan PT dalam satu tahun anggaran adalah Rp500 mil... | Urutan 1 | Lulus |  |
| H14 | Hitungan | PT memiliki 300 dosen dalam satu tahun terakhir; 45 dosen ber-... | Urutan 1 | Lulus |  |
| H15 | Hitungan | Dari 400 SDM PT (dosen/peneliti), 12 orang terlibat langsung d... | Urutan 3 | Lulus |  |
| H16 | Hitungan | Nilai akhir evaluasi SAKIP sebuah PT adalah 82. Apa predikatny... | Urutan 1 | Lulus |  |
| H17 | Hitungan | PT merencanakan 24 kegiatan pencegahan dan penanganan kekerasa... | Urutan 1 | Lulus |  |
| H18 | Hitungan | UMP di provinsi tempat PT berada adalah Rp3.000.000. Berapa pe... | Urutan 1 | Lulus |  |
| D13 | Ketahanan | aee tu apaan sih? ngukur apa? | Urutan 3 | Lulus | Bahasa santai: bukti di urutan 3 |
| D14 | Ketahanan | pendptan apa aj yg ga diitung di iku9? | Urutan 4 | Lulus | Salah ketik: bukti di urutan 4 |
| H19 | Ketahanan | brp aee s1 klo yg lulus tepat wktu cm 40 org dr 200 mhs? | Urutan 2 | Lulus |  |
| H20 | Ketahanan | realisasi aee kampus kmi: D3 30%, S1 22,5%, S2 40%. aee pt nya... | Urutan 1 | Lulus |  |
| H21 | Ketahanan | lulusan kampus kami 1.341 org, minimal responden tracer study ... | Urutan 2 | Lulus |  |
| H22 | Ketahanan | klo lulusannya 2rb orang, responden minimum tracer studi brp | Urutan 2 | Lulus |  |
| H23 | Ketahanan | kerjsama PT kita ada 120, luaran nya 30 judul. capaian iku5 br... | Urutan 1 | Lulus |  |
| H24 | Ketahanan | dr 50 progam sdgs, 25 yg kontribusi ke sdg 1,4,17 + 2 sdg pili... | Urutan 4 | Lulus | Bahasa santai: bukti di urutan 4 |
| H25 | Ketahanan | total pendapatan PT 500 M. rinciannya ukt 300M, boptn 80 M, hi... | Urutan 2 | Lulus |  |
| H26 | Ketahanan | pendapatan total Rp1.250.000.000, terdiri dr ukt rp 900jt, kon... | Urutan 1 | Lulus |  |
| H27 | Ketahanan | total pendapatan 2 milyar: hibah riset 300 jt, konsultasi 0,2 ... | Urutan 1 | Lulus | Sebelumnya gagal: "0,2 M" dibaca 0,2 juta. Sekarang konversi dikerjakan kalkulator |
| H28 | Ketahanan | ump disini 3,5jt, penghasilan minimal dosen lektor kepala brp? | Urutan 1 | Gagal | BUG: "Rp3,500,000" terbaca Rp3.500; kalkulator Rp14.000, tetapi jawaban menulis Rp14.000.000 |
| H29 | Ketahanan | UMP prov kami Rp 4.250.000 , brp penghasilan min dosen asisten... | Urutan 1 | Lulus |  |
| H30 | Ketahanan | dosen kami 250 org setahun terakhir, yg ber-NUPTK & dpt rekogn... | Urutan 1 | Lulus |  |

## 4. Kendala

1. **Model gratis tidak stabil.** AI sering salah ketik nama alat (15 kali) dan mengirim respons kosong (14 kali) dalam satu run. Semuanya diulang otomatis, tetapi memakan waktu dan token.
2. **Kuota terbatas.** Sekitar 28 soal per hari per akun (200.000 token) dan 8.000 token per menit, jadi satu evaluasi penuh perlu beberapa akun atau hari. Data di paket gratis dapat dipakai penyedia, jadi data internal kampus tidak boleh dimasukkan.
3. **Bug nominal uang (H28).** Format "Rp3,500,000" dibaca salah, dan peringatan bawaan chatbot belum menangkap jawaban yang berbeda dari kalkulator.
4. **Format jawaban belum rapi.** Rumus LaTeX kadang masih muncul, dan rujukan kadang salah bentuk ("[*1*]").
5. **Pencarian untuk bahasa santai dan salah ketik** menaruh bukti di urutan 3-4, masih di 5 teratas. Reranker diuji dan tidak dipakai (Hit@5 turun 41 ke 40, waktu 0,05 ke 15,7 detik per pertanyaan).
6. **Soal uji belum independen.** Ke-44 soal sudah dipakai untuk menyetel sistem, jadi skor 93% cenderung lebih tinggi dari performa nyata. Perlu 10-15 soal baru dari pengguna nyata.
7. **Belum tercakup:** 12 rumus sub-indikator, pembatasan topik per halaman dasbor, dan ingatan percakapan.

## 5. Langkah berikutnya

- Perbaiki pembacaan nominal "Rp3,500,000", perketat peringatan jawaban-vs-kalkulator, dan perbaiki rujukan "[*1*]"; uji ulang H28, D03, D06.
- Buat layanan FastAPI untuk tim Backend, lengkap dengan pembatasan topik per halaman.
- Minta keputusan PO: demo terbatas, anggaran model berbayar (RAB), sumber yang dipegang bila Buku dan PPT berbeda (7 IKU wajib di Buku, 6 di PPT hlm. 44), dan soal uji independen.
- Ulangi evaluasi penuh setiap kali model, prompt, atau data berubah.
