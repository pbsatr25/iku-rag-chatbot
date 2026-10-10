# Uji Jawaban Chatbot (retriever + LLM + kalkulator)

- Waktu: 2026-10-10 19:06:04
- Model LLM: `openai/gpt-oss-120b`
- Soal: 44 dari 44 dijalankan (hitungan 30, definisi & jebakan 14)
- Status run: selesai

## Ringkasan

| Metrik | Hasil |
|---|---|
| Lulus semua pemeriksaan otomatis | **41/44** |
| Hitungan: kalkulator dipanggil | 30/30 |
| Hitungan: hasil kalkulator = kunci | 29/30 |
| Hitungan: angka kunci ada di jawaban | 30/30 |
| Halaman sitasi benar (hitungan) | 30/30 |
| Halaman sitasi benar (definisi) | 12/13 |
| Soal error (API/kuota) | 0 |
| Jawaban dengan peringatan chatbot | 21 |

| ID | Status | Pemeriksaan yang gagal |
|---|---|---|
| D01 | ✅ | - |
| D02 | ✅ | - |
| D03 | ❌ | halaman sitasi benar |
| D04 | ✅ | - |
| D05 | ✅ | - |
| D06 | ❌ | fakta: dosen pembimbing / pendampingan |
| D07 | ✅ | - |
| D08 | ✅ | - |
| D09 | ✅ | - |
| D10 | ✅ | - |
| D11 | ✅ | - |
| D12 | ✅ | - |
| H01 | ✅ | - |
| H02 | ✅ | - |
| H03 | ✅ | - |
| H04 | ✅ | - |
| H05 | ✅ | - |
| H06 | ✅ | - |
| H07 | ✅ | - |
| H08 | ✅ | - |
| H09 | ✅ | - |
| H10 | ✅ | - |
| H11 | ✅ | - |
| H12 | ✅ | - |
| H13 | ✅ | - |
| H14 | ✅ | - |
| H15 | ✅ | - |
| H16 | ✅ | - |
| H17 | ✅ | - |
| H18 | ✅ | - |
| D13 | ✅ | - |
| D14 | ✅ | - |
| H19 | ✅ | - |
| H20 | ✅ | - |
| H21 | ✅ | - |
| H22 | ✅ | - |
| H23 | ✅ | - |
| H24 | ✅ | - |
| H25 | ✅ | - |
| H26 | ✅ | - |
| H27 | ✅ | - |
| H28 | ❌ | hasil kalkulator = kunci |
| H29 | ✅ | - |
| H30 | ✅ | - |

Pemeriksaan otomatis hanya bantuan. Baca jawaban lengkap di bawah dan bandingkan dengan jawaban yang diharapkan.

## Detail per soal

### D01 — ✅ LULUS

**Pertanyaan:** Apa itu IKU 1?

**Jawaban chatbot:**

```text
IKU 1 – Angka Efisiensi Edukasi Perguruan Tinggi (AEE PT) adalah indikator yang mengukur tingkat keberhasilan mahasiswa menyelesaikan studi tepat waktu sesuai masa studi standar, dibandingkan dengan total mahasiswa yang masuk pada periode tertentu. AEE PT dihitung dari rata-rata pencapaian AEE masing-masing program pendidikan (misalnya D3, D4, S1, S2, S3) di perguruan tinggi [1].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Definisi); juga di PPT hlm. 45

**Jawaban yang diharapkan:**

- Halaman kunci: 49

IKU 1 adalah **Angka Efisiensi Edukasi (AEE) Perguruan Tinggi**, yaitu indikator yang mengukur tingkat keberhasilan mahasiswa menyelesaikan studi **tepat waktu** sesuai masa studi standar, dibandingkan dengan total mahasiswa yang masuk pada periode tertentu. AEE PT dihitung dari **rata-rata tingkat pencapaian AEE setiap program pendidikan**. Sifatnya **IKU Wajib**.

**Pemeriksaan otomatis:**

- ✅ fakta: tepat waktu
- ✅ fakta: efisiensi edukasi / AEE
- ✅ halaman sitasi benar

### D02 — ✅ LULUS

**Pertanyaan:** Berapa masa tempuh kurikulum dan AEE ideal untuk program Sarjana dan Diploma Tiga?

**Jawaban chatbot:**

```text
- **Program Diploma Tiga (D3)**  
  - Masa tempuh kurikulum: **6 semester**[1]  
  - AEE ideal: **33 %**[1]

- **Program Sarjana (S1/Sarjana Terapan)**  
  - Masa tempuh kurikulum: **8 semester**[1]  
  - AEE ideal: **25 %**[1]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 100–101; PPT hlm. 45

**Jawaban yang diharapkan:**

- Halaman kunci: 49

- Sarjana / Sarjana Terapan (D4): masa tempuh **8 semester**, AEE ideal **25%**.
- Diploma Tiga: masa tempuh **6 semester**, AEE ideal **33%**.

**Pemeriksaan otomatis:**

- ✅ fakta: 8 semester / delapan semester
- ✅ fakta: 25% / 25 %
- ✅ fakta: 6 semester / enam semester
- ✅ fakta: 33% / 33 %
- ✅ halaman sitasi benar

### D03 — ❌ PERLU DICEK

**Pertanyaan:** Berapa jumlah IKU wajib, IKU pilihan, dan IKU partisipatif?

**Jawaban chatbot:**

```text
Berdasarkan dokumen IKU:

- **IKU wajib**: sebanyak **7 (tujuh)** indikator [*1*]  
- **IKU pilihan**: terdapat **5 (lima)** indikator, dari mana tiap PT dapat memilih **2 (dua)** [*1*]  
- **IKU partisipatif**: masing-masing PT harus mengusulkan **1 (satu)** IKU [*1*]
```

**Peringatan chatbot:**

- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Halaman kunci: 48

- **7 IKU wajib** bagi seluruh perguruan tinggi.
- **5 IKU pilihan**; PT memilih **2** dari 5.
- PT harus mengusulkan **1 IKU partisipatif**.
- Catatan: IKU 6 (publikasi Scopus/WoS) **wajib bagi PTN-BH**.

**Pemeriksaan otomatis:**

- ✅ fakta: 7 (tujuh) / tujuh / 7 IKU / 7 indikator / sebanyak 7
- ✅ fakta: 5 (lima) / lima / 5 IKU / 5 indikator
- ✅ fakta: 2 (dua) / dua / memilih 2
- ✅ fakta: partisipatif
- ❌ halaman sitasi benar

### D04 — ✅ LULUS

**Pertanyaan:** Sebutkan IKU yang bersifat wajib.

**Jawaban chatbot:**

```text
Berikut adalah indikator kinerja utama (IKU) yang bersifat **wajib** bagi seluruh perguruan tinggi (ditandai dengan (*) pada tabel):

1. **IKU 1 – Angka Efisiensi Edukasi Perguruan Tinggi** [1][2]  
2. **IKU 2 – Persentase lulusan pendidikan tinggi & vokasi yang langsung bekerja/melanjutkan jenjang pendidikan berikutnya dalam jangka waktu 1 tahun setelah kelulusan** [1]  
3. **IKU 3 – Persentase mahasiswa S1/D4/D3/D2/D1 berkegiatan/meraih prestasi di luar program studi** [1][3]  
4. **IKU 5 – Rasio luaran hasil kerja sama antara PT dan start-up/industri/Lembaga** [1][4]  
5. **IKU 7 – Persentase keterlibatan Perguruan Tinggi dalam SDG 1 (Tanpa Kemiskinan), SDG 4 (Pendidikan Berkualitas), SDG 17 (Kemitraan) dan 2 SDGs lain sesuai keunggulan** [1][5]  
6. **IKU 9 – Persentase Pendapatan Non Pendidikan/UKT** [1]  
7. **IKU 12 – Ketersediaan perencanaan strategis peningkatan kesejahteraan dosen** [1]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 48–49
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Definisi); juga di PPT hlm. 45
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Definisi); juga di PPT hlm. 49
- [4] Buku IKU Diktisaintek Berdampak V1, hlm. 55 (IKU 5, Definisi); juga di PPT hlm. 51
- [5] Buku IKU Diktisaintek Berdampak V1, hlm. 58 (IKU 7, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 120–121

**Jawaban yang diharapkan:**

- Halaman kunci: 48

IKU 1 (AEE), IKU 2 (lulusan bekerja/studi lanjut/wirausaha dalam 1 tahun), IKU 3 (mahasiswa berkegiatan/berprestasi di luar prodi), IKU 5 (rasio luaran kerja sama), IKU 7 (keterlibatan SDGs), IKU 9 (pendapatan non-UKT), dan IKU 12 (perencanaan kesejahteraan dosen).

**Pemeriksaan otomatis:**

- ✅ fakta: efisiensi edukasi / IKU 1
- ✅ fakta: lulusan / IKU 2
- ✅ fakta: di luar program studi / IKU 3
- ✅ fakta: kerja sama / kerjasama / IKU 5
- ✅ fakta: SDG / IKU 7
- ✅ fakta: non pendidikan / non-pendidikan / UKT / IKU 9
- ✅ fakta: kesejahteraan dosen / IKU 12
- ✅ halaman sitasi benar

### D05 — ✅ LULUS

**Pertanyaan:** Dari mana data IKU 2 diperoleh, dan bagaimana menentukan jumlah responden minimum?

**Jawaban chatbot:**

```text
Data untuk **IKU 2** diambil melalui **tracer study** yang dilakukan **1 tahun setelah kelulusan** untuk mengetahui status kerja, wirausaha, atau melanjutkan studi para lulusan [1]​.  

