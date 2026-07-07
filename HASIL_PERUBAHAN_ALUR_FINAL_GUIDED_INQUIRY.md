# Hasil Perubahan Alur Guided Inquiry

Perubahan dibuat dari file `awal(1).zip` sesuai arahan alur pembelajaran:

**Fenomena + gambar → rumusan masalah → hipotesis → simulasi/perubahan variabel → pengumpulan data → materi pendukung → uji hipotesis → kesimpulan dan tindakan nyata.**

## 1. Halaman Simulasi Ekosistem

File yang diubah: `pages/3_Simulasi_Ekosistem.py`

Perubahan utama:

- Tampilan awal setiap simulasi sekarang langsung menampilkan **fenomena masalah** dan **gambar pendukung**.
- Sebelum simulasi muncul, siswa wajib mengisi:
  - rumusan masalah penyelidikan;
  - hipotesis awal;
  - dasar konsep yang digunakan.
- Bagian simulasi baru terbuka setelah rumusan masalah dan hipotesis diisi.
- Tombol simulasi diubah menjadi **Simpan Data untuk Uji Hipotesis** agar alurnya lebih jelas.
- Data rumusan masalah, hipotesis, dan dasar konsep ikut disimpan di `input_simulasi` tanpa mengubah struktur database.
- Materi pendukung disediakan melalui panel/tombol **Materi Pendukung untuk Penyelidikan**.
- Tampilan hasil simulasi dibuat lebih ringan:
  - ringkasan hasil utama;
  - grafik yang dipisah sesuai hubungan variabel;
  - data lengkap disembunyikan dalam expander.

## 2. Halaman Uji Hipotesis dan Kesimpulan

File yang diubah: `pages/4_Tanggapan_Siswa.py`

Perubahan utama:

- Judul halaman diubah menjadi **Uji Hipotesis dan Kesimpulan**.
- Halaman ini tidak lagi meminta siswa menulis rumusan masalah dan hipotesis dari awal karena sudah diisi sebelum simulasi.
- Siswa diarahkan untuk:
  - menguji hipotesis berdasarkan data simulasi;
  - menghubungkan hasil dengan materi pendukung;
  - menyusun kesimpulan ilmiah;
  - menuliskan tindakan nyata.

## 3. Komponen Tampilan Guru dan Pertanyaan Guided Inquiry

File yang diubah: `components/ui.py`

Perubahan utama:

- Pertanyaan guided inquiry disesuaikan dengan alur baru.
- Tampilan jawaban siswa di halaman guru diubah menjadi:
  - Uji Hipotesis Berdasarkan Data;
  - Kaitan dengan Materi Pendukung;
  - Kesimpulan Ilmiah;
  - Tindakan Nyata.
- Ringkasan hasil siswa sekarang menampilkan **Rencana Investigasi Awal** yang berisi:
  - Rumusan Masalah;
  - Hipotesis Awal;
  - Dasar Konsep.

## 4. Panduan Penggunaan

File yang diubah: `pages/10_Panduan_Penggunaan.py`

Perubahan utama:

- Panduan siswa dan guru diselaraskan dengan alur final guided inquiry.
- Tabel alur guided inquiry diperbarui menjadi:
  - Orientasi;
  - Merumuskan masalah;
  - Merumuskan hipotesis;
  - Mengumpulkan data;
  - Penguatan konsep;
  - Menguji hipotesis;
  - Menarik kesimpulan;
  - Feedback dan refleksi.

## 5. Halaman Guru

File yang diubah:

- `pages/8_Jawaban_Siswa.py`
- `pages/9_Feedback_Guru.py`

Perubahan utama:

- Judul halaman guru diperjelas menjadi hasil penyelidikan siswa.
- Istilah “tanggapan” pada detail feedback disesuaikan menjadi “hasil penyelidikan”.

## Catatan Teknis

- Struktur database tidak diubah.
- Kolom lama tetap digunakan:
  - `jawaban_1`
  - `jawaban_2`
  - `jawaban_3`
  - `kesimpulan`
- Data tambahan rumusan masalah dan hipotesis disimpan di dalam JSON `input_simulasi`.
- Semua file Python sudah dicek kompilasi dan tidak ada error sintaks.


## Revisi Tambahan

Bagian **Hasil Pengamatan** pada halaman simulasi telah dikembalikan seperti tampilan pada `awal.zip`, yaitu menggunakan judul **Hasil Pengamatan**, grafik/tabel langsung tampil, dan susunan status/keterangan mengikuti dokumen awal. Alur guided inquiry final tetap dipertahankan.
