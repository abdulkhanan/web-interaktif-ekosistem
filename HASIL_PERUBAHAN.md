# Hasil Perubahan P2

## Fokus perubahan

Skema login dan konstruksi halaman dari P1 sudah diterapkan ke P2. Logika dan bentuk simulasi yang dijalankan pada P2 tidak diubah.

## File yang diubah atau ditambah

1. `app.py`
   - Diubah menjadi halaman login utama berbasis Google OAuth.
   - Menambahkan redirect otomatis berdasarkan role:
     - `admin` ke `pages/Admin.py`
     - `guru` ke `pages/6_Dashboard_Guru.py`
     - `siswa` ke `pages/1_Dashboard_Siswa.py`

2. `modules/auth.py`
   - Login manual sidebar P2 diganti dengan skema Google OAuth dari P1.
   - Menambahkan session state untuk `logged_in`, `id_user`, `nama_pengguna`, `email`, `role`, dan `kelas`.
   - Menambahkan validasi akses melalui `require_role()`.
   - Menambahkan fungsi `logout()`.

3. `database/init_db.py`
   - Menambahkan tabel `users` untuk menyimpan akun, email, role, kelas, status, dan identitas Google.
   - Tabel lama P2 tetap dipertahankan:
     - `tanggapan_siswa`
     - `feedback_guru`
     - `progress_siswa`
     - `progress_materi`

4. `database/queries.py`
   - Menambahkan fungsi manajemen user:
     - `get_user_by_email()`
     - `get_or_create_google_user()`
     - `create_user_manual()`
     - `get_users_df()`
     - `update_user_role_status()`
     - `get_user_counts()`
   - Fungsi lama untuk tanggapan, feedback, progres, dan materi tetap dipertahankan.

5. `components/ui.py`
   - Menambahkan gaya login P1.
   - Menambahkan gaya halaman berbasis kartu hero.
   - Menambahkan navigasi role di bagian atas halaman.
   - Sidebar Streamlit disembunyikan agar alur halaman mengikuti konstruksi P1.

6. `pages/Admin.py`
   - Menambahkan halaman admin untuk mengelola user.
   - Admin dapat melihat ringkasan user, daftar user, tambah user, serta mengubah role dan status user.

7. Halaman siswa dan guru P2
   - Menambahkan navigasi role di bagian atas halaman.
   - Menjaga akses berdasarkan role.
   - Halaman yang tetap digunakan:
     - `pages/1_Dashboard_Siswa.py`
     - `pages/2_Materi_Ekosistem.py`
     - `pages/3_Simulasi_Ekosistem.py`
     - `pages/4_Tanggapan_Siswa.py`
     - `pages/5_Feedback_Siswa.py`
     - `pages/6_Dashboard_Guru.py`
     - `pages/7_Data_Siswa.py`
     - `pages/8_Jawaban_Siswa.py`
     - `pages/9_Feedback_Guru.py`
     - `pages/10_Panduan_Penggunaan.py`

8. `.streamlit/config.toml`
   - Ditambahkan konfigurasi untuk menyembunyikan navigasi sidebar Streamlit.

9. `.streamlit/secrets.toml`
   - Konfigurasi OAuth dari P1 diterapkan agar login Google dapat berjalan.
   - Nilai credential tidak ditulis ulang pada dokumen ini.

10. `requirements.txt`
    - Menambahkan dependency:
      - `authlib`
      - `requests`

## Bagian yang sengaja tidak diubah

1. `modules/simulation.py`
   - Tidak diubah.

2. Rumus dan output simulasi
   - Simulasi Pencemaran Sungai tetap menggunakan rumus dan tampilan lama.
   - Simulasi Aliran Energi tetap menggunakan rumus dan tampilan lama.
   - Simulasi Daur Air tetap menggunakan rumus dan tampilan lama.

3. `pages/3_Simulasi_Ekosistem.py`
   - Logika simulasi tidak diubah.
   - Perubahan hanya pada import dan pemanggilan navigasi role.

## Catatan koreksi

Jika ada bagian yang perlu dikoreksi, cek terlebih dahulu bagian berikut:

1. Jika login Google gagal, cek `.streamlit/secrets.toml` dan pastikan `redirect_uri` sama dengan URL aplikasi Streamlit.
2. Jika user berhasil login tetapi tidak dapat masuk, cek status akun pada halaman Admin. Status harus `aktif`.
3. Jika siswa belum dapat membuka simulasi, cek materi prasyarat pada halaman Materi Ekosistem.
4. Jika tombol halaman tidak muncul, cek fungsi `role_navigation()` pada `components/ui.py`.
5. Jika data siswa tidak muncul di guru, cek kesamaan nama pengguna yang tersimpan dari akun Google dengan data progres/tanggapan.
