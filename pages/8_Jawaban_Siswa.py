import streamlit as st
from database.init_db import init_db
from database.queries import get_tanggapan_status_df
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
    page_title="Jawaban Siswa",
    page_icon="📖",
    layout="wide"
)

load_css()
require_role(["guru"])
role_navigation()

page_title(
    "📖 Jawaban atau Tanggapan Siswa",
    "Halaman ini digunakan guru untuk membaca hasil analisis siswa pada setiap jenis simulasi."
)

df = get_tanggapan_status_df()

if df.empty:
    info_card(
        "Belum Ada Tanggapan",
        "Belum ada siswa yang mengirim tanggapan.",
        "yellow-card"
    )

else:
    section_title("Filter Jawaban")

    daftar_status = [
        "Semua",
        "Belum diberi feedback",
        "Sudah diberi feedback"
    ]

    status_pilihan = st.selectbox("Filter status feedback", daftar_status)

    if status_pilihan != "Semua":
        df = df[df["status_feedback"] == status_pilihan]

    daftar_simulasi = ["Semua"] + sorted(df["jenis_simulasi"].unique().tolist())
    simulasi_pilihan = st.selectbox("Filter jenis simulasi", daftar_simulasi)

    if simulasi_pilihan != "Semua":
        df = df[df["jenis_simulasi"] == simulasi_pilihan]

    if df.empty:
        info_card(
            "Data Tidak Ditemukan",
            "Tidak ada tanggapan pada filter yang dipilih.",
            "yellow-card"
        )

    else:
        daftar_siswa = ["Semua"] + sorted(df["nama"].unique().tolist())
        pilihan_siswa = st.selectbox("Pilih siswa", daftar_siswa)

        if pilihan_siswa != "Semua":
            df = df[df["nama"] == pilihan_siswa]

        section_title("Daftar Tanggapan")

        st.write(f"Jumlah tanggapan: **{len(df)}**")

        for index, row in df.iterrows():
            status_label = "✅ Sudah diberi feedback" if row["status_feedback"] == "Sudah diberi feedback" else "⏳ Belum diberi feedback"

            with st.expander(f"{row['nama']} | {row['jenis_simulasi']} | {row['waktu']} | {status_label}"):
                feedback_status_card(row["status_feedback"])

                st.write("**ID Tanggapan:**", row["id_tanggapan"])
                st.write("**Nama siswa:**", row["nama"])
                st.write("**Waktu:**", row["waktu"])
                st.write("**Jumlah feedback:**", row["jumlah_feedback"])

                generic_simulation_result_view(row)
                guided_inquiry_answer_view_generic(row)