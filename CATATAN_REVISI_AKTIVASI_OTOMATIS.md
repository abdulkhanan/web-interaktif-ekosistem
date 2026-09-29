# Catatan Revisi — Fitur Aktivasi Otomatis Pendaftaran

## Latar Belakang

Sebelumnya, setiap akun baru yang mendaftar (baik melalui email/password maupun Google OAuth) selalu berstatus **nonaktif** dan harus diaktifkan manual oleh admin satu per satu. Revisi ini menambahkan fitur **toggle "Mode Aktivasi Otomatis"** di Dashboard Admin.

## Perubahan yang Dilakukan

### 1. Database Schema (`supabase_schema.sql`)
- Ditambahkan tabel baru `app_settings` untuk menyimpan pengaturan aplikasi.
- Default setting `auto_aktivasi` = `false`.

**⚠️ PENTING**: Jalankan SQL berikut di Supabase SQL Editor:

```sql
create table if not exists public.app_settings (
    setting_key text primary key,
    setting_value text not null default '',
    updated_at text
);

insert into public.app_settings (setting_key, setting_value, updated_at)
values ('auto_aktivasi', 'false', now()::text)
on conflict (setting_key) do nothing;
```

### 2. Database Queries (`database/queries.py`)
- Ditambahkan fungsi `get_app_setting()`, `set_app_setting()`, dan `is_auto_aktivasi()`.
- `get_or_create_google_user()` menerima parameter `auto_aktivasi` untuk menentukan status akun baru.

### 3. Admin Dashboard (`pages/Admin.py`)
- Ditambahkan kartu **"⚡ Mode Aktivasi Otomatis"** di Dashboard Admin.
- Terdapat toggle checkbox untuk mengaktifkan/menonaktifkan mode ini.
- Menampilkan badge status aktif/nonaktif secara visual.

### 4. Halaman Login (`app.py`)
- Tab "Daftar Akun" sekarang membaca setting `auto_aktivasi`.
- Jika mode aktif → status akun baru = `aktif`, pesan sukses menginformasikan bisa langsung login.
- Jika mode nonaktif → status akun baru = `nonaktif`, pesan sukses menginformasikan menunggu aktivasi admin.

### 5. Google OAuth (`modules/auth.py`)
- `handle_google_callback()` meneruskan status `auto_aktivasi` ke `get_or_create_google_user()`.
- Akun Google baru juga mengikuti pengaturan ini.

## Alur Kerja

### Mode Aktivasi Otomatis AKTIF:
1. Siswa mendaftar → status langsung **aktif**
2. Siswa login → langsung masuk **Dashboard Siswa**

### Mode Aktivasi Otomatis NONAKTIF (default):
1. Siswa mendaftar → status **nonaktif**
2. Admin harus mengaktifkan via menu Daftar Pengguna → Edit → Status → Aktif
3. Setelah diaktifkan, siswa bisa login ke Dashboard Siswa
