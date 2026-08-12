import streamlit as st
from html import escape
from modules.learning_path import (
    SIMULASI_PRASYARAT,
    cek_prasyarat_simulasi,
    format_nama_materi
)
from modules.auth import require_role
from database.init_db import init_db
from database.queries import (
    get_tanggapan_by_nama_df,
    get_feedback_by_nama_df,
    get_progress_by_nama,
    get_materi_selesai_codes
)
from components.ui import (
    role_navigation,
    load_css,
    page_title,
    section_title,
    status_card,
    info_card,
    generic_simulation_result_view,
    guided_inquiry_answer_view_generic
)

init_db()

st.set_page_config(
    page_title="Dashboard Siswa",
    page_icon="👨‍🎓",
    layout="wide"
)

# --- CSS Khusus Dashboard Siswa ---
st.markdown(
    """
    <style>
        .dashboard-section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 16px;
            margin-top: 24px;
        }

        .alert-banner-action {
            background: linear-gradient(135deg, rgba(5, 150, 105, 0.08), rgba(2, 132, 199, 0.08));
            border: 1px solid rgba(5, 150, 105, 0.25);
            border-left: 4px solid #059669;
            border-radius: 14px;
            padding: 16px 20px;
            font-size: 15px;
            color: #064e3b;
            font-weight: 600;
            margin-bottom: 24px;
            line-height: 1.6;
        }

        /* Progress Tracker Styles */
        .tracker-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 20px;
            box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
            padding: 24px 32px;
            margin-bottom: 24px;
            position: relative;
        }
        .tracker-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 2;
            width: 80px;
        }
        .tracker-icon {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            background: #f1f5f9;
            color: #94a3b8;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
            margin-bottom: 8px;
        }
        .tracker-label {
            font-size: 13px;
            font-weight: 700;
            color: #64748b;
            text-align: center;
        }
        
        /* Active/Done States */
        .tracker-step.done .tracker-icon {
            background: #10b981;
            color: white;
            border-color: #059669;
            box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
        }
        .tracker-step.done .tracker-label { color: #10b981; }
        
        .tracker-step.active .tracker-icon {
            background: #0ea5e9;
            color: white;
            border-color: #0284c7;
            box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.2);
        }
        .tracker-step.active .tracker-label { color: #0ea5e9; }

        /* Lines between steps */
        .tracker-line-bg {
            position: absolute;
            top: 48px;
            left: 60px;
            right: 60px;
            height: 4px;
            background: #e2e8f0;
            z-index: 1;
        }
        .tracker-line-fill {
            height: 100%;
            background: #10b981;
            transition: width 0.5s ease;
        }

        /* Review Card */
        .review-card {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
            padding: 20px;
            margin-bottom: 16px;
        }
        .review-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid #f1f5f9;
        }
        .review-title {
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
        }
        .review-date {
            font-size: 12px;
            color: #64748b;
            font-weight: 600;
        }
        .review-body {
            font-size: 14px;
            color: #334155;
            line-height: 1.6;
        }
        .review-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            background: rgba(124, 58, 237, 0.1);
            color: #7c3aed;
            margin-bottom: 8px;
        }
        .feedback-box {
            background: rgba(16, 185, 129, 0.05);
            border-left: 3px solid #10b981;
            padding: 12px 16px;
            margin-top: 16px;
            border-radius: 0 8px 8px 0;
        }
        .feedback-title {
            font-size: 13px;
            font-weight: 800;
            color: #059669;
            margin-bottom: 4px;
        }


        /* Capaian Pembelajaran */
        .cp-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #dbeafe;
            border-left: 5px solid #0284c7;
            border-radius: 18px;
            padding: 22px 24px;
            margin: 0 0 24px 0;
            box-shadow: 0 8px 24px -14px rgba(2, 132, 199, 0.25);
        }
        .cp-title {
            font-family: 'Outfit', sans-serif;
            font-size: 19px;
            font-weight: 900;
            color: #0f172a;
            margin-bottom: 14px;
        }
        .cp-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
        }
        .cp-item {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px 18px;
        }
        .cp-item-title {
            font-size: 14px;
            font-weight: 800;
            color: #0369a1;
            margin-bottom: 8px;
        }
        .cp-text {
            font-size: 14px;
            color: #334155;
            line-height: 1.7;
            text-align: justify;
        }
        @media (max-width: 800px) {
            .cp-grid { grid-template-columns: 1fr; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

load_css()
require_role(["siswa"])
role_navigation()

nama_siswa = st.session_state.get("nama_pengguna", "")

st.markdown(
    f"""
    <div style="margin-top: 1rem; margin-bottom: 2rem;">
        <h1 style="font-family:'Outfit',sans-serif; font-weight:900; color:#0f172a; font-size:36px; margin-bottom:4px;">👨‍🎓 Halo, {escape(nama_siswa)}!</h1>
        <p style="color:#64748b; font-size:16px;">Pantau terus progress belajarmu dan selesaikan semua tahapan pembelajaran Ekosistem.</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="cp-card">
        <div class="cp-title">🎯 Capaian Pembelajaran (CP) Fase E — Biologi</div>
        <div class="cp-grid">
            <div class="cp-item">
                <div class="cp-item-title">🧬 Pemahaman Biologi</div>
                <div class="cp-text">
                    Menerapkan prinsip klasifikasi dan strategi pelestarian keanekaragaman hayati;
                    mendeskripsikan peranan virus, bakteri, dan jamur dalam kehidupan;
                    <strong>menganalisis interaksi antar komponen ekosistem dan pengaruhnya terhadap keseimbangan ekosistem</strong>;
                    dan menerapkan konsep IPA untuk mengatasi permasalahan berkaitan dengan perubahan iklim.
                </div>
            </div>
            <div class="cp-item">
                <div class="cp-item-title">🔎 Keterampilan Proses</div>
                <div class="cp-text">
                    Keterampilan inkuiri terkait biologi yang meliputi keterampilan mengamati;
                    merumuskan pertanyaan dan memprediksi; merencanakan dan melakukan penyelidikan;
                    memproses dan menganalisis data/informasi; mengevaluasi dan refleksi; serta
                    mengomunikasikan hasil.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

df_tanggapan = get_tanggapan_by_nama_df(nama_siswa)
df_feedback = get_feedback_by_nama_df(nama_siswa)
df_progress = get_progress_by_nama(nama_siswa)
materi_selesai = get_materi_selesai_codes(nama_siswa)

if df_progress.empty:
    simulasi_dijalankan = False
    tanggapan_dikirim = not df_tanggapan.empty
    feedback_diterima = not df_feedback.empty
else:
    progress = df_progress.iloc[0]
    simulasi_dijalankan = progress["simulasi_dijalankan"] == 1
    tanggapan_dikirim = progress["tanggapan_dikirim"] == 1 or not df_tanggapan.empty
    feedback_diterima = progress["feedback_diterima"] == 1 or not df_feedback.empty

materi_ada = len(materi_selesai) > 0

if df_progress.empty:
    simulasi_dijalankan = False
    tanggapan_dikirim = not df_tanggapan.empty
    feedback_diterima = not df_feedback.empty
else:
    progress = df_progress.iloc[0]
    simulasi_dijalankan = progress["simulasi_dijalankan"] == 1
    tanggapan_dikirim = progress["tanggapan_dikirim"] == 1 or not df_tanggapan.empty
    feedback_diterima = progress["feedback_diterima"] == 1 or not df_feedback.empty

materi_ada = len(materi_selesai) > 0

# Tentukan status progress sesuai alur guided inquiry
step1_done = simulasi_dijalankan
step2_done = materi_ada
step3_done = tanggapan_dikirim
step4_done = feedback_diterima

# Logic Next Action sesuai alur guided inquiry
if not step1_done:
    next_action = "Menjalankan <strong>Simulasi Ekosistem</strong>"
    next_link = "Simulasi Ekosistem"
elif not step2_done:
    next_action = "Membaca <strong>Materi Ekosistem sebagai Bahan Penyelidikan</strong>"
    next_link = "Materi Ekosistem"
elif not step3_done:
    next_action = "Mengirim <strong>Tanggapan Analisis</strong>"
    next_link = "Simulasi Ekosistem / Tanggapan"
elif not step4_done:
    next_action = "Menunggu <strong>Feedback Guru</strong>"
    next_link = "Dashboard"
else:
    next_action = "Selamat! Semua tahapan selesai. 🎉"
    next_link = ""

st.markdown(
    f"""
    <div class="alert-banner-action">
        🚀 <strong>Langkah Selanjutnya:</strong> {next_action}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="dashboard-section-title">📍 Jalur Belajar Kamu</div>', unsafe_allow_html=True)

# Hitung progress tracker bar
done_count = sum([step1_done, step2_done, step3_done, step4_done])
bar_width = min((done_count / 3) * 100, 100) if done_count > 0 else 0

st.markdown(
    f"""
    <div class="tracker-container">
        <div class="tracker-line-bg">
            <div class="tracker-line-fill" style="width: {bar_width}%;"></div>
        </div>
        <div class="tracker-step {'done' if step1_done else ('active' if not step1_done else '')}">
            <div class="tracker-icon">🔬</div>
            <div class="tracker-label">Simulasi</div>
        </div>
        <div class="tracker-step {'done' if step2_done else ('active' if step1_done and not step2_done else '')}">
            <div class="tracker-icon">📖</div>
            <div class="tracker-label">Materi Penyelidikan</div>
        </div>
        <div class="tracker-step {'done' if step3_done else ('active' if step2_done and not step3_done else '')}">
            <div class="tracker-icon">📝</div>
            <div class="tracker-label">Tanggapan</div>
        </div>
        <div class="tracker-step {'done' if step4_done else ('active' if step3_done and not step4_done else '')}">
            <div class="tracker-icon">💬</div>
            <div class="tracker-label">Feedback</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col_mat_l, col_mat_r = st.columns([1, 1], gap="large")

with col_mat_l:
    st.markdown('<div class="dashboard-section-title">📚 Materi sebagai Bahan Penyelidikan</div>', unsafe_allow_html=True)
    if len(materi_selesai) == 0:
        info_card("Belum Ada", "Kamu belum membaca materi sebagai bahan penyelidikan.", "yellow-card")
    else:
        daftar = "".join([f"<li style='margin-bottom:8px; color:#334155;'><strong>✅ {format_nama_materi(kode)}</strong></li>" for kode in materi_selesai])
        st.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:16px; padding:20px; box-shadow:0 4px 10px rgba(0,0,0,0.02);">
                <ul style="list-style:none; padding:0; margin:0;">{daftar}</ul>
            </div>
        """, unsafe_allow_html=True)



with col_mat_r:
    st.markdown('<div class="dashboard-section-title">💬 Riwayat & Feedback</div>', unsafe_allow_html=True)
    
    if df_tanggapan.empty:
        info_card("Riwayat Kosong", "Kamu belum mengirim tanggapan dari simulasi.", "yellow-card")
    else:
        for index, row in df_tanggapan.iterrows():
            id_t = row['id_tanggapan']
            waktu = escape(str(row['waktu']))
            jenis = escape(str(row['jenis_simulasi']))
            
            # Cari feedback untuk tanggapan ini
            fb_match = df_feedback[df_feedback["id_tanggapan"] == id_t]
            
            fb_html = ""
            if not fb_match.empty:
                guru = escape(str(fb_match.iloc[0]["nama_guru"]))
                isi = escape(str(fb_match.iloc[0]["isi_feedback"]))
                fb_html = (
                    f"<div class='feedback-box'>"
                    f"<div class='feedback-title'>Feedback dari {guru}</div>"
                    f"<div style='font-size:13px; color:#334155;'>{isi}</div>"
                    f"</div>"
                )
            else:
                fb_html = (
                    f"<div style='margin-top:12px; font-size:12px; color:#f59e0b; font-weight:700;'>"
                    f"⏳ Menunggu feedback dari guru..."
                    f"</div>"
                )
                
            st.markdown(f"""
<div class="review-card">
<div class="review-header">
<div class="review-title">Simulasi {jenis}</div>
<div class="review-date">{waktu}</div>
</div>
<div class="review-body">
<strong>Kesimpulan Kamu:</strong><br>
<span style="color:#64748b;">"{escape(str(row['kesimpulan']))}"</span>
</div>
{fb_html}
</div>
""", unsafe_allow_html=True)
