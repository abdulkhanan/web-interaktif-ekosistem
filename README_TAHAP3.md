# Tahap 3: Misi 1 Guided Inquiry Lengkap

Tahap 3 mengaktifkan **Misi 1: Misteri Sungai yang Mulai Rusak** dari awal sampai akhir.

## Alur siswa

1. Orientasi fenomena
2. Merumuskan masalah
3. Menyusun hipotesis dan variabel
4. Melakukan minimal 3 percobaan berbeda
5. Menganalisis data dan menguji hipotesis
6. Menarik kesimpulan
7. Membaca penguatan konsep
8. Menulis refleksi dan aksi lingkungan

## File baru

- `components/inquiry_ui.py`
- `modules/mission_content.py`
- `README_TAHAP3.md`
- `CARA_PASANG_TAHAP3.txt`

## File yang diperbarui

- `database/queries.py`
- `pages/1_Dashboard_Siswa.py`
- `pages/2_Misi_Penyelidikan.py`
- `pages/3_Simulasi_Ekosistem.py`

## Database

Tidak ada SQL baru pada Tahap 3. Tahap ini memakai tabel yang sudah dibuat pada Tahap 1:

- `mission_progress`
- `inquiry_responses`
- `experiment_runs`

## Perilaku sementara selama pengembangan

Misi 1 aktif penuh. Misi 2, 3, dan 4 tetap tampil di dashboard, tetapi tombolnya dinonaktifkan sampai aktivitas lengkapnya dibangun pada tahap berikutnya.

## Tes utama

1. Login sebagai siswa.
2. Mulai Misi 1.
3. Isi fenomena, masalah, dan hipotesis.
4. Simpan minimal tiga percobaan dengan tingkat limbah berbeda.
5. Lengkapi analisis dan uji hipotesis.
6. Simpan kesimpulan.
7. Pastikan status Misi 1 menjadi `selesai` di Supabase.
8. Simpan refleksi dan aksi lingkungan.
