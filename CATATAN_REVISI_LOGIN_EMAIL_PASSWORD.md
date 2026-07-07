# Catatan Revisi Login Email & Password

Revisi ini menambahkan opsi login tanpa Google untuk memudahkan validasi media.

## Perubahan Utama

1. Halaman login sekarang memiliki form:
   - Email
   - Password
   - Tombol **Masuk dengan Email & Password**

2. Login Google tetap tersedia jika konfigurasi `[google_oauth]` di Streamlit Secrets masih diisi.
   Jika konfigurasi Google tidak tersedia, tombol Google tidak ditampilkan dan aplikasi tetap bisa dipakai dengan email & password.

3. Tabel `users` ditambah kolom:

```sql
alter table public.users add column if not exists password_hash text;
```

4. Menu Admin > Daftar Pengguna sekarang memiliki fitur:
   - Tambah akun email & password
   - Atur role: siswa, guru, admin
   - Atur status: aktif/nonaktif
   - Mengganti password pengguna

## Cara Membuat Akun Pengguna

1. Login sebagai admin.
2. Buka menu **Daftar Pengguna**.
3. Buka bagian **Tambah Akun Email & Password **.
4. Isi nama, email, password, role, status aktif, dan keterangan.
5. Klik **Buat Akun**.
6. Akun pengguna dapat langsung login dari halaman utama menggunakan email dan password tersebut.

## Catatan Penting

- Password disimpan dalam bentuk hash PBKDF2-SHA256, bukan teks biasa.
- Password minimal 6 karakter.
- Akun harus berstatus **aktif** agar bisa login.
- Untuk validasi media, role yang disarankan adalah `siswa` jika pengguna ingin melihat tampilan siswa, atau `guru` jika pengguna ingin melihat dashboard guru.
