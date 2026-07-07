# Revisi Penyelarasan Media dengan Guided Inquiry / Inkuiri Terbimbing

Revisi ini menyelaraskan media dengan sintaks:

1. Orientasi
2. Merumuskan masalah
3. Merumuskan hipotesis
4. Mengumpulkan data
5. Menganalisis/menguji hipotesis
6. Menarik kesimpulan

## File yang direvisi

### pages/3_Simulasi_Ekosistem.py
- Menambahkan panduan sintaks guided inquiry pada setiap simulasi.
- Menambahkan contoh rumusan masalah, contoh hipotesis, data yang perlu diamati, dan cara menguji hipotesis.
- Mengubah arahan halaman agar siswa tidak hanya menjalankan simulasi, tetapi juga menyiapkan masalah, hipotesis, data, dan uji hipotesis.

### pages/4_Tanggapan_Siswa.py
- Mengubah instruksi halaman agar jawaban siswa mengikuti guided inquiry.
- Menambahkan kartu penjelasan alur jawaban: rumusan masalah, hipotesis, data/uji hipotesis, dan kesimpulan.

### components/ui.py
- Mengubah pertanyaan tanggapan siswa agar sesuai sintaks guided inquiry.
- Mengubah tampilan jawaban guru menjadi:
  1. Rumusan Masalah
  2. Hipotesis
  3. Data Hasil Pengamatan dan Uji Hipotesis
  4. Kesimpulan dan Aksi Nyata
- Memperbaiki kecocokan nama simulasi Daur Air, CO2, dan O2 agar tidak masuk ke pertanyaan default.

### pages/9_Feedback_Guru.py
- Menyesuaikan deskripsi feedback guru agar mengacu pada jawaban guided inquiry.

### pages/10_Panduan_Penggunaan.py
- Mengubah tabel alur guided inquiry agar sesuai dengan sintaks yang digunakan dalam penelitian.

## Catatan

Struktur database tidak diubah agar tetap kompatibel dengan Supabase lama. Kolom jawaban tetap memakai empat kolom utama:

- jawaban_1 = Rumusan masalah
- jawaban_2 = Hipotesis
- jawaban_3 = Data hasil pengamatan dan uji hipotesis
- kesimpulan = Kesimpulan dan aksi nyata

Dengan cara ini, media menjadi lebih sesuai guided inquiry tanpa perlu menjalankan migrasi database baru.
