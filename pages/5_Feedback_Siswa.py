import streamlit as st
from database.init_db import init_db
from database.queries import get_feedback_by_nama_df
from modules.auth import require_role
from components.ui import load_css, page_title, section_title, info_card, role_navigation

init_db()

st.set_page_config(
    page_title="Feedback Siswa",
    page_icon="💬",
    layout="wide"
)

load_css()
require_role(["siswa"])
role_navigation()

nama_siswa = st.session_state.get("nama_pengguna", "")

page_title(
    "💬 Feedback dari Guru",
    "Halaman ini menampilkan feedback guru terhadap tanggapan yang sudah kamu kirim."
)

info_card(
    "Feedback untuk",
    nama_siswa,
    "green-card"
)

df = get_feedback_by_nama_df(nama_siswa)

section_title("Daftar Feedback")

if df.empty:
    info_card(
        "Belum Ada Feedback",
        "Guru belum memberikan feedback. Silakan cek kembali setelah guru membaca tanggapanmu.",
        "yellow-card"
    )
else:
    st.success(f"Ditemukan {len(df)} feedback.")

    for index, row in df.iterrows():
        with st.expander(f"Feedback pada {row['waktu_feedback']}"):
            st.write("**Guru:**", row["nama_guru"])
            st.write("**Waktu feedback:**", row["waktu_feedback"])
            st.write("**Isi feedback:**")
            st.write(row["isi_feedback"])

    info_card(
        "Refleksi",
        "Gunakan feedback dari guru untuk memperbaiki pemahamanmu tentang hubungan antara pencemaran, komponen abiotik, dan komponen biotik dalam ekosistem.",
        "blue-card"
    )
