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

role = st.session_state.get("role", "")


def tampilkan_tujuan_umum():
    section_title("Tujuan Web")

    info_card(
        "Media Pembelajaran Ekosistem",
        """
        Web ini dibuat sebagai media pembelajaran interaktif materi ekosistem untuk siswa SMA.
        Web mendukung model pembelajaran guided inquiry melalui alur membaca materi,
        menjalankan simulasi, menganalisis hasil simulasi, menulis tanggapan,
        menerima feedback, dan memantau progres belajar.
        """,
        "green-card"
    )


def tampilkan_simulasi_siswa():
    section_title("Jenis Simulasi yang Dapat Digunakan Siswa")

    info_card(
        "1. Simulasi Pencemaran Sungai",
        """
        Siswa menggunakan simulasi ini untuk memahami pengaruh pencemaran terhadap ekosistem sungai.
        Siswa dapat mengatur tingkat pencemaran limbah pabrik, lalu mengamati perubahan DO,
        kualitas air, makroinvertebrata, dan kondisi ekosistem sungai.
        """,
        "blue-card"
    )

    info_card(
        "2. Simulasi Aliran Energi dan Piramida Ekologi",
        """
        Siswa menggunakan simulasi ini untuk memahami perpindahan energi dari produsen
        ke konsumen tingkat I, konsumen tingkat II, dan konsumen tingkat III.
        Siswa dapat melihat bahwa energi semakin berkurang pada tingkat trofik yang lebih tinggi.
        """,
        "blue-card"
    )

    info_card(
        "3. Simulasi Daur Biogeokimia: Daur Air",
        """
        Siswa menggunakan simulasi ini untuk memahami proses daur air dalam ekosistem.
        Siswa dapat mengatur intensitas panas matahari, curah hujan, dan tutupan vegetasi,
        lalu mengamati perubahan evaporasi, kondensasi, presipitasi, infiltrasi,
        dan limpasan permukaan.
        """,
        "blue-card"
    )


def tampilkan_panduan_siswa():
    page_title(
        "📌 Panduan Siswa",
        "Halaman ini berisi panduan penggunaan web pembelajaran ekosistem khusus untuk siswa."
    )

    tampilkan_tujuan_umum()
    tampilkan_simulasi_siswa()

    section_title("Panduan Penggunaan untuk Siswa")

    info_card(
        "1. Login sebagai Siswa",
        """
        Siswa masuk melalui halaman login Google. Sistem akan membaca email siswa,
        kemudian memberikan akses jika akun siswa sudah aktif pada database.
        """,
        "green-card"
    )

    info_card(
        "2. Membaca Materi Ekosistem",
        """
        Siswa membuka halaman Materi Ekosistem, membaca materi yang tersedia,
        lalu menekan tombol Saya sudah membaca materi. Setelah tahap ini selesai,
        siswa baru dapat menjalankan simulasi.
        """,
        "green-card"
    )

    info_card(
        "3. Memilih dan Menjalankan Simulasi",
        """
        Siswa membuka halaman Simulasi Ekosistem. Pada halaman tersebut tersedia tiga simulasi,
        yaitu Pencemaran Sungai, Aliran Energi, dan Daur Air. Siswa memilih salah satu simulasi,
        mengatur nilai input, lalu menekan tombol Gunakan Simulasi.
        """,
        "green-card"
    )

    info_card(
        "4. Mengirim Tanggapan",
        """
        Setelah menjalankan simulasi, siswa membuka halaman Tanggapan Siswa.
        Pertanyaan guided inquiry akan menyesuaikan jenis simulasi yang dipilih.
        Siswa mengisi rumusan masalah, hasil pengamatan, analisis, dan kesimpulan.
        """,
        "green-card"
    )

    info_card(
        "5. Melihat Feedback Guru",
        """
        Setelah guru memberikan feedback, siswa dapat membuka halaman Feedback Siswa
        atau Dashboard Siswa untuk membaca komentar, saran, dan penilaian dari guru.
        """,
        "green-card"
    )

    section_title("Urutan Penggunaan Wajib untuk Siswa")

    info_card(
        "Alur Belajar Siswa",
        """
        Siswa harus mengikuti alur penggunaan secara berurutan. Siswa tidak dapat menjalankan simulasi
        sebelum menyelesaikan materi. Siswa juga tidak dapat mengirim tanggapan sebelum memilih
        dan menjalankan salah satu simulasi.
        """,
        "danger-card"
    )

    section_title("Catatan Penting untuk Siswa")

    info_card(
        "Gunakan Akun yang Sama",
        """
        Gunakan akun Google yang sama setiap kali login. Sistem membaca progres belajar,
        tanggapan, dan feedback berdasarkan identitas akun yang aktif pada database.
        """,
        "blue-card"
    )