Jumlah responden minimum ditentukan dengan menggunakan **rumus Slovin** dengan galat 2,3 % sebagaimana tercantum dalam bagian Formula [2]​. Rumusnya:  

```
n = N / (N·d² + 1) × 100%
```

di mana  
- **N** = jumlah total lulusan (D1, D2, D3, D4/Sarjana Terapan, atau Sarjana) yang menjadi populasi,  
- **d** = galat yang ditetapkan, yaitu **2,3 %** (0,023).  

Dengan memasukkan nilai N dan d ke dalam rumus di atas, didapatkan **jumlah responden minimum (n)** yang harus dikumpulkan dalam tracer study agar IKU 2 dapat dihitung secara valid. Karena nilai N tidak disediakan dalam pertanyaan, perhitungan spesifik tidak dapat dilakukan tanpa data tersebut.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 51 (IKU 2, Ketentuan); juga di PPT hlm. 48; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 52 (IKU 2, Formula); juga di PPT hlm. 48–49; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104–105

**Jawaban yang diharapkan:**

- Halaman kunci: 51, 52

Data diperoleh dari **tracer study** yang dilakukan **1 tahun setelah kelulusan**. Responden minimum dihitung dengan **rumus Slovin** dengan **galat (d) 2,3%**: n = N / (N·d² + 1), dengan N = jumlah lulusan.

**Pemeriksaan otomatis:**

- ✅ fakta: tracer study
- ✅ fakta: slovin
- ✅ fakta: 2,3 / 2.3
- ✅ halaman sitasi benar

### D06 — ❌ PERLU DICEK

**Pertanyaan:** Kegiatan di luar program studi apa saja yang diakui untuk IKU 3?

**Jawaban chatbot:**

```text
Kegiatan di luar program studi yang diakui untuk menghitung **IKU 3 – Persentase mahasiswa S1/D4/D3/D2/D1 berkegiatan/meraih prestasi di luar program studi** meliputi:

1. **Magang atau praktik kerja** yang dilakukan pada  
   - perusahaan swasta (nasional, multinasional, startup, UMKM, dll.),  
   - lembaga/organisasi nirlaba,  
   - institusi/organisasi multilateral (mis. PBB, UNICEF), atau  
   - instansi pemerintah, BUMN, atau BUMD[1].  
2. **Program mahasiswa Berdampak** berupa proyek sosial/pengabdian kepada masyarakat untuk pemberdayaan di daerah bencana, pedesaan, atau terpencil (mis. pembangunan ekonomi, infrastruktur, dll.)[1].  
3. **Pertukaran mahasiswa** yang melibatkan mengambil kelas atau semester di perguruan tinggi lain (dalam negeri atau luar negeri) berdasarkan perjanjian kerja sama yang sudah ada, dengan pengakuan kredit semester[1].  
4. **Penelitian atau riset** yang dilakukan di bawah bimbingan dosen atau peneliti, baik di bidang sains maupun sosial-humaniora[1].  

Selain itu, kegiatan-kegiatan tersebut dapat **dikombinasikan dan dihitung secara kumulatif** dalam perhitungan IKU 3[2].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 105–106; PPT hlm. 49
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 106–107; PPT hlm. 49; PPT hlm. 50

**Jawaban yang diharapkan:**

- Halaman kunci: 53

Kegiatan harus didampingi dosen pembimbing dan mendapat pengakuan SKS, berupa:
1. magang/praktik kerja (swasta, nirlaba, organisasi multilateral, pemerintah/BUMN/BUMD);
2. program mahasiswa berdampak (sosial/pengabdian masyarakat);
3. pertukaran mahasiswa (dalam/luar negeri, berdasarkan perjanjian kerja sama); dan/atau
4. penelitian/riset di bawah pengawasan dosen atau peneliti.

Prestasi diakui bila berupa kompetisi tingkat provinsi/nasional/internasional, minimal sebagai finalis.
Catatan: magang **tidak dihitung** bagi prodi vokasi yang sudah memiliki magang wajib.

**Pemeriksaan otomatis:**

- ✅ fakta: magang / praktik kerja
- ✅ fakta: pertukaran
- ✅ fakta: penelitian / riset
- ❌ fakta: dosen pembimbing / pendampingan
- ✅ halaman sitasi benar

### D07 — ✅ LULUS

**Pertanyaan:** SDG apa saja yang wajib dan pilihan dalam IKU 7?

**Jawaban chatbot:**

```text
Pada IKU 7 terdapat tiga SDG yang **wajib** dilakukan oleh perguruan tinggi, yaitu:

- **SDG 1 – No Poverty (Tanpa Kemiskinan)**
- **SDG 4 – Quality Education (Pendidikan Berkualitas)**
- **SDG 17 – Partnerships for the Goals (Kemitraan)**[1]  

