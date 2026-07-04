# Migrasi Fondasi Guided Inquiry

Perubahan ini menambahkan fondasi data baru tanpa menghapus tabel lama. Aplikasi lama tetap dapat berjalan selama halaman baru belum diaktifkan.

## 1. Jalankan migration di Supabase

Buka **Supabase Dashboard → SQL Editor → New query**. Salin seluruh isi:

`database/migrations/001_guided_inquiry.sql`

Lalu klik **Run**.

Migration membuat tiga tabel:

- `mission_progress`, progres setiap siswa pada empat misi;
- `inquiry_responses`, jawaban siswa pada sintaks guided inquiry;
- `experiment_runs`, seluruh percobaan simulasi yang disimpan siswa.

## 2. Verifikasi tabel

Di **Table Editor**, pastikan ketiga tabel muncul. Tabel lama seperti `progress_siswa`, `tanggapan_siswa`, dan `progress_materi` tidak dihapus.

## 3. Uji dari aplikasi

Lapisan query baru sudah ditambahkan ke `database/queries.py`. Belum ada halaman lama yang wajib memakai fungsi baru, sehingga deployment tetap kompatibel.

Fungsi utama yang tersedia:

- `initialize_mission_progress(id_user)`
- `get_mission_progress_df(id_user)`
- `start_mission(id_user, mission_code)`
- `advance_mission_stage(id_user, mission_code, completed_stage)`
- `complete_mission(id_user, mission_code)`
- `save_inquiry_response(id_user, mission_code, **fields)`
- `get_inquiry_response(id_user, mission_code)`
- `save_experiment_run(...)`
- `get_experiment_runs_df(id_user, mission_code)`

## 4. Keamanan data

Sistem baru menggunakan `id_user` sebagai identitas utama. Nama siswa tetap dapat ditampilkan di antarmuka, tetapi tidak lagi menjadi kunci relasi progres.
