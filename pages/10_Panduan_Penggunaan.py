import streamlit as st
from modules.auth import require_role
from components.ui import load_css, page_title, section_title, info_card, role_navigation

st.set_page_config(
    page_title="Panduan Penggunaan",
    page_icon="📌",
    layout="wide"
)

load_css()
require_role(["admin", "guru", "siswa"])
role_navigation()

page_title(
    "📌 Panduan Penggunaan Web",
    "Halaman ini menjelaskan cara menggunakan web pembelajaran ekosistem untuk role siswa dan guru."
)

section_title("Tujuan Web")

info_card(
    "Media Pembelajaran Ekosistem",
    """
    Web ini dibuat sebagai media pembelajaran interaktif materi ekosistem untuk siswa SMA.
    Web mendukung model pembelajaran guided inquiry melalui alur membaca materi,
    memilih simulasi, menganalisis hasil simulasi, menulis tanggapan, menerima feedback,
    dan memantau progres belajar.
    """,
    "green-card"
)

section_title("Jenis Simulasi yang Tersedia")

info_card(
    "1. Simulasi Pencemaran Sungai",
    """
    Simulasi ini digunakan untuk memahami interaksi antarkomponen ekosistem.
    Siswa dapat mengatur tingkat pencemaran limbah pabrik, lalu mengamati perubahan
    pada DO, kualitas air, makroinvertebrata, dan kondisi ekosistem sungai.
    """,
    "blue-card"
)

info_card(
    "2. Simulasi Aliran Energi dan Piramida Ekologi",
    """
    Simulasi ini digunakan untuk memahami perpindahan energi dari produsen
    ke konsumen tingkat I, konsumen tingkat II, dan konsumen tingkat III.
    Siswa dapat melihat bahwa energi semakin berkurang pada tingkat trofik yang lebih tinggi.
    """,
    "blue-card"
)

info_card(
    "3. Simulasi Daur Biogeokimia: Daur Air",
    """
    Simulasi ini digunakan untuk memahami proses daur air dalam ekosistem.
    Siswa dapat mengatur intensitas panas matahari, curah hujan, dan tutupan vegetasi,
    lalu mengamati perubahan evaporasi, kondensasi, presipitasi, infiltrasi,
    dan limpasan permukaan.
    """,
    "blue-card"
)

section_title("Panduan untuk Siswa")

info_card(
    "1. Login sebagai Siswa",
    """
    Siswa masuk melalui halaman login Google. Sistem membaca email siswa, lalu memberi akses jika akun sudah aktif pada database.
    """,
    "green-card"
)

info_card(
    "2. Membaca Materi Ekosistem",
    """
    Siswa membuka halaman Materi Ekosistem, membaca materi, lalu menekan tombol
    Saya sudah membaca materi. Setelah tahap ini selesai, siswa baru dapat menjalankan simulasi.
    """,
    "green-card"
)

info_card(
    "3. Memilih dan Menjalankan Simulasi",
    """
    Siswa membuka halaman Simulasi Ekosistem. Pada halaman tersebut tersedia tiga tab simulasi,
    yaitu Pencemaran Sungai, Aliran Energi, dan Daur Air. Siswa memilih salah satu simulasi,
    mengatur nilai input, lalu menekan tombol Gunakan Simulasi.
    """,
    "green-card"
)

info_card(
    "4. Mengirim Tanggapan",
    """
    Setelah memilih simulasi, siswa membuka halaman Tanggapan Siswa.
    Pertanyaan guided inquiry akan menyesuaikan jenis simulasi yang dipilih.
    Siswa mengisi rumusan masalah, hasil pengamatan, analisis, dan kesimpulan.
    """,
    "green-card"
)

info_card(
    "5. Melihat Feedback Guru",
    """
    Setelah guru memberikan feedback, siswa dapat membuka halaman Feedback Siswa
    atau Dashboard Siswa untuk membaca komentar dari guru.
    """,
    "green-card"
)

section_title("Panduan untuk Guru")

info_card(
    "1. Login sebagai Guru",
    """
    Guru masuk melalui halaman login Google. Nama guru dan role akses diambil dari data akun yang terdaftar pada database.
    """,
    "yellow-card"
)

info_card(
    "2. Melihat Dashboard Guru",
    """
    Dashboard Guru menampilkan jumlah siswa, jumlah tanggapan, jumlah feedback,
    serta status tanggapan yang sudah dan belum diberi feedback.
    """,
    "yellow-card"
)

info_card(
    "3. Melihat Progres Siswa",
    """
    Guru membuka halaman Data Siswa untuk melihat progres belajar setiap siswa.
    Progres mencakup status membaca materi, menjalankan simulasi, mengirim tanggapan,
    dan menerima feedback.
    """,
    "yellow-card"
)

info_card(
    "4. Membaca Jawaban Siswa",
    """
    Guru membuka halaman Jawaban Siswa untuk membaca hasil analisis siswa.
    Guru dapat memfilter jawaban berdasarkan status feedback, jenis simulasi,
    atau nama siswa.
    """,
    "yellow-card"
)

info_card(
    "5. Memberikan Feedback",
    """
    Guru membuka halaman Feedback Guru, memilih tanggapan siswa, membaca hasil simulasi
    dan jawaban guided inquiry, lalu memberikan feedback. Setelah feedback dikirim,
    siswa dapat melihatnya pada halaman Feedback Siswa.
    """,
    "yellow-card"
)

section_title("Alur Guided Inquiry dalam Web")

st.markdown("""
| Tahap Guided Inquiry | Implementasi di Web |
|---|---|
| Orientasi masalah | Kasus pada masing-masing simulasi |
| Eksplorasi konsep | Materi ekosistem |
| Pengumpulan data | Simulasi pencemaran sungai, aliran energi, atau daur air |
| Analisis data | Pertanyaan pada halaman tanggapan siswa |
| Kesimpulan | Kolom kesimpulan siswa |
| Komunikasi hasil | Guru membaca jawaban siswa |
| Feedback dan refleksi | Guru memberi feedback, siswa membaca feedback |
""")

section_title("Urutan Penggunaan Wajib")

info_card(
    "Urutan untuk Siswa",
    """
    Siswa harus mengikuti alur secara berurutan. Siswa tidak dapat menjalankan simulasi
    sebelum menyelesaikan materi. Siswa juga tidak dapat mengirim tanggapan sebelum memilih
    dan menjalankan salah satu simulasi.
    """,
    "danger-card"
)

section_title("Catatan Penting")

info_card(
    "Nama Pengguna",
    """
    Gunakan akun Google yang sama ketika login. Sistem membaca progres, tanggapan, dan feedback berdasarkan identitas akun yang aktif pada database.
    """,
    "blue-card"
)