Selain itu, perguruan tinggi wajib **memilih dua (2) SDG lain** di luar ketiga SDG wajib tersebut, yang disesuaikan dengan keunggulan, spesialisasi, atau konteks strategis masing-masing institusi. Pilihan dua SDG ini harus dituangkan dalam dokumen resmi (misalnya Renstra atau laporan kinerja tahunan)[1].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 58 (IKU 7, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 120–121

**Jawaban yang diharapkan:**

- Halaman kunci: 58

SDG wajib: **SDG 1** (Tanpa Kemiskinan), **SDG 4** (Pendidikan Berkualitas), dan **SDG 17** (Kemitraan). Ditambah **2 SDG pilihan** di luar ketiganya, sesuai keunggulan PT, dan harus dituangkan dalam dokumen resmi (Renstra atau laporan kinerja tahunan).

**Pemeriksaan otomatis:**

- ✅ fakta: SDG 1 / SDG1
- ✅ fakta: SDG 4 / SDG4
- ✅ fakta: SDG 17 / SDG17
- ✅ fakta: 2 (dua) / dua (2) / dua SDG / 2 SDG / dua tujuan / 2 tujuan
- ✅ halaman sitasi benar

### D08 — ✅ LULUS

**Pertanyaan:** Pendapatan apa saja yang tidak termasuk dalam perhitungan IKU 9?

**Jawaban chatbot:**

```text
Pendapatan yang **tidak termasuk** dalam perhitungan IKU 9 (Persentase Pendapatan Non Pendidikan/UKT) meliputi:

1. **SPP/UKT/biaya kuliah mahasiswa**.  
2. **Iuran pengembangan institusi**.  
3. **Subsidi langsung dari pemerintah**, seperti belanja pegawai, belanja operasional, BOPTN, BPPTNBH, dan sejenisnya.  
4. **Sumbangan/filantropi yang tidak masuk laporan keuangan resmi perguruan tinggi**.  
5. **Dana pokok dana abadi/endowment fund** yang disimpan permanen dan tidak dibelanjakan.  
6. **Pendapatan yang tidak dibukukan**, hibah barang tanpa nilai, atau dana yang mengalir lewat kampus tanpa pelaporan resmi.  

Sumber: kriteria tidak termasuk pada IKU 9 [1]; tambahan pengecualian pada kriteria dan ketentuan sub-indikator IKU 9 [5].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 59 (IKU 9, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 122–123; PPT hlm. 56
- [5] Buku IKU Diktisaintek Berdampak V1, hlm. 79 (IKU 9, Kriteria dan Ketentuan); juga di PPT hlm. 81; PPT hlm. 85; PPT hlm. 86

**Jawaban yang diharapkan:**

- Halaman kunci: 59

1. SPP/UKT/biaya kuliah mahasiswa;
2. iuran pengembangan institusi;
3. subsidi langsung pemerintah (belanja pegawai, operasional, BOPTN, BPPTNBH, dan sejenisnya);
4. sumbangan/filantropi yang tidak masuk laporan keuangan resmi; dan
5. dana pokok dana abadi (*endowment fund*).

**Pemeriksaan otomatis:**

- ✅ fakta: UKT / SPP
- ✅ fakta: BOPTN
- ✅ fakta: iuran pengembangan
- ✅ fakta: dana abadi / endowment
- ✅ halaman sitasi benar

### D09 — ✅ LULUS

**Pertanyaan:** Penerbit apa yang tidak diperhitungkan dalam IKU 6?

**Jawaban chatbot:**

```text
Penerbit yang **tidak** diperhitungkan dalam perhitungan IKU 6 adalah **MDPI, Frontiers, dan Hindawi Publisher**[1].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 63 (IKU 6, Ketentuan); juga di PPT hlm. 61–62; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 118–119

**Jawaban yang diharapkan:**

- Halaman kunci: 63

**MDPI, Frontiers, dan Hindawi**.

**Pemeriksaan otomatis:**

- ✅ fakta: MDPI
- ✅ fakta: Frontiers
- ✅ fakta: Hindawi
- ✅ halaman sitasi benar

### D10 — ✅ LULUS

**Pertanyaan:** Bagaimana arah penilaian IKU 11c (pelanggaran integritas akademik)?

**Jawaban chatbot:**

```text
Arah penilaian IKU 11c (Jumlah Laporan Pelanggaran Integritas Akademik) bersifat “semakin rendah semakin baik”. Nilai 0 (nol) dapat mencerminkan kinerja yang baik, asalkan perguruan tinggi sudah memiliki dan menjalankan mekanisme pencegahan, pelaporan, verifikasi, dan penanganan pelanggaran integritas akademik secara institusional[2][5].
```

**Sitasi chatbot:**

- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 67 (IKU 11c, Ketentuan)
- [5] PPT IKU Diktisaintek Berdampak PTS V2, hlm. 67 (IKU 11, Ketentuan); juga di PPT hlm. 69; PPT hlm. 66; PPT hlm. 65–66

**Jawaban yang diharapkan:**

- Halaman kunci: 67

**Semakin rendah semakin baik.** Nilai 0 laporan mencerminkan kinerja baik, **asalkan** PT memiliki dan menjalankan mekanisme pencegahan, pelaporan, verifikasi, dan penanganan pelanggaran integritas akademik. Formula: jumlah laporan pelanggaran integritas akademik dalam 1 periode (satuan: laporan).

**Pemeriksaan otomatis:**

- ✅ fakta: semakin rendah
- ✅ halaman sitasi benar

### D11 — ✅ LULUS

**Pertanyaan:** Lulusan 400, yang bekerja 280, berapa capaian IKU 1?

**Jawaban chatbot:**

```text
Data yang diberikan (jumlah lulusan = 400, yang bekerja = 280) tidak sesuai dengan definisi dan rumus IKU 1 – Angka Efisiensi Edukasi Perguruan Tinggi (AEE PT). IKU 1 mengukur persentase mahasiswa yang lulus tepat waktu dibandingkan total mahasiswa pada tahun akademik, bukan persentase lulusan yang bekerja [1][3][4].  

Jika Anda ingin menghitung capaian untuk indikator tersebut, diperlukan data:
- Jumlah mahasiswa yang lulus tepat waktu (sesuai masa tempuh kurikulum) per program pendidikan, dan
- Total mahasiswa yang terdaftar pada tahun akademik yang bersangkutan.

Data yang Anda miliki lebih relevan untuk **IKU 2 – Persentase lulusan pendidikan tinggi & vokasi yang langsung bekerja/melanjutkan jenjang pendidikan berikutnya dalam jangka waktu 1 tahun setelah kelulusan** [5]. Silakan ajukan pertanyaan terkait IKU 2 atau sediakan data yang diperlukan untuk menghitung IKU 1.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49–50 (IKU 1, Formula); juga di PPT hlm. 46–47; PPT hlm. 46; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Ketentuan); juga di PPT hlm. 45; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 100–101
- [4] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Kriteria); juga di PPT hlm. 45
- [5] Buku IKU Diktisaintek Berdampak V1, hlm. 51 (IKU 2, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 103–104; PPT hlm. 47; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 103–104; PPT hlm. 47; PPT hlm. 47; PPT hlm. 47; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 103–104; PPT hlm. 47; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 103–104; PPT hlm. 47; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 103–104; PPT hlm. 48

**Jawaban yang diharapkan:**

- Halaman kunci: 49, 51

Chatbot harus **mengoreksi**: IKU 1 adalah Angka Efisiensi Edukasi (kelulusan tepat waktu), bukan persentase lulusan bekerja. Data lulusan bekerja termasuk **IKU 2**. Jika dihitung sebagai IKU 2, dengan asumsi seluruh 280 lulusan berbobot 1 (masa tunggu < 6 bulan dan gaji > 1,2× UMP) dan 400 adalah total responden tracer study: 280/400 × 100% = **70%** (lihat H04).

*Catatan soal:* Soal jebakan: chatbot harus meluruskan bahwa data lulusan bekerja termasuk IKU 2, bukan IKU 1.

**Pemeriksaan otomatis:**

- ✅ fakta: IKU 2
- ✅ fakta: efisiensi edukasi / tepat waktu / AEE
- ✅ halaman sitasi benar

### D12 — ✅ LULUS

**Pertanyaan:** Berapa besaran UKT di Universitas Gadjah Mada tahun 2026?

**Jawaban chatbot:**

```text
Informasi mengenai besaran UKT di Universitas Gadjah Mada tahun 2026 tidak ditemukan dalam dokumen IKU yang diberikan.
```

**Jawaban yang diharapkan:**

- Halaman kunci: -

Informasi ini **tidak ada** di Buku IKU. Chatbot harus menyatakan tidak menemukan jawabannya di dokumen, bukan mengarang angka.

*Catatan soal:* Soal di luar cakupan: chatbot harus menolak, bukan mengarang angka UKT.

**Pemeriksaan otomatis:**

- ✅ fakta: tidak ditemukan / tidak terdapat / tidak tersedia / tidak ada informasi / tidak dijelaskan / tidak memuat
- ✅ tidak mengarang sitasi

### H01 — ✅ LULUS

**Pertanyaan:** Prodi S1 memiliki 200 mahasiswa dalam satu tahun akademik. Sebanyak 40 mahasiswa lulus tepat 8 semester. Berapa AEE realisasi dan tingkat pencapaian AEE prodi tersebut?

**Jawaban chatbot:**

```text
AEE realisasi prodi S1 = 20 % [1]  
Tingkat pencapaian AEE prodi S1 = 80 % [1]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49–50 (IKU 1, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102; PPT hlm. 46; PPT hlm. 46–47

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 1 – Ketentuan & Formula a–b, hlm. 49

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"jenjang\":\"S1\",\"lulus_tepat_waktu\":40,\"total_mahasiswa\":200,\"pindah\":0,\"drop_out\":0,\"cuti_lebih\":0}","fungsi":"iku1_aee_prodi"}` → aee_realisasi_pct = 20,00, tingkat_pencapaian_pct = 80,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'hit_iku' tidak dikenal); diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **aee_realisasi_pct = 20,00, tingkat_pencapaian_pct = 80,00**
- Halaman kunci: 49

AEE realisasi **20%**, tingkat pencapaian **80%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H02 — ✅ LULUS

**Pertanyaan:** Sebuah PT memiliki 3 program pendidikan: D3 dengan AEE realisasi 30%, S1 dengan 22,5%, dan S2 dengan 40%. Berapa AEE PT?

**Jawaban chatbot:**

```text
AEE PT untuk tiga program tersebut adalah **86,97 %**. Langkah perhitungannya:

- Tingkat pencapaian D3 = 30 % ÷ 33 % = 90,91 %  
- Tingkat pencapaian S1 = 22,5 % ÷ 25 % = 90 %  
- Tingkat pencapaian S2 = 40 % ÷ 50 % = 80 %  

AEE PT = (90,91 % + 90 % + 80 %) ÷ 3 = **86,97 %** [2][1]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49–50 (IKU 1, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102; PPT hlm. 46; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102; PPT hlm. 46–47
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 49–50 (IKU 1, Formula)

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 1 – Formula c & contoh perhitungan, hlm. 49–50

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"realisasi_per_jenjang\": {\"D3\": 30, \"S1\": 22.5, \"S2\": 40}}","fungsi":"iku1_aee_pt"}` → 86,97

**Jawaban yang diharapkan:**

- Angka kunci: **86,97**
- Halaman kunci: 49, 50

**86,97%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H03 — ✅ LULUS

**Pertanyaan:** Prodi S1 mencatat 250 mahasiswa pada satu tahun akademik, termasuk 10 mahasiswa pindah dan 15 mahasiswa *drop out*. Sebanyak 45 mahasiswa lulus tepat 8 semester. Berapa AEE realisasi dan tingkat pencapaiannya?

**Jawaban chatbot:**

```text
AEE realisasi untuk program S1 adalah **20 %** dan tingkat pencapaiannya adalah **80 %**.

Langkah perhitungannya:
- Basis = 250 (total mahasiswa) − 10 (mahasiswa pindah) − 15 (mahasiswa drop out) − 0 (cuti lebih) = **225** mahasiswa.  
- AEE realisasi = 45 ÷ 225 × 100 % = **20 %**.  
- AEE ideal S1 = 25 % (berdasarkan ketentuan masa studi 8 semester).  
- Tingkat pencapaian = 20 % ÷ 25 % × 100 % = **80 %**.  

Sumber: Buku IKU Diktisaintek Berdampak V1, IKU 1 – Ketentuan & Formula a–b, hlm. 49.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 1 – Ketentuan & Formula a–b, hlm. 49

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"jenjang\": \"S1\", \"lulus_tepat_waktu\": 45, \"total_mahasiswa\": 250, \"pindah\": 10, \"drop_out\": 15, \"cuti_lebih\": 0}","fungsi":"iku1_aee_prodi"}` → aee_realisasi_pct = 20,00, tingkat_pencapaian_pct = 80,00

**Peringatan chatbot:**

- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **aee_realisasi_pct = 20,00, tingkat_pencapaian_pct = 80,00**
- Halaman kunci: 49

AEE realisasi **20%**, tingkat pencapaian **80%**. Jawaban 45/250 = 18% **salah**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H04 — ✅ LULUS

**Pertanyaan:** Tracer study mengumpulkan 400 responden lulusan S1. Sebanyak 280 lulusan bekerja dengan masa tunggu < 6 bulan dan gaji > 1,2× UMP; sisanya belum bekerja. Berapa capaian IKU 2?

**Jawaban chatbot:**

```text
Capaian IKU 2 (Persentase lulusan pendidikan tinggi & vokasi yang langsung bekerja/melanjutkan jenjang pendidikan berikutnya dalam jangka waktu 1 tahun setelah kelulusan) adalah **70 %** [5][6]
```

**Sitasi chatbot:**

- [5] Buku IKU Diktisaintek Berdampak V1, hlm. 52 (IKU 2, Formula); juga di PPT hlm. 48–49; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104–105

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 2 – Kriteria b–f & Formula, hlm. 51–52

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_responden\": 400, \"kategori\": {\"bekerja_\u003c6bln_\u003e1.2ump\": 280}}","fungsi":"iku2"}` → 70,00

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.
- Rujukan tidak valid (tidak ada di konteks): [6]

