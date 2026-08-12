# Perbaikan Import `delete_user_account`

Error pada `pages/Admin.py` terjadi ketika halaman Admin memanggil `delete_user_account` tetapi deployment masih membaca `database/queries.py` versi lama.

Perbaikan:
- `Admin.py` tidak lagi gagal start bila `delete_user_account` belum tersedia di `database.queries`; tersedia fallback langsung ke Supabase.
- `modules/auth.py` juga kompatibel bila `get_user_by_id` belum tersedia di `database.queries`.
- `database/queries.py` tetap memiliki implementasi utama `delete_user_account` dan `get_user_by_id`.
- Admin yang sedang login tetap tidak dapat menghapus akun dirinya sendiri.
- Data pembelajaran tidak ikut dihapus.
