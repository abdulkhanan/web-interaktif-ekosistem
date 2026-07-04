import streamlit as st
from html import escape

from modules.auth import require_role
from modules.missions import MISSIONS, MISSION_CODES
from database.init_db import init_db
from database.queries import initialize_mission_progress, start_mission
from components.ui import load_css, role_navigation
from components.mission_ui import (
    get_stage_label,
    get_status_meta,
    inject_mission_css,
    mission_card_html,
    stage_tracker_html,
)


st.set_page_config(
    page_title="Misi Penyelidikan",
    page_icon="🔬",
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
    st.error("Halaman misi belum dapat membaca progres dari database.")
    st.code(str(exc))
    st.stop()

progress_by_code = {
    str(row["mission_code"]): row.to_dict()
    for _, row in progress_df.iterrows()
}

query_mission = st.query_params.get("misi")
if isinstance(query_mission, list):
    query_mission = query_mission[0] if query_mission else None
selected_code = query_mission or st.session_state.get("selected_mission_code")
if selected_code not in MISSION_CODES:
    selected_code = None

st.markdown(
    """
    <div class="mission-hero">
        <div class="mission-kicker">Guided Inquiry</div>
        <h1>Misi Penyelidikan</h1>
        <p>Pilih satu misi. Sistem akan menyimpan progresmu dan menjaga urutan enam tahap penyelidikan.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not selected_code:
    st.markdown("### Pilih misi")
    codes = list(MISSION_CODES)
    for row_start in range(0, len(codes), 2):
        columns = st.columns(2, gap="large")
        for column, mission_code in zip(columns, codes[row_start:row_start + 2]):
            mission = MISSIONS[mission_code]
            progress = progress_by_code.get(
                mission_code,
                {"status": "belum_dimulai", "current_stage": "fenomena"},
            )
            with column:
                with st.container(border=True, key=f"hub_card_{mission_code}"):
                    st.markdown(
                        mission_card_html(mission_code, mission, progress),
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "Pilih Misi",
                        key=f"select_{mission_code}",
                        use_container_width=True,
                    ):
                        st.session_state["selected_mission_code"] = mission_code
                        st.query_params["misi"] = mission_code
                        st.rerun()
    st.stop()

mission = MISSIONS[selected_code]
progress = progress_by_code.get(
    selected_code,
    {"status": "belum_dimulai", "current_stage": "fenomena"},
)
status = progress.get("status", "belum_dimulai")
current_stage = progress.get("current_stage", "fenomena")
status_meta = get_status_meta(status)

back_col, _ = st.columns([1, 4])
with back_col:
    if st.button("← Pilih Misi Lain", use_container_width=True):
        st.session_state.pop("selected_mission_code", None)
        st.query_params.clear()
        st.rerun()

st.markdown(
    f"""
    <div class="mission-detail">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:18px;flex-wrap:wrap;">
            <div style="display:flex;gap:16px;align-items:flex-start;">
                <div style="width:58px;height:58px;border-radius:18px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-size:31px;">{escape(str(mission['icon']))}</div>
                <div>
                    <div style="font-size:12px;font-weight:900;letter-spacing:1px;color:#64748b;text-transform:uppercase;">{escape(selected_code.replace('_', ' ').title())}</div>
                    <div style="font-family:Outfit,sans-serif;font-size:30px;font-weight:900;color:#0f172a;line-height:1.15;margin-top:4px;">{escape(str(mission['title']))}</div>
                    <div style="font-size:15px;color:#64748b;line-height:1.6;margin-top:8px;max-width:760px;">{escape(str(mission['focus']))}</div>
                </div>
            </div>
            <div class="mission-status" style="background:{status_meta['bg']};color:{status_meta['text']};">{status_meta['icon']} {status_meta['label']}</div>
        </div>
        {stage_tracker_html(status, current_stage)}
    </div>
    """,
    unsafe_allow_html=True,
)

info_col1, info_col2, info_col3 = st.columns(3)
with info_col1:
    st.metric("Tahap aktif", get_stage_label(current_stage))
with info_col2:
    st.metric("Jumlah tahap", "6 tahap")
with info_col3:
    st.metric("Minimal percobaan", f"{mission['minimum_trials']} kali")

st.markdown("### Apa yang akan kamu lakukan?")
st.write(
    "Kamu akan mengamati fenomena, merumuskan masalah, menyusun hipotesis, menjalankan simulasi, menganalisis data, dan menarik kesimpulan berdasarkan bukti."
)

button_col1, button_col2 = st.columns([2, 1])
with button_col1:
    if status == "belum_dimulai":
        if st.button("Mulai Misi", type="primary", use_container_width=True):
            try:
                start_mission(id_user, selected_code)
                st.success("Misi dimulai. Tahap aktif: Fenomena.")
                st.rerun()
            except Exception as exc:
                st.error("Misi belum dapat dimulai.")
                st.code(str(exc))
    elif status == "selesai":
        if st.button("Lihat Hasil Saya", type="primary", use_container_width=True):
            st.switch_page("pages/3_Hasil_Saya.py")
    else:
        if st.button("Masuk ke Aktivitas", type="primary", use_container_width=True):
            st.session_state["selected_mission_code"] = selected_code
            st.switch_page("pages/3_Simulasi_Ekosistem.py")

with button_col2:
    if st.button("Kembali ke Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard_Siswa.py")

if status == "sedang_dikerjakan":
    st.caption(
        "Progres misi sudah tersimpan. Lanjutkan aktivitas sesuai fokus misi yang dipilih."
    )