**Jawaban yang diharapkan:**

- Angka kunci: **70,00**
- Halaman kunci: 51, 52

**70%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H05 — ✅ LULUS

**Pertanyaan:** Tracer study mengumpulkan 500 responden lulusan. Rinciannya: - 200 bekerja, masa tunggu < 6 bulan, gaji > 1,2× UMP - 100 bekerja, masa tunggu < 1 tahun, gaji > 1,2× UMP - 50 bekerja, masa tunggu < 1 tahun, gaji < 1,2× UMP - 30 melanjutkan studi (surat penerimaan < 12 bulan) - 20 *founder*, < 6 bulan, penghasilan > 1,2× UMP - 10 *freelancer*, > 6 bulan, penghasilan < 1,2× UMP - 90 belum bekerja/studi/wirausaha Berapa capaian IKU 2?

**Jawaban chatbot:**

```text
Capaian IKU 2 = 70,8 % [5]  

Langkah perhitungan:  
- Bekerja < 6 bulan & gaji > 1,2 × UMP: 200 × 1 = 200  
- Bekerja < 1 tahun & gaji > 1,2 × UMP: 100 × 0,8 = 80  
- Bekerja < 1 tahun & gaji < 1,2 × UMP: 50 × 0,6 = 30  
- Founder < 6 bulan & penghasilan > 1,2 × UMP: 20 × 1,2 = 24  
- Freelancer > 6 bulan & penghasilan < 1,2 × UMP: 10 × 0,2 = 2  
- Melanjutkan studi (< 12 bulan): 30 × 0,6 = 18  

Jumlah Σ(n·k) = 354  

Capaian = 354 ÷ 500 × 100 % = 70,8 %  

(Perhitungan menggunakan fungsi hitung_iku).
```

**Sitasi chatbot:**

- [5] Buku IKU Diktisaintek Berdampak V1, hlm. 52 (IKU 2, Formula); juga di PPT hlm. 48–49; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104–105

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 2 – Kriteria b–f & Formula, hlm. 51–52

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_responden\": 500, \"kategori\": {\"bekerja_\u003c6bln_\u003e1.2ump\": 200, \"bekerja_\u003c1thn_\u003e1.2ump\": 100, \"bekerja_\u003c1thn_\u003c1.2ump\": 50, \"founder_\u003c6bln_\u003e1.2ump\": 20, \"freelancer_\u003e6bln_\u003c1.2ump\": 10, \"studi_lanjut_\u003c12bln\": 30}}","fungsi":"iku2"}` → 70,80

**Jawaban yang diharapkan:**

- Angka kunci: **70,80**
- Halaman kunci: 51, 52

**70,8%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H06 — ✅ LULUS

**Pertanyaan:** Jumlah lulusan suatu PT adalah 2.000 orang. Berapa jumlah responden minimum tracer study untuk IKU 2?

**Jawaban chatbot:**

```text
Berdasarkan rumus Slovin dengan galat 2,3 % (d = 0,023), jumlah responden minimum untuk tracer study IKU 2 dengan total lulusan 2 000 orang adalah **972 responden**.  

Langkah perhitungannya:  
1. Hitung N·d² = 2 000 × 0,023² = 1,06.  
2. n = N ÷ (N·d² + 1) = 2 000 ÷ (1,06 + 1) = 971,82.  
3. Dibulatkan ke atas menjadi 972 responden.  

Sumber: Buku IKU Diktisaintek Berdampak V1, IKU 2 – Formula Responden Minimum, hlm. 52.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 2 – Formula Responden Minimum, hlm. 52

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"jumlah_lulusan\": 2000}","fungsi":"iku2_responden_minimum"}` → 972

**Peringatan chatbot:**

- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **972**
- Halaman kunci: 52

**972 responden**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H07 — ✅ LULUS

**Pertanyaan:** Sebuah PT memiliki 1.000 mahasiswa S1/Diploma. Rinciannya: - 100 mahasiswa magang 20 SKS - 150 mahasiswa pertukaran 8 SKS - 50 mahasiswa riset 4 SKS - 5 mahasiswa juara 1 lomba nasional - 10 mahasiswa finalis lomba internasional Berapa capaian IKU 3?

**Jawaban chatbot:**

```text
Capaian IKU 3 = 21,5 % [1][2][3]

Langkah perhitungan (menggunakan alat hitung_iku):
- Kegiatan 20 SKS (magang): 100 × 1 = 100  
- Kegiatan 8 SKS (pertukaran): 150 × 0,6 = 90  
- Kegiatan 4 SKS (riset): 50 × 0,4 = 20  
- Prestasi juara 1 lomba nasional: 5 × 0,6 = 3  
- Prestasi finalis lomba internasional: 10 × 0,2 = 2  
- Σ (nᵢ × kᵢ) = 215  
- Capaian = 215 ÷ 1000 × 100 % = 21,5 %  

Jadi persentase mahasiswa S1/Diploma yang berkegiatan atau meraih prestasi di luar program studi adalah **21,5 %**.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 53–54 (IKU 3, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 107–108; PPT hlm. 50
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 106–107; PPT hlm. 50; PPT hlm. 49
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 105–106; PPT hlm. 49

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 3 – Formula & Ketentuan Bobot, hlm. 53–54

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_mahasiswa\":1000,\"kegiatan\":[{\"jumlah\":100,\"sks\":20},{\"jumlah\":150,\"sks\":8},{\"jumlah\":50,\"sks\":4}],\"prestasi\":[{\"jumlah\":5,\"tingkat\":\"nasional\",\"peringkat\":\"juara1\"},{\"jumlah\":10,\"tingkat\":\"internasional\",\"peringkat\":\"finalis\"}]}","fungsi":"iku3"}` → 21,50

**Jawaban yang diharapkan:**

- Angka kunci: **21,50**
- Halaman kunci: 53, 54

**21,5%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H08 — ✅ LULUS

**Pertanyaan:** Dari 500 mahasiswa, prestasi yang tercatat adalah 2 juara 1 internasional, 4 juara 2 tingkat provinsi, dan 20 finalis tingkat provinsi. Tidak ada kegiatan SKS di luar prodi. Berapa capaian IKU 3?

**Jawaban chatbot:**

```text
Capaian IKU 3 = 0,76 % [1][2][3] 

Langkah perhitungan (diperoleh dari fungsi hitung_iku):
- Prestasi juara 1 internasional: 2 × 1 = 2  
- Prestasi juara 2 (provinsi): 4 × 0,2 = 0,8  
- Prestasi finalis (provinsi): 20 × 0,05 = 1  
- Σ(n·k) = 3,8  
- Capaian = 3,8 ÷ 500 × 100 % = 0,76 % 

Tidak ada kegiatan pembelajaran SKS di luar program studi, sehingga hanya bobot prestasi yang dihitung.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 53–54 (IKU 3, Formula); juga di PPT hlm. 50; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 107–108
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 105–106; PPT hlm. 49
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 53 (IKU 3, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 106–107; PPT hlm. 50; PPT hlm. 49

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 3 – Formula & Ketentuan Bobot, hlm. 53–54

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_mahasiswa\": 500, \"kegiatan\": [], \"prestasi\": [{\"jumlah\": 2, \"tingkat\": \"internasional\", \"peringkat\": \"juara1\"}, {\"jumlah\": 4, \"tingkat\": \"provinsi\", \"peringkat\": \"juara2\"}, {\"jumlah\": 20, \"tingkat\": \"provinsi\", \"peringkat\": \"finalis\"}]}","fungsi":"iku3"}` → ValueError: Prestasi (tingkat, peringkat) ('provinsi', 'juara2') tidak dikenal. Pilihan: ('internasional', 'juara1'), ('internasional', 'juara2_3_favorit'), ('internasional', 'harapan'), ('internasional', 'finalis'), ('nasional', 'juara1'), ('nasional', 'juara2_3_favorit'), ('nasional', 'harapan'), ('nasional', 'finalis'), ('provinsi', 'juara1'), ('provinsi', 'juara2_3_favorit'), ('provinsi', 'harapan'), ('provinsi', 'finalis'). Periksa nama fungsi dan format argumen.
- argumen `{"argumen_json":"{\"total_mahasiswa\": 500, \"kegiatan\": [], \"prestasi\": [{\"jumlah\": 2, \"tingkat\": \"internasional\", \"peringkat\": \"juara1\"}, {\"jumlah\": 4, \"tingkat\": \"provinsi\", \"peringkat\": \"juara2_3_favorit\"}, {\"jumlah\": 20, \"tingkat\": \"provinsi\", \"peringkat\": \"finalis\"}]}","fungsi":"iku3"}` → 0,76

**Jawaban yang diharapkan:**

- Angka kunci: **0,76**
- Halaman kunci: 54

**0,76%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H09 — ✅ LULUS

**Pertanyaan:** PT memiliki 120 kerja sama. Dari kerja sama itu dihasilkan 30 karya (judul) yang telah dimanfaatkan oleh mitra, melibatkan total 90 dosen. Berapa capaian IKU 5?

**Jawaban chatbot:**

```text
Capaian IKU 5 dihitung dengan rumus:

