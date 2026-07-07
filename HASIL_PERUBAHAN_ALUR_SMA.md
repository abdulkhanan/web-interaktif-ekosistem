# Hasil Revisi Alur Guided Inquiry Level SMA

Revisi ini dibuat karena versi sebelumnya terlalu banyak memberikan contoh dan kalimat bantu sehingga terasa seperti siswa “disuapi”. Pada versi ini, alur tetap sesuai sintaks guided inquiry, tetapi disajikan dengan tingkat kemandirian yang lebih sesuai untuk siswa SMA.

## Perubahan Utama

1. Istilah alur dikembalikan ke sintaks formal guided inquiry:
   - Orientasi
   - Merumuskan masalah
   - Merumuskan hipotesis
   - Mengumpulkan data
   - Menganalisis/menguji hipotesis
   - Menarik kesimpulan

2. Bagian simulasi tidak lagi menampilkan contoh rumusan masalah dan contoh hipotesis siap pakai.

3. Petunjuk diubah menjadi **rambu penyelidikan**, berisi:
   - konteks penyelidikan,
   - variabel yang dimanipulasi,
   - parameter yang diamati,
   - data yang dapat digunakan sebagai bukti,
   - konsep ekologi yang perlu dipakai saat menganalisis.

4. Halaman Tanggapan Siswa diubah menjadi **Lembar Jawaban Guided Inquiry** dengan kolom:
   - Rumusan masalah penyelidikan,
   - Hipotesis dan dasar teori,
   - Analisis data dan uji hipotesis,
   - Kesimpulan berbasis bukti.

5. Placeholder tetap ada, tetapi tidak memberikan pola jawaban seperti “Bagaimana pengaruh...” atau “Jika..., maka...”. Placeholder hanya berfungsi sebagai arahan umum.

6. Tombol simulasi diubah menjadi **Pilih Hasil Ini untuk Dianalisis** agar lebih sesuai dengan aktivitas ilmiah siswa SMA.

## Catatan

Struktur database tidak diubah. Kolom lama seperti `jawaban_1`, `jawaban_2`, `jawaban_3`, dan `kesimpulan` tetap digunakan agar aman dengan Supabase/SQLite yang sudah ada. Perubahan hanya pada tampilan, instruksi, dan makna pedagogis tiap kolom.
