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
        "1. Simulasi Pencemaran Sungai Akibat Limbah Pabrik",
        """
        Pada simulasi ini, siswa mengamati fenomena pencemaran sungai akibat masuknya limbah pabrik.
        Siswa dapat mengubah tingkat limbah industri, lalu melihat pengaruhnya terhadap kualitas air,
        oksigen terlarut atau DO, populasi ikan, indeks makroinvertebrata, dan kondisi ekosistem sungai.
        Simulasi ini membantu siswa memahami hubungan antara komponen abiotik dan biotik dalam ekosistem perairan.
        """,
        "blue-card"
    )

    info_card(
        "2. Simulasi Rantai Makanan Saat Kemarau",
        """
        Pada simulasi ini, siswa mengamati fenomena berkurangnya rumput saat kemarau panjang.
        Rumput berperan sebagai produsen yang menjadi sumber energi bagi tingkat trofik berikutnya.
        Siswa dapat mengubah jumlah energi produsen, persentase penurunan rumput akibat kemarau,
        dan efisiensi perpindahan energi. Hasil simulasi menunjukkan perubahan energi pada produsen,
        konsumen I, konsumen II, dan konsumen III.
        """,
        "blue-card"
    )

    info_card(
        "3. Simulasi Daur Air, CO2, dan O2 Saat Pohon Berkurang",
        """
        Pada simulasi ini, siswa mengamati fenomena berkurangnya pohon atau tutupan vegetasi.
        Siswa dapat mengubah curah hujan dan tutupan vegetasi setelah penebangan, lalu melihat pengaruhnya
        terhadap infiltrasi, limpasan permukaan, penyerapan karbon dioksida atau CO2, dan produksi oksigen atau O2.
        Simulasi ini membantu siswa memahami peran tumbuhan dalam menjaga keseimbangan daur air,
        karbon dioksida, dan oksigen.
        """,
        "blue-card"
    )

    info_card(
        "4. Simulasi Peningkatan Alga Akibat Pupuk Berlebih",
        """
        Pada simulasi ini, siswa mengamati fenomena masuknya pupuk pertanian secara berlebihan ke perairan.
        Siswa dapat mengubah kadar nitrogen dan fosfor dari pupuk, lalu melihat pengaruhnya terhadap
        zat hara, pertumbuhan alga, oksigen air, dan kondisi organisme air.
        Simulasi ini membantu siswa memahami peristiwa eutrofikasi dan dampaknya terhadap keseimbangan ekosistem perairan.
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
        "Alur Belajar Berbasis Guided Inquiry yang Ramah Siswa",
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
        "1. Simulasi Pencemaran Sungai Akibat Limbah Pabrik",
        """
        Guru dapat meninjau hasil penyelidikan siswa terkait fenomena pencemaran sungai
        akibat limbah pabrik. Data yang dapat diamati meliputi tingkat pencemaran,
        kualitas air, oksigen terlarut atau DO, populasi ikan, indeks makroinvertebrata,
        dan kondisi ekosistem sungai. Melalui simulasi ini, guru dapat melihat kemampuan
        siswa dalam menghubungkan perubahan komponen abiotik dengan dampaknya terhadap
        organisme perairan.
        """,
        "blue-card"
    )

    info_card(
        "2. Simulasi Rantai Makanan Saat Kemarau",
        """
        Guru dapat meninjau pemahaman siswa tentang pengaruh kemarau terhadap ketersediaan
        produsen dalam rantai makanan. Data yang dapat diamati meliputi energi produsen,
        penurunan rumput akibat kemarau, efisiensi perpindahan energi, serta energi pada
        konsumen I, konsumen II, dan konsumen III. Simulasi ini membantu guru melihat
        apakah siswa memahami bahwa perubahan pada produsen dapat memengaruhi tingkat
        trofik berikutnya.
        """,
        "blue-card"
    )

    info_card(
        "3. Simulasi Daur Air, Karbon Dioksida, dan Oksigen Saat Pohon Berkurang",
        """
        Guru dapat meninjau hasil penyelidikan siswa tentang pengaruh berkurangnya pohon
        atau tutupan vegetasi terhadap keseimbangan lingkungan. Data yang dapat diamati
        meliputi curah hujan, tutupan vegetasi, infiltrasi, limpasan permukaan,
        penyerapan karbon dioksida atau CO2, dan produksi oksigen atau O2. Simulasi ini
        membantu guru menilai kemampuan siswa dalam memahami peran tumbuhan terhadap
        daur air, siklus karbon, dan ketersediaan oksigen.
        """,
        "blue-card"
    )

    info_card(
        "4. Simulasi Peningkatan Alga Akibat Pupuk Berlebih",
        """
        Guru dapat meninjau hasil penyelidikan siswa tentang masuknya pupuk pertanian
        secara berlebihan ke perairan. Data yang dapat diamati meliputi kadar nitrogen,
        fosfor, pertumbuhan alga, oksigen air, dan kondisi organisme air. Simulasi ini
        membantu guru melihat pemahaman siswa mengenai proses eutrofikasi dan dampaknya
        terhadap keseimbangan ekosistem perairan.
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

    section_title("Alur Guided Inquiry")

    st.markdown(
        """
        | Tahap Guided Inquiry | Implementasi di Web |
        |---|---|
        | Orientasi | Siswa menelaah fenomena ekosistem yang disajikan pada halaman simulasi. |
        | Merumuskan masalah | Siswa merumuskan sendiri pertanyaan ilmiah berdasarkan fenomena dan variabel yang tersedia. |
        | Merumuskan hipotesis | Siswa menyusun dugaan sementara disertai alasan ilmiah berdasarkan konsep ekologi. |
        | Mengumpulkan data | Siswa menjalankan simulasi, memanipulasi variabel, dan membaca grafik/tabel hasil simulasi. |
        | Menganalisis/menguji hipotesis | Siswa membandingkan data dengan hipotesis untuk menentukan apakah hipotesis didukung atau tidak. |
        | Menarik kesimpulan | Siswa membuat kesimpulan yang menjawab rumusan masalah dan didukung oleh data. |
        | Feedback dan refleksi | Guru memberi feedback terhadap ketepatan konsep, bukti data, dan argumentasi siswa. |
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