( Jumlah luaran hasil kerja sama ) ÷ ( Total kerja sama PT ) × 100%  
= 30 ÷ 120 × 100% = **25 %**.

Langkah perhitungan dan hasilnya sesuai alat hitung_iku: 25 % [2].
```

**Sitasi chatbot:**

- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 57–58 (IKU 5, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 117; PPT hlm. 53

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 5 – Formula & Keterangan, hlm. 57

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\":\"iku5\",\"pembilang\":30,\"penyebut\":120}","fungsi":"rasio"}` → 25,00

**Jawaban yang diharapkan:**

- Angka kunci: **25,00**
- Halaman kunci: 57

**25%**. Yang dihitung adalah **jumlah judul/karya, bukan jumlah dosen**, sehingga angka 90 tidak dipakai.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H10 — ✅ LULUS

**Pertanyaan:** Total publikasi PT dalam satu periode adalah 200, terdiri atas 10 jurnal Top Tier, 40 Q1, 50 Q2, 30 Q3, 20 Q4, dan 50 publikasi tidak terindeks Scopus/WoS. Berapa capaian IKU 6?

**Jawaban chatbot:**

```text
Capaian IKU 6 dihitung dengan menjumlahkan bobot tiap publikasi yang terindeks, kemudian dibagi total publikasi dan dikalikan 100 %[3].  

Langkah perhitungan:
- Top Tier: 10 × 1,2 = 12  
- Q1: 40 × 1,00 = 40  
- Q2: 50 × 0,75 = 37,5  
- Q3: 30 × 0,50 = 15  
- Q4: 20 × 0,25 = 5  

Jumlah Σ(n·k) = 12 + 40 + 37,5 + 15 + 5 = **109,5**.  

Capaian = 109,5 ÷ 200 × 100 % = **54,75 %**[3].
```

**Sitasi chatbot:**

- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 63 (IKU 6, Formula); juga di PPT hlm. 62; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 119

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 6 – Kriteria (bobot kuartil) & Formula, hlm. 63

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_publikasi\": 200, \"publikasi\": {\"top_tier\": 10, \"q1\": 40, \"q2\": 50, \"q3\": 30, \"q4\": 20}, \"kolaborasi\": {}}","fungsi":"iku6"}` → 54,75

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.
- Panggilan alat ditolak server (nama alat 'hitungan_iku' tidak dikenal); diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **54,75**
- Halaman kunci: 63

**54,75%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H11 — ✅ LULUS

**Pertanyaan:** Total publikasi 20, terdiri atas 4 artikel Q1 hasil kolaborasi dengan penulis luar negeri, 6 artikel Q1 tanpa kolaborasi, dan 10 prosiding internasional terindeks Scopus. Berapa capaian IKU 6?

**Jawaban chatbot:**

```text
Capaian IKU 6 = 67,5 % [4][1]

Penjelasan perhitungan (menggunakan alat hitung_iku):
- 6 artikel Q1 tanpa kolaborasi: 6 × 1 = 6  
- 10 prosiding internasional: 10 × 0,25 = 2,5  
- 4 artikel Q1 dengan kolaborasi internasional: 4 × (1 + 0,25) = 5  
- Σ (n·k) = 13,5  
- Capaian = 13,5 ÷ 20 × 100 % = 67,5 %  

Hasil dan langkah perhitungan diberikan oleh alat hitung_iku.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 63 (IKU 6, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 117–118; PPT hlm. 61
- [4] Buku IKU Diktisaintek Berdampak V1, hlm. 63 (IKU 6, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 119

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 6 – Kriteria (bobot kuartil) & Formula, hlm. 63

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\": \"iku6\", \"pembilang\": 13.5, \"penyebut\": 20}","fungsi":"rasio"}` → 'iku6' bukan kode rasio: IKU ini punya fungsi sendiri (iku6). Panggil ulang hitung_iku dengan fungsi tersebut dan data asli dari pertanyaan (jangan dihitung dulu). Format: - iku6: {"total_publikasi": 200, "publikasi": {"q1": 40}, "kolaborasi": {"q1": 4}}  (jenis: "top_tier", "q1", "q2", "q3", "q4", "prosiding", "tidak_terindeks"; kolaborasi = publikasi dengan penulis luar negeri)
- argumen `{"argumen_json":"{\"total_publikasi\": 20, \"publikasi\": {\"q1\": 10, \"prosiding\": 10}, \"kolaborasi\": {\"q1\": 4}}","fungsi":"iku6"}` → ValueError: Jumlah publikasi per jenis (24) melebihi total publikasi (20). Periksa nama fungsi dan format argumen.
- argumen `{"argumen_json":"{\"total_publikasi\": 20, \"publikasi\": {\"q1\": 6, \"prosiding\": 10}, \"kolaborasi\": {\"q1\": 4}}","fungsi":"iku6"}` → 67,50

**Jawaban yang diharapkan:**

- Angka kunci: **67,50**
- Halaman kunci: 63

**67,5%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H12 — ✅ LULUS

**Pertanyaan:** Dari 60 program SDGs PT, 45 program berkontribusi pada SDG 1, 4, 17, dan 2 SDG pilihan. Berapa capaian IKU 7?

**Jawaban chatbot:**

```text
Capaian IKU 7 dihitung dengan rumus:

(Jumlah program/kegiatan yang berkontribusi pada SDG 1, 4, 17, dan 2 SDG pilihan) ÷ (Total program SDG PT) × 100%  

= 45 ÷ 60 × 100% = **75 %** [1][2] (hasil perhitungan oleh alat hitung_iku).
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 58 (IKU 7, Formula); juga di PPT hlm. 55; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 121
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 58 (IKU 7, Kriteria); juga di PPT hlm. 55; PPT hlm. 54; PPT hlm. 54; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 119–120; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 119–120

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 7 – Formula, hlm. 58

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\":\"iku7\",\"pembilang\":45,\"penyebut\":60}","fungsi":"rasio"}` → 75,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'rasio' tidak dikenal); diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **75,00**
- Halaman kunci: 58

**75%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H13 — ✅ LULUS

**Pertanyaan:** Total pendapatan PT dalam satu tahun anggaran adalah Rp500 miliar, terdiri atas: - UKT Rp300 miliar - BOPTN Rp80 miliar - hibah riset kompetitif Rp50 miliar - jasa konsultasi dan pelatihan Rp40 miliar - unit bisnis (hotel, penerbitan) Rp20 miliar - hasil investasi dana abadi Rp10 miliar Berapa capaian IKU 9?

**Jawaban chatbot:**

```text
Capaian IKU 9 – Persentase Pendapatan Non Pendidikan/UKT adalah **24 %**.

Perhitungan:
- Total pendapatan PT dalam satu tahun anggaran: Rp500 miliar.
- Pendapatan yang termasuk dalam kriteria non-mahasiswa (hibah riset kompetitif, jasa konsultasi, pelatihan, unit bisnis, hasil investasi dana abadi) = Rp50 miliar + Rp40 miliar + Rp0 + Rp20 miliar + Rp10 miliar = **Rp120 miliar**.
- Persentase = (Rp120 miliar ÷ Rp500 miliar) × 100 % = **24 %**.

