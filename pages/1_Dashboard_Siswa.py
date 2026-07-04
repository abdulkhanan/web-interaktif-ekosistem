import streamlit as st
from html import escape

from modules.auth import require_role
from modules.missions import MISSIONS, MISSION_CODES
from database.init_db import init_db
from database.queries import initialize_mission_progress
from components.ui import load_css, role_navigation
from components.mission_ui import (
    inject_mission_css,
    mission_card_html,
    render_overall_progress,
)


AVAILABLE_MISSION_CODES = {"misi_1"}


st.set_page_config(
    page_title="Dashboard Siswa",
    page_icon="🌿",
    layout="wide",
)


@st.cache_resource
def cached_init_db():
    init_db()


cached_init_db()
load_css()
require_role(["siswa"])
role_navigation()
inject_mission_css()

id_user = st.session_state.get("id_user")
nama_siswa = st.session_state.get("nama_pengguna") or "Siswa"

if not id_user:
    st.error("Identitas akun siswa tidak ditemukan. Silakan keluar lalu login kembali.")
    st.stop()

try:
    progress_df = initialize_mission_progress(id_user)
except Exception as exc:
    st.error("Dashboard belum dapat membaca progres misi dari database.")
    st.code(str(exc))
    st.stop()

progress_by_code = {
    str(row["mission_code"]): row.to_dict()
    for _, row in progress_df.iterrows()
}

completed_count = sum(
    1
    for code in MISSION_CODES
    if progress_by_code.get(code, {}).get("status") == "selesai"
)

active_code = next(
    (
        code
        for code in MISSION_CODES
        if code in AVAILABLE_MISSION_CODES
        and progress_by_code.get(code, {}).get("status") == "sedang_dikerjakan"
    ),
    None,
)
if active_code is None:
    active_code = next(
        (
            code
            for code in MISSION_CODES
            if code in AVAILABLE_MISSION_CODES
            and progress_by_code.get(code, {}).get("status") == "belum_dimulai"
        ),
        None,
    )

st.markdown(
    f"""
    <div class="mission-hero">
        <div class="mission-kicker">Eksplorasi Ekosistem</div>
        <h1>Halo, {escape(str(nama_siswa))}</h1>
        <p>
            Selesaikan empat misi penyelidikan untuk memahami bagaimana perubahan satu komponen
            dapat memengaruhi keseimbangan ekosistem. Setiap misi terdiri atas enam tahap guided inquiry.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_overall_progress(completed_count)

if completed_count == len(MISSION_CODES):
    st.markdown(
        """
        <div class="next-mission-banner">
            <strong>Semua misi selesai.</strong> Buka halaman Hasil Saya untuk meninjau kembali progres dan hasil penyelidikanmu.
        </div>
        """,
        unsafe_allow_html=True,
    )
elif active_code:
    active_mission = MISSIONS[active_code]
    active_status = progress_by_code.get(active_code, {}).get("status", "belum_dimulai")
    action_text = "Lanjutkan" if active_status == "sedang_dikerjakan" else "Mulai"
    st.markdown(
        f"""
        <div class="next-mission-banner">
            <strong>Langkah berikutnya:</strong> {action_text} <strong>{escape(active_mission['title'])}</strong>.
            Fokuskan perhatian pada satu misi sampai tahap penyelidikan selesai.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    "<div style='font-family:Outfit,sans-serif;font-size:24px;font-weight:900;color:#0f172a;margin:8px 0 16px;'>Misi Penyelidikan</div>",
    unsafe_allow_html=True,
)

codes = list(MISSION_CODES)
for row_start in range(0, len(codes), 2):
    columns = st.columns(2, gap="large")
    for column, mission_code in zip(columns, codes[row_start:row_start + 2]):
        mission = MISSIONS[mission_code]
        progress = progress_by_code.get(
            mission_code,
            {"status": "belum_dimulai", "current_stage": "fenomena"},
        )
        status = progress.get("status", "belum_dimulai")
        is_available = mission_code in AVAILABLE_MISSION_CODES
        button_label = (
            {
                "belum_dimulai": "Mulai Misi",
                "sedang_dikerjakan": "Lanjutkan Misi",
                "selesai": "Lihat Misi",
            }.get(status, "Buka Misi")
            if is_available
            else "Segera Hadir"
        )

        with column:
            with st.container(border=True, key=f"mission_card_{mission_code}"):
                st.markdown(
                    mission_card_html(mission_code, mission, progress),
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="mission-card-spacer"></div>', unsafe_allow_html=True)
                if st.button(
                    button_label,
                    key=f"open_{mission_code}",
                    use_container_width=True,
                    type="primary" if mission_code == active_code else "secondary",
                    disabled=not is_available,
                ):
                    st.session_state["selected_mission_code"] = mission_code
                    st.query_params["misi"] = mission_code
                    st.switch_page("pages/2_Misi_Penyelidikan.py")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown("### Cara kerja setiap misi")
    st.caption(
        "Amati fenomena, rumuskan masalah, buat hipotesis, lakukan penyelidikan, analisis data, lalu tarik kesimpulan."
    )
