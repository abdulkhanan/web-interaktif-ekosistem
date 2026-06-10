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
        "Media Pembelajaran Ekosistem Berbasis Guided Inquiry",
        """
        Web ini dibuat sebagai media pembelajaran interaktif materi ekosistem berbasis guided inquiry.
        Alur pembelajaran dimulai dari penyajian fenomena atau masalah pada halaman simulasi.
        Siswa mengamati fenomena tersebut melalui pertanyaan pemantik, kemudian menjalankan simulasi
        untuk memperoleh data. Selama proses penyelidikan, siswa dapat menggunakan materi ekosistem
        sebagai bahan pendukung untuk memahami konsep dan menafsirkan hasil simulasi. Setelah melakukan
        penyelidikan, siswa menulis tanggapan berupa hasil pengamatan, analisis, dan kesimpulan.
        Tanggapan tersebut kemudian ditinjau oleh guru, lalu siswa menerima feedback sebagai bahan
        refleksi dan perbaikan pemahaman.
        """,
        "green-card"
    )


def tampilkan_simulasi_siswa():
    section_title("Jenis Simulasi yang Dapat Digunakan Siswa")

    info_card(
        "1. Simulasi Pencemaran Sungai",
        """
        Siswa menggunakan simulasi ini untuk menyelidiki pengaruh pencemaran terhadap ekosistem sungai.
        Siswa dapat mengatur tingkat pencemaran limbah pabrik, lalu mengamati perubahan DO,
        kualitas air, makroinvertebrata, dan kondisi ekosistem sungai.
        """,
        "blue-card"
    )

    info_card(
        "2. Simulasi Aliran Energi dan Piramida Ekologi",
        """
        Siswa menggunakan simulasi ini untuk menyelidiki perpindahan energi dari produsen
        ke konsumen tingkat I, konsumen tingkat II, dan konsumen tingkat III. Melalui simulasi ini,
        siswa dapat melihat bahwa energi semakin berkurang pada tingkat trofik yang lebih tinggi.
        """,
        "blue-card"
    )

    info_card(
        "3. Simulasi Daur Biogeokimia: Daur Air",
        """
        Siswa menggunakan simulasi ini untuk menyelidiki proses daur air dalam ekosistem.
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
        "2. Mengamati Fenomena pada Simulasi",
        """
        Setelah login, siswa membuka halaman Simulasi Ekosistem. Pada halaman tersebut,
        siswa akan menemukan fenomena atau permasalahan ekosistem yang harus diamati.
        Fenomena ini menjadi dasar awal bagi siswa untuk melakukan penyelidikan.
        """,
        "green-card"
    )

    info_card(
        "3. Menjalankan Simulasi",
        """
        Siswa memilih salah satu simulasi, yaitu Pencemaran Sungai, Aliran Energi,
        atau Daur Air. Setelah itu, siswa mengatur variabel simulasi dan mengamati
        perubahan data yang muncul. Data dari simulasi digunakan sebagai bahan untuk
        menjawab fenomena atau permasalahan yang disajikan.
        """,
        "green-card"
    )

    info_card(
        "4. Menggunakan Materi sebagai Bahan Penyelidikan",
        """
        Selama proses penyelidikan, siswa dapat membuka halaman Materi Ekosistem.
        Materi pada halaman tersebut digunakan untuk membantu siswa memahami konsep ekosistem,
        menghubungkan teori dengan hasil simulasi, dan memperkuat analisis terhadap fenomena.
        """,
        "green-card"
    )

    info_card(
        "5. Mengirim Tanggapan",
        """
        Setelah menjalankan simulasi dan melakukan penyelidikan, siswa membuka halaman Tanggapan Siswa.
        Pertanyaan guided inquiry akan menyesuaikan jenis simulasi yang dipilih. Siswa mengisi hasil
        pengamatan, analisis, dan kesimpulan berdasarkan data simulasi serta pemahaman dari materi
        ekosistem sebagai bahan penyelidikan.
        """,
        "green-card"
    )

    info_card(
        "6. Melihat Feedback Guru",
        """
        Setelah guru memberikan feedback, siswa dapat membuka halaman Feedback Siswa
        atau Dashboard Siswa untuk membaca komentar, saran, dan penilaian dari guru.
        Feedback tersebut digunakan sebagai bahan refleksi untuk memperbaiki pemahaman siswa.
        """,
        "green-card"
    )

    section_title("Urutan Penggunaan untuk Siswa")

    info_card(
        "Alur Belajar Berbasis Guided Inquiry",
        """
        Siswa memulai kegiatan belajar dengan mengamati fenomena pada halaman simulasi.
        Setelah itu, siswa menjalankan simulasi untuk memperoleh data dan menggunakan materi ekosistem
        sebagai bahan penyelidikan untuk membantu memahami konsep yang berkaitan dengan fenomena tersebut.
        Setelah proses penyelidikan selesai, siswa menulis tanggapan berdasarkan hasil pengamatan,
        analisis, dan kesimpulan. Siswa baru dapat mengirim tanggapan setelah memilih dan menjalankan
        salah satu simulasi.
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
        Progres mencakup status menjalankan simulasi, mengirim tanggapan,
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

    st.markdown(
        """
        | Tahap Guided Inquiry | Implementasi di Web |
        |---|---|
        | Orientasi masalah | Siswa mengamati fenomena atau masalah pada halaman simulasi |
        | Pertanyaan pemantik | Siswa membaca pertanyaan yang berkaitan dengan fenomena ekosistem |
        | Penyelidikan | Siswa menjalankan simulasi dengan mengatur variabel yang tersedia |
        | Pengumpulan data | Siswa mengamati hasil perubahan data dari simulasi |
        | Penguatan konsep | Siswa menggunakan materi ekosistem sebagai bahan penyelidikan |
        | Analisis data | Siswa menjawab pertanyaan pada halaman Tanggapan Siswa |
        | Kesimpulan | Siswa menuliskan kesimpulan berdasarkan hasil simulasi dan materi pendukung |
        | Feedback dan refleksi | Guru memberi feedback, lalu siswa menggunakan feedback untuk memperbaiki pemahaman |
        """
    )

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
        "Admin dapat memilih jenis panduan yang ingin ditinjau."
    )

    pilihan_panduan = st.radio(
        "Pilih panduan yang ingin ditampilkan:",
        ["Panduan Siswa", "Panduan Guru"],
        horizontal=True
    )

    if pilihan_panduan == "Panduan Siswa":
        tampilkan_panduan_siswa()
    else:
        tampilkan_panduan_guru()


if role == "siswa":
    tampilkan_panduan_siswa()
elif role == "guru":
    tampilkan_panduan_guru()
elif role == "admin":
    tampilkan_panduan_admin()
else:
    st.warning("Role pengguna tidak dikenali. Silakan login ulang.")
