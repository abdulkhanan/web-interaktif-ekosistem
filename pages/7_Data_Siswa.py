import streamlit as st
from database.init_db import init_db
from database.queries import get_progress_siswa_df
from modules.auth import require_role
from components.ui import (
    role_navigation,
    load_css,
    page_title,
    section_title,
    info_card,
    progress_summary,
    progress_table,
    status_legend
)

init_db()

st.set_page_config(
    page_title="Data Siswa",
    page_icon="📋",
    layout="wide"
)

load_css()
require_role(["guru"])
role_navigation()

page_title(
    "📋 Data dan Progres Siswa",
    "Halaman ini menampilkan progres siswa berdasarkan alur: rencana investigasi, simulasi/data, materi pendukung, uji hipotesis, kesimpulan, dan feedback."
)

df = get_progress_siswa_df()

if df.empty:
    info_card(
        "Belum Ada Data",
        "Belum ada data progres siswa. Data akan muncul setelah siswa mulai merancang investigasi, menjalankan simulasi, membuka materi pendukung, atau mengirim hasil penyelidikan.",
        "yellow-card"
    )

else:
    section_title("Ringkasan Progres Guided Inquiry")
    progress_summary(df)

    section_title("Tabel Progres Penyelidikan Siswa")
    progress_table(df)

    section_title("Keterangan Status")
    status_legend()