def tampilkan_simulasi_guru():
    section_title("Informasi Simulasi yang Dipantau Guru")

    info_card(
        "1. Simulasi Pencemaran Sungai",
        """
        Guru dapat meninjau hasil simulasi siswa terkait pencemaran sungai,
        seperti tingkat pencemaran, perubahan kualitas air, DO, makroinvertebrata,
        dan kondisi ekosistem.
        """,
        "blue-card"
    )

    info_card(
        "2. Simulasi Aliran Energi dan Piramida Ekologi",
        """
        Guru dapat meninjau pemahaman siswa tentang perpindahan energi pada tingkat trofik.
        Hasil simulasi ini membantu guru melihat apakah siswa memahami bahwa energi
        semakin berkurang pada tingkat trofik yang lebih tinggi.
        """,
        "blue-card"
    )

    info_card(
        "3. Simulasi Daur Biogeokimia: Daur Air",
        """
        Guru dapat meninjau hasil pengamatan siswa terkait proses evaporasi, kondensasi,
        presipitasi, infiltrasi, dan limpasan permukaan pada simulasi daur air.
        """,
        "blue-card"
    )


def tampilkan_panduan_guru():
    page_title(
        "📌 Panduan Guru",
        "Halaman ini berisi panduan penggunaan web pembelajaran ekosistem khusus untuk guru."
    )

    tampilkan_tujuan_umum()
    tampilkan_simulasi_guru()

    section_title("Panduan Penggunaan untuk Guru")

    info_card(
        "1. Login sebagai Guru",
        """
        Guru masuk melalui halaman login Google. Nama guru dan role akses akan diambil
        dari data akun yang terdaftar pada database.
        """,
        "yellow-card"
    )

    info_card(
        "2. Melihat Dashboard Guru",
        """
        Dashboard Guru menampilkan ringkasan jumlah siswa, jumlah tanggapan,
        jumlah feedback, serta status tanggapan yang sudah dan belum diberi feedback.
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

    section_title("Alur Guided Inquiry yang Dipantau Guru")

    st.markdown("""
    | Tahap Guided Inquiry | Implementasi di Web |
    |---|---|
    | Orientasi masalah | Kasus pada masing-masing simulasi |
    | Eksplorasi konsep | Materi ekosistem yang dibaca siswa |
    | Pengumpulan data | Siswa menjalankan simulasi ekosistem |
    | Analisis data | Siswa menjawab pertanyaan pada halaman tanggapan |
    | Kesimpulan | Siswa menuliskan kesimpulan berdasarkan hasil simulasi |
    | Komunikasi hasil | Guru membaca jawaban siswa |
    | Feedback dan refleksi | Guru memberi feedback, siswa membaca feedback |
    """)

    section_title("Catatan Penting untuk Guru")

    info_card(
        "Pemantauan Progres Belajar",
        """
        Guru dapat menggunakan data progres siswa untuk melihat tahapan belajar yang sudah
        dan belum diselesaikan. Jika banyak siswa belum mengirim tanggapan,
        guru dapat memberi arahan kembali pada pertemuan pembelajaran.
        """,
        "blue-card"
    )


def tampilkan_panduan_admin():
    page_title(
        "📌 Panduan Admin",
        "Halaman ini menampilkan ringkasan panduan untuk admin, guru, dan siswa."
    )

    info_card(
        "Catatan Admin",
        """
        Admin dapat melihat panduan ini untuk memastikan alur penggunaan web sudah sesuai
        dengan kebutuhan pembelajaran. Panduan siswa dan guru tetap dipisahkan ketika pengguna
        login sesuai role masing-masing.
        """,
        "blue-card"
    )

    tampilkan_panduan_siswa()
    tampilkan_panduan_guru()


if role == "siswa":
    tampilkan_panduan_siswa()

elif role == "guru":
    tampilkan_panduan_guru()

elif role == "admin":
    tampilkan_panduan_admin()

else:
    st.warning("Role pengguna tidak dikenali. Silakan login ulang.")