Langkah perhitungan dan hasil diperoleh melalui fungsi hitung_iku sesuai rumus resmi IKU 9 [3][1][2].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 59 (IKU 9, Kriteria); juga di PPT hlm. 56; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 122–123
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 59 (IKU 9, Definisi); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 122; PPT hlm. 56
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 59 (IKU 9, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 124; PPT hlm. 56

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 9 – Kriteria & Formula, hlm. 59

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\": \"iku9\", \"pembilang\": 120, \"penyebut\": 500}","fungsi":"rasio"}` → 'iku9' bukan kode rasio: IKU ini punya fungsi sendiri (iku9). Panggil ulang hitung_iku dengan fungsi tersebut dan data asli dari pertanyaan (jangan dihitung dulu). Format: - iku9: {"total_pendapatan": "3 milyar", "rincian": {"hibah_riset": "450 jt", "pelatihan": "0,1 M", "ukt": "2,45 M"}}  (masukkan SEMUA pos yang disebut, termasuk yang tidak dihitung; pos yang dihitung: "aset_produktif", "filantropi_tercatat", "hasil_dana_abadi", "hibah_riset", "inkubasi", "kerja_sama", "komersialisasi", "konsultasi", "kontrak_riset", "layanan_profesional", "pelatihan", "royalti", "unit_bisnis"; pos yang tidak dihitung: "boptn", "bpptnbh", "filantropi_tidak_tercatat", "iuran_pengembangan", "pokok_dana_abadi", "subsidi_pemerintah", "ukt")
- argumen `{"argumen_json":"{\"total_pendapatan\": \"500 miliar\", \"rincian\": {\"hibah_riset\": \"50 miliar\", \"konsultasi\": \"40 miliar\", \"pelatihan\": \"0\", \"unit_bisnis\": \"20 miliar\", \"hasil_dana_abadi\": \"10 miliar\", \"ukt\": \"300 miliar\", \"boptn\": \"80 miliar\"}}","fungsi":"iku9"}` → 24,00

**Jawaban yang diharapkan:**

- Angka kunci: **24,00**
- Halaman kunci: 59

**24%**. Jawaban yang memasukkan BOPTN (200/500 = 40%) **salah**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H14 — ✅ LULUS

**Pertanyaan:** PT memiliki 300 dosen dalam satu tahun terakhir; 45 dosen ber-NUPTK mendapat rekognisi internasional. Berapa capaian IKU 4?

**Jawaban chatbot:**

```text
Capaian IKU 4 = 15 % [1][2][3]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 62–63 (IKU 4, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 112; PPT hlm. 60–61
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 61 (IKU 4, Definisi); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 108; PPT hlm. 58
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 62 (IKU 4, Ketentuan); juga di PPT hlm. 60; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 111–112

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 4 – Formula, hlm. 62

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\": \"iku4\", \"pembilang\": 45, \"penyebut\": 300}","fungsi":"rasio"}` → 15,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'rasio' tidak dikenal); diulang otomatis.
- Panggilan alat ditolak server (nama alat 'hituk_iku' tidak dikenal); diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **15,00**
- Halaman kunci: 62

**15%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H15 — ✅ LULUS

**Pertanyaan:** Dari 400 SDM PT (dosen/peneliti), 12 orang terlibat langsung dalam penyusunan kebijakan nasional/daerah/industri, dibuktikan dengan SK atau undangan resmi. Berapa capaian IKU 8?

**Jawaban chatbot:**

```text
Capaian IKU 8 adalah **3 %**. Perhitungannya: (12 ÷ 400) × 100 % = 3 % [3][5]
```

**Sitasi chatbot:**

- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 64 (IKU 8, Formula); juga di PPT hlm. 63; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 122
- [5] PPT IKU Diktisaintek Berdampak PTS V2, hlm. 20

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 8 – Formula, hlm. 64

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\": \"iku8\", \"pembilang\": 12, \"penyebut\": 400}","fungsi":"rasio"}` → 3,00

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **3,00**
- Halaman kunci: 64

**3%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H16 — ✅ LULUS

**Pertanyaan:** Nilai akhir evaluasi SAKIP sebuah PT adalah 82. Apa predikatnya?

**Jawaban chatbot:**

```text
Berdasarkan perhitungan dengan rumus resmi IKU, nilai akhir 82 termasuk dalam rentang 80–89, sehingga predikat SAKIP yang diberikan adalah **A (sangat baik)**【iku11b_predikat】.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 11b – Skala dan Predikat, hlm. 66

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"nilai_akhir\": 82}","fungsi":"iku11b_predikat"}` → A (sangat baik)

**Peringatan chatbot:**

- LLM menghitung sendiri tanpa kalkulator; diminta mengulang dengan alat.
- Panggilan alat ditolak server (nama alat 'hitungan_iku' tidak dikenal); diulang otomatis.
- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **A (sangat baik)**
- Halaman kunci: 66

Predikat **A (sangat baik)**, rentang nilai 80–89: efektif dan efisien, menghasilkan kinerja di atas target.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H17 — ✅ LULUS

**Pertanyaan:** PT merencanakan 24 kegiatan pencegahan dan penanganan kekerasan, narkoba, dan korupsi; 18 kegiatan terlaksana. Berapa capaian IKU 11d?

**Jawaban chatbot:**

```text
Capaian IKU 11d (Pencegahan dan Penanganan Anti Kekerasan, Anti Narkoba, dan Anti Korupsi) adalah **75 %**. Perhitungannya: 18 kegiatan terlaksana ÷ 24 kegiatan direncanakan × 100 % = 75 %[1].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 68 (IKU 11d, Formula)

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 11d – Formula, hlm. 68

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\": \"iku11d\", \"pembilang\": 18, \"penyebut\": 24}","fungsi":"rasio"}` → 75,00

**Jawaban yang diharapkan:**

- Angka kunci: **75,00**
- Halaman kunci: 68

**75%**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H18 — ✅ LULUS

**Pertanyaan:** UMP di provinsi tempat PT berada adalah Rp3.000.000. Berapa penghasilan minimum dosen dengan jabatan Lektor dan Profesor menurut IKU 12?

**Jawaban chatbot:**

```text
Menurut IKU 12, penghasilan minimum dosen dihitung dengan mengalikan UMP dengan faktor yang ditetapkan untuk masing-meningkat jabatan:

- **Lektor**: ≥ 3 × UMP  
- **Profesor**: ≥ 6 × UMP  

Dengan UMP = Rp3.000.000, perhitungannya adalah:

- Lektor: 3 × Rp3.000.000 = **Rp9.000.000**  
- Profesor: 6 × Rp3.000.000 = **Rp18.000.000**  

Hasil perhitungan diperoleh melalui fungsi `iku12_penghasilan_minimum` [1].
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 60 (IKU 12, Kriteria); juga di PPT hlm. 57; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 131

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 12 – Kriteria b.2, hlm. 60

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"ump\": \"Rp3.000.000\", \"jabatan\": [\"lektor\", \"profesor\"]}","fungsi":"iku12_penghasilan_minimum"}` → lektor = 9.000.000,00, profesor = 18.000.000,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'hit\u200buk\u200bi\u200b12_penghasilan_minimum' tidak dikenal); diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **lektor = 9.000.000, profesor = 18.000.000**
- Halaman kunci: 60

Lektor minimal **Rp9.000.000**, Profesor minimal **Rp18.000.000**.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### D13 — ✅ LULUS

**Pertanyaan:** aee tu apaan sih? ngukur apa?

**Jawaban chatbot:**

```text
AEE (Angka Efisiensi Edukasi) adalah indikator yang mengukur **tingkat keberhasilan mahasiswa menyelesaikan studi tepat waktu sesuai masa studi standar** dibandingkan dengan total mahasiswa yang masuk pada periode tertentu [3]. AEE menilai seberapa efisien perguruan tinggi dalam menghasilkan lulusan yang lulus tepat waktu.
```

**Sitasi chatbot:**

- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Definisi); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 100; PPT hlm. 45

**Jawaban yang diharapkan:**

- Halaman kunci: 49

AEE = Angka Efisiensi Edukasi (IKU 1), mengukur keberhasilan mahasiswa menyelesaikan studi **tepat waktu** sesuai masa studi standar (sama dengan D01).

*Catatan soal:* Ketahanan: bahasa santai ('aee tu apaan sih'). 'AEE' sengaja tidak dijadikan fakta karena sudah ada di pertanyaan.

**Pemeriksaan otomatis:**

- ✅ fakta: tepat waktu
- ✅ fakta: efisiensi edukasi
- ✅ halaman sitasi benar

### D14 — ✅ LULUS

**Pertanyaan:** pendptan apa aj yg ga diitung di iku9?

**Jawaban chatbot:**

```text
Pendapatan yang **tidak dihitung** dalam IKU 9 – Persentase Pendapatan Non Pendidikan/UKT meliputi:

1. SPP/UKT/biaya kuliah mahasiswa[4]  
2. Iuran pengembangan institusi[4]  
3. Subsidi langsung dari pemerintah, termasuk belanja pegawai, belanja operasional, BOPTN, BPPTNBH, dan sejenisnya[4]  
4. Sumbangan/filantropi yang **tidak masuk** laporan keuangan resmi perguruan tinggi[4]  
5. Dana pokok dana abadi/endowment fund (yang disimpan permanen dan tidak dibelanjakan)[4]  
6. Pendapatan yang **tidak dibukukan** dalam laporan keuangan[5]  
7. Hibah barang **tanpa nilai** yang tidak tercatat[5]  
8. Dana yang lewat kampus tanpa pelaporan resmi[5]

Semua jenis pendapatan di atas dikecualikan dari perhitungan IKU 9.
```

**Sitasi chatbot:**

- [4] Buku IKU Diktisaintek Berdampak V1, hlm. 59 (IKU 9, Kriteria); juga di PPT hlm. 56; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 122–123
- [5] Buku IKU Diktisaintek Berdampak V1, hlm. 79 (IKU 9, Kriteria dan Ketentuan); juga di PPT hlm. 81; PPT hlm. 85; PPT hlm. 86

