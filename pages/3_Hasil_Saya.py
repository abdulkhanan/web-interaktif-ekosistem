import streamlit as st
from html import escape

from modules.auth import require_role
from modules.missions import MISSIONS, MISSION_CODES
from database.init_db import init_db
from database.queries import (
    count_experiment_runs,
    get_inquiry_response,
    initialize_mission_progress,
)
from components.ui import load_css, role_navigation
from components.mission_ui import (
    get_stage_label,
    get_status_meta,
    inject_mission_css,
    render_overall_progress,
)


st.set_page_config(
    page_title="Hasil Saya",
    page_icon="📊",
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
if not id_user:
    st.error("Identitas akun siswa tidak ditemukan. Silakan keluar lalu login kembali.")
    st.stop()

try:
    progress_df = initialize_mission_progress(id_user)
except Exception as exc:
    st.error("Halaman hasil belum dapat membaca progres dari database.")
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

st.markdown(
    """
    <div class="mission-hero">
        <div class="mission-kicker">Rekam Jejak Belajar</div>
        <h1>Hasil Saya</h1>
        <p>Tinjau progres setiap misi, jumlah percobaan yang tersimpan, dan hasil penyelidikanmu.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_overall_progress(completed_count)

for mission_code in MISSION_CODES:
    mission = MISSIONS[mission_code]
    progress = progress_by_code.get(
        mission_code,
        {"status": "belum_dimulai", "current_stage": "fenomena"},
    )
    status = progress.get("status", "belum_dimulai")
    current_stage = progress.get("current_stage", "fenomena")
    status_meta = get_status_meta(status)

    try:
        response = get_inquiry_response(id_user, mission_code) or {}
        run_count = count_experiment_runs(id_user, mission_code)
    except Exception:
        response = {}
        run_count = 0

    with st.container(border=True):
        col_icon, col_content, col_status = st.columns([0.7, 5, 1.4])
        with col_icon:
            st.markdown(f"<div style='font-size:34px;text-align:center;'>{mission['icon']}</div>", unsafe_allow_html=True)
        with col_content:
            st.markdown(f"**{mission['title']}**")
            st.caption(
                f"Tahap aktif: {get_stage_label(current_stage)} · Percobaan tersimpan: {run_count}"
            )
        with col_status:
            st.markdown(
                f"<div style='text-align:center;border-radius:999px;padding:7px 10px;background:{status_meta['bg']};color:{status_meta['text']};font-size:12px;font-weight:800;'>{status_meta['icon']} {status_meta['label']}</div>",
                unsafe_allow_html=True,
            )

        if response:
            rumusan = escape(str(response.get("rumusan_masalah") or "Belum diisi"))
            kesimpulan = escape(str(response.get("kesimpulan") or "Belum diisi"))
            st.markdown(
                f"<div class='result-row'><div><div class='result-title'>Rumusan masalah</div><div class='result-meta'>{rumusan}</div></div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='result-row'><div><div class='result-title'>Kesimpulan</div><div class='result-meta'>{kesimpulan}</div></div></div>",
                unsafe_allow_html=True,
            )
        else:
            st.caption("Belum ada jawaban guided inquiry yang tersimpan untuk misi ini.")
