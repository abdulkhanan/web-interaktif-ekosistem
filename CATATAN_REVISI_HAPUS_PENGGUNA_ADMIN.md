# Revisi: Admin dapat menghapus akun pengguna

Perubahan yang ditambahkan:

- Tombol **Hapus** pada setiap kartu pengguna di menu **Admin > Daftar Pengguna**.
- Konfirmasi sebelum penghapusan untuk mencegah penghapusan tidak sengaja.
- Admin yang sedang login tidak dapat menghapus akunnya sendiri.
- Penghapusan hanya menghapus akun pada tabel `users`; tanggapan, progres, dan feedback pembelajaran tetap dipertahankan.
- Sesi pengguna divalidasi ulang ke database. Jika akun dihapus atau dibuat nonaktif oleh admin, akses pengguna akan dicabut pada interaksi/navigasi berikutnya.
- Pengguna login Google yang dihapus dapat muncul kembali sebagai akun baru/nonaktif jika mencoba login Google lagi, sesuai mekanisme auto-registration yang sudah ada. Akses tetap tidak aktif sampai admin mengaktifkannya.