**Jawaban yang diharapkan:**

- Halaman kunci: 59

SPP/UKT, iuran pengembangan institusi, subsidi langsung pemerintah (termasuk BOPTN/BPPTNBH), filantropi yang tidak tercatat, dan pokok dana abadi (sama dengan D08).

*Catatan soal:* Ketahanan: typo ('pendptan', 'aj', 'diitung', 'iku9'). Sama dengan D08.

**Pemeriksaan otomatis:**

- ✅ fakta: UKT / SPP
- ✅ fakta: BOPTN
- ✅ fakta: iuran pengembangan
- ✅ fakta: dana abadi / endowment
- ✅ halaman sitasi benar

### H19 — ✅ LULUS

**Pertanyaan:** brp aee s1 klo yg lulus tepat wktu cm 40 org dr 200 mhs?

**Jawaban chatbot:**

```text
AEE (Angka Efisiensi Edukasi) untuk program S1 dengan 40 mahasiswa lulus tepat waktu dari total 200 mahasiswa adalah **20 %**[1].  

Langkah perhitungannya:
- AEE realisasi = 40 ÷ 200 × 100 % = 20 %  
- AEE ideal S1 = 25 % (berdasarkan standar masa studi 8 semester)  
- Tingkat pencapaian = 20 % ÷ 25 % × 100 % = 80 %  

Jadi, AEE S1 = 20 % (tingkat pencapaian 80 %).
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49 (IKU 1, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 100; PPT hlm. 45

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 1 – Ketentuan & Formula a–b, hlm. 49

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"jenjang\": \"S1\", \"lulus_tepat_waktu\": 40, \"total_mahasiswa\": 200, \"pindah\": 0, \"drop_out\": 0, \"cuti_lebih\": 0}","fungsi":"iku1_aee_prodi"}` → aee_realisasi_pct = 20,00, tingkat_pencapaian_pct = 80,00

**Jawaban yang diharapkan:**

- Angka kunci: **aee_realisasi_pct = 20,00, tingkat_pencapaian_pct = 80,00**
- Halaman kunci: 49

AEE realisasi **20%**, tingkat pencapaian **80%**.

*Catatan soal:* Ketahanan: typo & singkatan (brp, klo, wktu, mhs). Sama dengan H01.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H20 — ✅ LULUS

**Pertanyaan:** realisasi aee kampus kmi: D3 30%, S1 22,5%, S2 40%. aee pt nya jd brp ya?

**Jawaban chatbot:**

```text
AEE PT = **86,97 %**. [2][1]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 49–50 (IKU 1, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102; PPT hlm. 46; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 101–102; PPT hlm. 46–47
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 49–50 (IKU 1, Formula)

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 1 – Formula c & contoh perhitungan, hlm. 49–50

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"realisasi_per_jenjang\": {\"D3\": 30, \"S1\": 22.5, \"S2\": 40}}","fungsi":"iku1_aee_pt"}` → 86,97

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'hit_iku' tidak dikenal); diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **86,97**
- Halaman kunci: 49, 50

**86,97%**.

*Catatan soal:* Ketahanan: desimal koma '22,5%' harus dibaca 22.5. Sama dengan H02.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H21 — ✅ LULUS

**Pertanyaan:** lulusan kampus kami 1.341 org, minimal responden tracer study nya brp?

**Jawaban chatbot:**

```text
Berdasarkan rumus Slovin (IKU 2 – Formula Responden Minimum) dengan galat d = 2,3 % dan jumlah lulusan N = 1 341, jumlah responden minimum yang diperlukan adalah **785 responden**[2]. 

Langkah perhitungannya:
- Hitung N × d² = 1 341 × 0,023² ≈ 0,71  
- n = N ÷ (N × d² + 1) = 1 341 ÷ (0,71 + 1) ≈ 784,5  
- Dibulatkan ke atas menjadi 785 responden.
```

**Sitasi chatbot:**

- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 52 (IKU 2, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104–105; PPT hlm. 48–49

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 2 – Formula Responden Minimum, hlm. 52

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"jumlah_lulusan\": 1341}","fungsi":"iku2_responden_minimum"}` → 785

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **785**
- Halaman kunci: 52

**785 responden**.

*Catatan soal:* Ketahanan: titik pemisah ribuan '1.341' = 1341 (bukan 1,341).

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H22 — ✅ LULUS

**Pertanyaan:** klo lulusannya 2rb orang, responden minimum tracer studi brp

**Jawaban chatbot:**

```text
Berdasarkan rumus Slovin untuk menghitung responden minimum (d = 2,3 %), dengan jumlah lulusan N = 2.000 orang, jumlah responden minimum yang harus dikumpulkan adalah **972 responden** [2][1].

Langkah perhitungannya:
1. Hitung N·d² = 2.000 × (0,023)² = 1,06  
2. n = 2.000 ÷ (1,06 + 1) = 971,82  
3. Dibulatkan ke atas menjadi 972 responden.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 51 (IKU 2, Ketentuan); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104; PPT hlm. 48
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 52 (IKU 2, Formula); juga di PPT hlm. 48–49; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 104–105

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 2 – Formula Responden Minimum, hlm. 52

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"jumlah_lulusan\": 2000}","fungsi":"iku2_responden_minimum"}` → 972

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'hituk_iku' tidak dikenal); diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **972**
- Halaman kunci: 52

**972 responden**.

*Catatan soal:* Ketahanan: '2rb' = 2000. Sama dengan H06.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H23 — ✅ LULUS

**Pertanyaan:** kerjsama PT kita ada 120, luaran nya 30 judul. capaian iku5 brp persen?

**Jawaban chatbot:**

```text
Capaian IKU 5 (Rasio luaran hasil kerja sama antara PT dan start-up/industri/lembaga) dihitung dengan rumus:

(Jumlah luaran hasil kerja sama ÷ Total kerja sama PT) × 100% = 30 ÷ 120 × 100% = 25 % [rasio][1] 

Jadi, capaian IKU 5 sebesar **25 %**.
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 57–58 (IKU 5, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 117; PPT hlm. 53

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 5 – Formula & Keterangan, hlm. 57

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\":\"iku5\",\"pembilang\":30,\"penyebut\":120}","fungsi":"rasio"}` → 25,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'rasio' tidak dikenal); diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **25,00**
- Halaman kunci: 57

**25%**.

*Catatan soal:* Ketahanan: typo 'kerjsama', 'iku5' tanpa spasi. Sama dengan H09.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H24 — ✅ LULUS

**Pertanyaan:** dr 50 progam sdgs, 25 yg kontribusi ke sdg 1,4,17 + 2 sdg pilihan. capaian iku 7 brapa

**Jawaban chatbot:**

```text
Capaian IKU 7 dihitung dengan rumus:

(Jumlah program/kegiatan yang berkontribusi pada SDG 1, 4, 17 plus 2 SDG pilihan) ÷ (Total program SDG PT) × 100%  

= 25 ÷ 50 × 100% = **50 %**[4]. 

Jadi, persentase keterlibatan perguruan tinggi dalam SDG 1, 4, 17 dan dua SDG pilihan lainnya adalah **50 %**.
```

**Sitasi chatbot:**

- [4] Buku IKU Diktisaintek Berdampak V1, hlm. 58 (IKU 7, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 121; PPT hlm. 55

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 7 – Formula, hlm. 58

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\": \"iku7\", \"pembilang\": 25, \"penyebut\": 50}","fungsi":"rasio"}` → 50,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'rasio' tidak dikenal); diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.
- LLM mengembalikan respons kosong; diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **50,00**
- Halaman kunci: 58

**50%**.

*Catatan soal:* Ketahanan: typo 'progam', 'brapa'.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H25 — ✅ LULUS

**Pertanyaan:** total pendapatan PT 500 M. rinciannya ukt 300M, boptn 80 M, hibah riset 50M, konsultasi 40 M, unit bisnis 20M, hasil dana abadi 10 M. iku 9 brp?

**Jawaban chatbot:**

```text
IKU 9 – Persentase Pendapatan Non Pendidikan/UKT  
Capaian = 24 %  

Perhitungan: total pendapatan PT = 500 M; pendapatan yang diakui sebagai non-pendidikan (hibah riset 50 M + konsultasi 40 M + unit bisnis 20 M + hasil dana abadi 10 M) = 120 M. 120 M ÷ 500 M × 100% = 24 % [2][3] (rumus pada Buku IKU V1, hlm. 59).
```

**Sitasi chatbot:**

- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 59 (IKU 9, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 122–123; PPT hlm. 56
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 79 (IKU 9, Kriteria dan Ketentuan); juga di PPT hlm. 83; PPT hlm. 85

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 9 – Kriteria & Formula, hlm. 59

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_pendapatan\": \"500 M\", \"rincian\": {\"hibah_riset\": \"50 M\", \"konsultasi\": \"40 M\", \"unit_bisnis\": \"20 M\", \"hasil_dana_abadi\": \"10 M\"}}","fungsi":"iku9"}` → 24,00

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

### H26 — ✅ LULUS

**Pertanyaan:** pendapatan total Rp1.250.000.000, terdiri dr ukt rp 900jt, kontrak riset 150 juta, royalti Rp50.000.000, sisanya 150jt dari boptn. capaian iku 9?

**Jawaban chatbot:**

```text
Capaian **IKU 9 – Persentase Pendapatan Non Pendidikan/UKT** sebesar **16 %**.

