# Panduan Deploy Streamlit Community Cloud + Supabase

## 1. Buat tabel di Supabase

1. Buka Supabase Dashboard.
2. Masuk ke project.
3. Buka SQL Editor.
4. Jalankan isi file `supabase_schema.sql`.

## 2. Isi Secrets di Streamlit Cloud

Gunakan contoh dari `.streamlit/secrets.toml.example`.
Jangan upload `secrets.toml` asli ke GitHub.

Format minimal:

```toml
[google_oauth]
client_id = "..."
client_secret = "..."
redirect_uri = "https://NAMA-APP.streamlit.app"
default_admin_email = "email-admin@contoh.com"

[auth_cookie]
secret_key = "random-secret-panjang"

[supabase]
url = "https://PROJECT_ID.supabase.co"
key = "sb_secret_xxx_atau_service_role_key"
```

## 3. Update Google OAuth Redirect URI

Di Google Cloud Console, tambahkan redirect URI sesuai alamat aplikasi Streamlit:

```text
https://NAMA-APP.streamlit.app
```

Nilai ini harus sama dengan `redirect_uri` di Secrets Streamlit.

## 4. Upload ke GitHub

Pastikan file ini ada di repository:

- `app.py`
- folder `pages/`
- folder `modules/`
- folder `components/`
- folder `database/`
- folder `assets/`
- folder `data/` untuk `materi_ekosistem.json`
- `requirements.txt`
- `supabase_schema.sql`

Jangan upload:

- `.streamlit/secrets.toml`
- `data/ekosistem.db`
- folder `__pycache__`

## 5. Deploy di Streamlit Community Cloud

1. Buka Streamlit Community Cloud.
2. Pilih repository GitHub.
3. Pilih branch.
4. Main file path: `app.py`.
5. Buka Advanced settings.
6. Tempel isi Secrets.
7. Klik Deploy.

## Catatan penting

Versi ini sudah tidak memakai SQLite sebagai penyimpanan utama. Data user, tanggapan, feedback, dan progress siswa akan masuk ke Supabase.
