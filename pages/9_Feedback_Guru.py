import streamlit as st
from datetime import datetime
from database.init_db import init_db
from database.queries import (
    get_tanggapan_status_df,
    insert_feedback,
    update_progress
)
from modules.auth import require_role
from components.ui import (
    role_navigation,
    load_css,
    page_title,
    section_title,
    info_card,
    feedback_status_card,
    generic_simulation_result_view,
    guided_inquiry_answer_view_generic
)

init_db()

st.set_page_config(
    page_title="Feedback Guru",
    page_icon="✍️",
    layout="wide"
)

load_css()
require_role(["guru"])
role_navigation()

nama_guru = st.session_state.get("nama_pengguna", "")

page_title(
    "✍️ Feedback Guru",
    "Guru memberikan feedback terhadap literasi sains dan sikap peduli lingkungan siswa."
)

info_card(
    "Guru yang Memberi Feedback",
    nama_guru,
    "green-card"
)

df_tanggapan = get_tanggapan_status_df()

if df_tanggapan.empty:
    info_card(
        "Belum Ada Tanggapan",
        "Belum ada tanggapan siswa yang dapat diberi feedback.",
        "yellow-card"
    )

else:
    section_title("Pilih Tanggapan")

    status_filter = st.selectbox(
        "Tampilkan tanggapan",
        ["Belum diberi feedback", "Semua", "Sudah diberi feedback"],
        key="feedback_guru_status_filter"
    )

    if status_filter != "Semua":
        df_tanggapan = df_tanggapan[
            df_tanggapan["status_feedback"] == status_filter
        ]

    if df_tanggapan.empty:
        info_card(
            "Tidak Ada Data",
            "Tidak ada tanggapan pada status feedback yang dipilih.",
            "yellow-card"
        )
        st.stop()

    daftar_simulasi = ["Semua"] + sorted(
        df_tanggapan["jenis_simulasi"].dropna().unique().tolist()
    )

    simulasi_filter = st.selectbox(
        "Filter jenis simulasi",
        daftar_simulasi,
        key="feedback_guru_simulasi_filter"
    )

    if simulasi_filter != "Semua":
        df_tanggapan = df_tanggapan[
            df_tanggapan["jenis_simulasi"] == simulasi_filter
        ]

    if df_tanggapan.empty:
        info_card(
            "Tidak Ada Data",
            "Tidak ada tanggapan pada jenis simulasi yang dipilih.",
            "yellow-card"
        )
        st.stop()

    daftar_tanggapan = []

    for index, row in df_tanggapan.iterrows():
        label = (
            f"{row['id_tanggapan']} | "
            f"{row['nama']} | "
            f"{row['jenis_simulasi']} | "
            f"{row['waktu']} | "
            f"{row['status_feedback']}"
        )
        daftar_tanggapan.append(label)

    pilihan = st.selectbox(
        "Pilih tanggapan siswa",
        daftar_tanggapan,
        key="feedback_guru_pilih_tanggapan"
    )

    if pilihan:
        id_terpilih = pilihan.split(" | ")[0]

        data_terpilih = df_tanggapan[
            df_tanggapan["id_tanggapan"].astype(str) == id_terpilih
        ].iloc[0]

        section_title("Detail Hasil Penyelidikan Siswa")

        feedback_status_card(data_terpilih["status_feedback"])

        col1, col2, col3 = st.columns(3)

        with col1:
            info_card(
                "Nama Siswa",
                data_terpilih["nama"],
                "green-card"
            )

        with col2:
            info_card(
                "Jenis Simulasi",
                data_terpilih["jenis_simulasi"],
                "blue-card"
            )

        with col3:
            info_card(
                "Waktu Tanggapan",
                data_terpilih["waktu"],
                "yellow-card"
            )

        section_title("Ringkasan Simulasi")
        generic_simulation_result_view(data_terpilih)

        section_title("Jawaban Siswa")
        guided_inquiry_answer_view_generic(data_terpilih)

        section_title("Panduan Feedback Guru")

        col1, col2 = st.columns(2)

        with col1:
            info_card(
                "Literasi Siswa ",
                """
                Berikan komentar tentang kemampuan siswa dalam menjelaskan fenomena,
                membaca data, menggunakan bukti, dan menarik kesimpulan ilmiah.
                """,
                "blue-card"
            )

        with col2:
            info_card(
                "Sikap Siswa Terhadap Lingkungan",
                """
                Berikan komentar tentang kepedulian siswa terhadap masalah lingkungan,
                tindakan nyata, dan komitmen menjaga lingkungan.
                """,
                "green-card"
            )

        section_title("Form Feedback Guru")

        form_key = f"form_feedback_guru_{id_terpilih}"

        with st.form(key=form_key):
            feedback_literasi = st.text_area(
                "Literasi Siswa",
                placeholder="Contoh: Siswa sudah mampu membaca hubungan antara limbah dan penurunan DO, tetapi perlu menambahkan bukti data dari grafik.",
                key=f"feedback_literasi_{id_terpilih}"
            )

            feedback_sikap = st.text_area(
                "Sikap Siswa Terhadap Lingkungan",
                placeholder="Contoh: Siswa sudah menunjukkan kepedulian lingkungan, tetapi tindakan nyata perlu dibuat lebih spesifik.",
                key=f"feedback_sikap_{id_terpilih}"
            )

            submit = st.form_submit_button("Kirim Feedback")

            if submit:
                if not feedback_literasi or not feedback_sikap:
                    st.error(
                        "Feedback literasi sains dan feedback sikap peduli lingkungan harus diisi."
                    )
                else:
                    isi_feedback = (
                        "Aspek Literasi Sains:\n"
                        f"{feedback_literasi}\n\n"
                        "Aspek Sikap Peduli Lingkungan:\n"
                        f"{feedback_sikap}"
                    )

                    data_feedback = {
                        "id_feedback": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                        "id_tanggapan": data_terpilih["id_tanggapan"],
                        "waktu_feedback": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "nama_siswa": data_terpilih["nama"],
                        "nama_guru": nama_guru,
                        "isi_feedback": isi_feedback
                    }

                    insert_feedback(data_feedback)
                    update_progress(data_terpilih["nama"], "feedback_diterima")

                    info_card(
                        "Feedback Berhasil Dikirim",
                        """
                        Feedback sudah tersimpan. Siswa dapat melihat feedback ini
                        pada halaman Feedback Siswa.
                        """,
                        "green-card"
                    )

                    st.write("**Nama siswa:**", data_terpilih["nama"])
                    st.write("**Nama guru:**", nama_guru)
                    st.write("**Feedback:**")
                    st.write(isi_feedback)