**Perhitungan (mengikuti rumus resmi):**  
- Total pendapatan PT: 1 250 jt = Rp1.250.000.000.  
- Pendapatan yang diakui sebagai non-mahasiswa (kriteria a): kontrak riset 150 jt + royalti 50 jt = 200 jt = Rp200.000.000.  
- Pendapatan yang tidak dihitung (kriteria b): UKT 900 jt dan BOPTN 150 jt.  

Capaian = (200 jt ÷ 1 250 jt) × 100 % = **16 %**.  

Sumber: Buku IKU Diktisaintek Berdampak V1, IKU 9 – Kriteria & Formula, hlm. 59.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 9 – Kriteria & Formula, hlm. 59

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_pendapatan\": \"1,250,000,000\", \"rincian\": {\"ukt\": \"900 jt\", \"kontrak_riset\": \"150 jt\", \"royalti\": \"50 jt\", \"boptn\": \"150 jt\"}}","fungsi":"iku9"}` → ValueError: Jumlah rincian pendapatan (1.250.000.000) melebihi total pendapatan (1.250.000). Periksa nama fungsi dan format argumen.
- argumen `{"argumen_json":"{\"total_pendapatan\": \"1250 jt\", \"rincian\": {\"ukt\": \"900 jt\", \"kontrak_riset\": \"150 jt\", \"royalti\": \"50 jt\", \"boptn\": \"150 jt\"}}","fungsi":"iku9"}` → 16,00

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'hit\u200buk\u200bik\u200bu\u200b9' tidak dikenal); diulang otomatis.
- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **16,00**
- Halaman kunci: 59

**16%**.

*Catatan soal:* Ketahanan: campuran 'Rp1.250.000.000', '900jt', '150 juta', 'Rp50.000.000'. Satuan harus disamakan sebelum dihitung.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H27 — ✅ LULUS

**Pertanyaan:** total pendapatan 2 milyar: hibah riset 300 jt, konsultasi 0,2 M, ukt 1,5 M. hitung iku 9 nya

**Jawaban chatbot:**

```text
IKU 9 – Persentase Pendapatan Non Pendidikan/UKT menghitung proporsi pendapatan yang tidak berasal dari UKT dibandingkan total pendapatan perguruan tinggi.  

Data yang diberikan:  
- Total pendapatan = 2 milyar (Rp2.000.000.000)  
- Hibah riset = 300 jt (Rp300.000.000) – termasuk dalam pendapatan non-mahasiswa  
- Konsultasi = 0,2 M (Rp200.000.000) – termasuk dalam pendapatan non-mahasiswa  
- UKT = 1,5 M (Rp1.500.000.000) – tidak dihitung karena merupakan pendapatan mahasiswa  

Menggunakan fungsi **iku9** untuk menghitung persentasenya, diperoleh:

- Pendapatan non-mahasiswa = 300 jt + 200 jt = 500 jt (Rp500.000.000)  
- Persentase = (500 jt ÷ 2 milyar) × 100% = **25 %**  

Langkah perhitungan dan hasil lengkap dapat dilihat pada output alat perhitungan: 25 % [hasil, langkah, dan sumber dari Buku IKU Diktisaintek Berdampak, hlm. 59]​.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 9 – Kriteria & Formula, hlm. 59

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"total_pendapatan\": \"2 milyar\", \"rincian\": {\"hibah_riset\": \"300 jt\", \"konsultasi\": \"0,2 M\", \"ukt\": \"1,5 M\"}}","fungsi":"iku9"}` → 25,00

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.
- Panggilan alat ditolak server (nama alat 'hit...' tidak dikenal); diulang otomatis.
- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **25,00**
- Halaman kunci: 59

**25%**.

*Catatan soal:* Ketahanan: ejaan 'milyar', desimal koma '0,2 M' dan '1,5 M' dicampur dengan 'jt'.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H28 — ❌ PERLU DICEK

**Pertanyaan:** ump disini 3,5jt, penghasilan minimal dosen lektor kepala brp?

**Jawaban chatbot:**

```text
Penghasilan minimal dosen dengan jabatan **Lektor Kepala** harus sebesar **4 kali UMP**. Dengan UMP = Rp 3,500,000, maka:

4 × Rp 3,500,000 = **Rp 14,000,000** [hasil hitung_iku] 

Jadi, penghasilan minimal dosen Lektor Kepala adalah **Rp 14 juta**.
```

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 12 – Kriteria b.2, hlm. 60

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"ump\":\"Rp3,500,000\",\"jabatan\":[\"lektor_kepala\"]}","fungsi":"iku12_penghasilan_minimum"}` → lektor_kepala = 14.000,00

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.
- Jawaban tidak memuat rujukan [n] ke konteks.

**Jawaban yang diharapkan:**

- Angka kunci: **lektor_kepala = 14.000.000**
- Halaman kunci: 60

Lektor kepala minimal **Rp14.000.000**.

*Catatan soal:* Ketahanan: '3,5jt' = Rp3.500.000. Argumen ump harus rupiah penuh, bukan 3.5.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ❌ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H29 — ✅ LULUS

**Pertanyaan:** UMP prov kami Rp 4.250.000 , brp penghasilan min dosen asisten ahli sm profesor?

**Jawaban chatbot:**

```text
Penghasilan minimum dosen berdasarkan UMP Rp 4.250.000 adalah:

- **Asisten Ahli:** ≥ 1,5 × UMP = Rp 6.375.000 per bulan [1]  
- **Profesor:** ≥ 6 × UMP = Rp 25.500.000 per bulan [1]  

(Perhitungan menggunakan fungsi hitung_iku yang menghasilkan nilai Rp 6.375.000 untuk Asisten Ahli dan Rp 25.500.000 untuk Profesor.)
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 60 (IKU 12, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 131; PPT hlm. 57

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 12 – Kriteria b.2, hlm. 60

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"ump\": \"Rp 4.250.000\", \"jabatan\": [\"asisten_ahli\", \"profesor\"]}","fungsi":"iku12_penghasilan_minimum"}` → asisten_ahli = 6.375.000,00, profesor = 25.500.000,00

**Peringatan chatbot:**

- LLM mengembalikan respons kosong; diulang otomatis.
- Panggilan alat ditolak server (nama alat 'hituk_iku' tidak dikenal); diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **asisten_ahli = 6.375.000, profesor = 25.500.000**
- Halaman kunci: 60

Asisten ahli minimal **Rp6.375.000**, profesor minimal **Rp25.500.000**.

*Catatan soal:* Ketahanan: 'Rp 4.250.000' dengan spasi setelah Rp dan titik ribuan.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar

### H30 — ✅ LULUS

**Pertanyaan:** dosen kami 250 org setahun terakhir, yg ber-NUPTK & dpt rekognisi internasional 18 org. capaiannya brp?

**Jawaban chatbot:**

```text
Persentase Dosen Perguruan Tinggi yang mendapatkan rekognisi internasional adalah **7,2 %**. Perhitungannya menggunakan rumus:

\( \frac{\text{Jumlah dosen ber-NUPTK yang mendapat rekognisi internasional}}{\text{Total dosen PT dalam satu tahun terakhir}} \times 100\% \)

\( = \frac{18}{250} \times 100\% = 7,2\% \) [1][2][3]
```

**Sitasi chatbot:**

- [1] Buku IKU Diktisaintek Berdampak V1, hlm. 62–63 (IKU 4, Formula); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 112; PPT hlm. 60–61
- [2] Buku IKU Diktisaintek Berdampak V1, hlm. 61 (IKU 4, Definisi); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 108; PPT hlm. 58
- [3] Buku IKU Diktisaintek Berdampak V1, hlm. 61–62 (IKU 4, Kriteria); juga di Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 108–111; PPT hlm. 58; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 108–111; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 108–111; PPT hlm. 59; Buku (Lampiran Kepmen 358/M/KEP/2025) hlm. 108–111; PPT hlm. 58; PPT hlm. 59

**Sumber rumus (kalkulator):**

- Buku IKU Diktisaintek Berdampak V1, IKU 4 – Formula, hlm. 62

**Panggilan kalkulator:**

- argumen `{"argumen_json":"{\"kode\":\"iku4\",\"pembilang\":18,\"penyebut\":250}","fungsi":"rasio"}` → 7,20

**Peringatan chatbot:**

- Panggilan alat ditolak server (nama alat 'rasio' tidak dikenal); diulang otomatis.

**Jawaban yang diharapkan:**

- Angka kunci: **7,20**
- Halaman kunci: 62

**7,2%** (IKU 4).

*Catatan soal:* Ketahanan: nomor IKU tidak disebut; chatbot harus mengenali IKU 4 dari isi soal.

**Pemeriksaan otomatis:**

- ✅ kalkulator dipanggil
- ✅ hasil kalkulator = kunci
- ✅ angka kunci ada di jawaban
- ✅ halaman sitasi benar
