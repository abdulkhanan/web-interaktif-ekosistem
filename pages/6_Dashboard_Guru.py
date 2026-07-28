import streamlit as st
import pandas as pd
from html import escape
from database.init_db import init_db
from database.queries import (
    get_dashboard_counts_with_status,
    get_tanggapan_status_df,
    get_progress_siswa_df,
    get_user_counts
)
from modules.auth import require_role
from components.ui import load_css, page_title, section_title, info_card, role_navigation

init_db()

st.set_page_config(
    page_title="Dashboard Guru",
    page_icon="👩‍🏫",
    layout="wide"
)

# --- CSS Khusus Dashboard V2 ---
st.markdown(
    """
    <style>
        .dashboard-section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 16px;
            margin-top: 8px;
        }

        .metric-card-v2 {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 20px;
            box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
            padding: 20px 22px;
            min-height: 105px;
            display: flex;
            align-items: center;
            gap: 16px;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            margin-bottom: 12px;
        }
        .metric-card-v2:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 35px -10px rgba(15, 23, 42, 0.12);
        }

        .mc-icon {
            width: 54px;
            height: 54px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 25px;
            flex-shrink: 0;
        }
        .mc-content { flex: 1; }
        .mc-label {
            font-size: 12px;
            color: #64748b;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 4px;
        }
        .mc-value {
            font-family: 'Outfit', sans-serif;
            font-size: 32px;
            font-weight: 900;
            line-height: 1;
        }

        .mc-blue .mc-icon { background: rgba(2, 132, 199, 0.1); }
        .mc-blue .mc-value { color: #0284c7; }
        .mc-green .mc-icon { background: rgba(5, 150, 105, 0.1); }
        .mc-green .mc-value { color: #059669; }
        .mc-purple .mc-icon { background: rgba(124, 58, 237, 0.1); }
        .mc-purple .mc-value { color: #7c3aed; }
        .mc-amber .mc-icon { background: rgba(245, 158, 11, 0.1); }
        .mc-amber .mc-value { color: #f59e0b; }

        .alert-banner {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(239, 68, 68, 0.06));
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-left: 4px solid #f59e0b;
            border-radius: 14px;
            padding: 16px 20px;
            font-size: 15px;
            color: #92400e;
            font-weight: 600;
            margin-bottom: 24px;
            line-height: 1.6;
        }

        .info-card {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 20px;
            box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
            padding: 24px;
            margin-bottom: 20px;
            height: 100%;
        }
        .info-card-title {
            font-family: 'Outfit', sans-serif;
            font-size: 17px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* List Items */
        .list-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(226, 232, 240, 0.5);
        }
        .list-item:last-child { border-bottom: none; }
        .li-info { flex: 1; }
        .li-title { font-size: 14px; font-weight: 700; color: #0f172a; }
        .li-subtitle { font-size: 12px; color: #64748b; margin-top: 2px; }
        .badge-warning {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            background: rgba(245, 158, 11, 0.1);
            color: #d97706;
        }

        /* Progress bars */
        .progress-item { margin-bottom: 18px; }
        .progress-item:last-child { margin-bottom: 0; }
        .progress-label { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
        .progress-text { font-size: 14px; font-weight: 600; color: #334155; }
        .progress-count { font-size: 13px; font-weight: 700; color: #64748b; }
        .progress-bar-bg { width: 100%; height: 10px; background: rgba(226, 232, 240, 0.6); border-radius: 999px; overflow: hidden; }
        .progress-bar-fill { height: 100%; border-radius: 999px; transition: width 0.6s ease; }
        .pb-green { background: linear-gradient(90deg, #059669, #10b981); }
        .pb-blue { background: linear-gradient(90deg, #0284c7, #38bdf8); }
        .pb-purple { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
    </style>
    """,
    unsafe_allow_html=True
)

load_css()
require_role(["guru"])
role_navigation()

nama_guru = st.session_state.get("nama_pengguna", "")

page_title(
    "👩‍🏫 Dashboard Guru",
    f"Selamat datang, {nama_guru}. Dashboard ini digunakan untuk memantau alur penyelidikan siswa: rencana investigasi, simulasi/data, uji hipotesis, kesimpulan, dan feedback."
)

(
    jumlah_siswa,
    jumlah_tanggapan,
    jumlah_feedback,
    jumlah_belum_feedback,
    jumlah_sudah_feedback
) = get_dashboard_counts_with_status()

# Ambil data tabel tanggapan untuk list warning
df_status = get_tanggapan_status_df()
df_belum_feedback = df_status[df_status["status_feedback"] == "Belum diberi feedback"]

try:
    progress_df = get_progress_siswa_df()
except Exception:
    progress_df = pd.DataFrame()

# Gunakan data users untuk mendapatkan jumlah siswa sebenarnya
user_counts = get_user_counts()
jumlah_siswa = user_counts.get("siswa", 0)

# Alert jika ada tanggapan menunggu
if jumlah_belum_feedback > 0:
    st.markdown(
        f"""
        <div class="alert-banner">
            ⚠️ Terdapat <strong>{jumlah_belum_feedback} hasil penyelidikan siswa</strong> yang membutuhkan
            feedback. Silakan menuju ke halaman <strong>Feedback Guru</strong> untuk memberi nilai.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="dashboard-section-title">📊 Ringkasan Penyelidikan</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card-v2 mc-blue">
            <div class="mc-icon">🎓</div>
            <div class="mc-content">
                <div class="mc-label">Jumlah Siswa</div>
                <div class="mc-value">{jumlah_siswa}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card-v2 mc-purple">
            <div class="mc-icon">📝</div>
            <div class="mc-content">
                <div class="mc-label">Hasil Penyelidikan</div>
                <div class="mc-value">{jumlah_tanggapan}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card-v2 mc-green">
            <div class="mc-icon">✅</div>
            <div class="mc-content">
                <div class="mc-label">Sudah Feedback</div>
                <div class="mc-value">{jumlah_sudah_feedback}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card-v2 mc-amber">
            <div class="mc-icon">⏳</div>
            <div class="mc-content">
                <div class="mc-label">Menunggu Feedback</div>
                <div class="mc-value">{jumlah_belum_feedback}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.markdown('<div class="dashboard-section-title">📋 Pantauan Guided Inquiry Kelas</div>', unsafe_allow_html=True)

detail_col1, detail_col2 = st.columns([1, 1], gap="large")

with detail_col1:
    list_html = ""
    if not df_belum_feedback.empty:
        # Tampilkan maksimal 6 tanggapan
        recent_pending = df_belum_feedback.head(6)
        list_items = []
        for _, row in recent_pending.iterrows():
            waktu = escape(str(row["waktu"]))
            nama = escape(str(row["nama"]))
            jenis = escape(str(row["jenis_simulasi"]))
            list_items.append(
                f'<div class="list-item">'
                f'<div class="li-info">'
                f'<div class="li-title">{nama} — {jenis}</div>'
                f'<div class="li-subtitle">Dikirim: {waktu}</div>'
                f'</div>'
                f'<span class="badge-warning">Menunggu</span>'
                f'</div>'
            )
        list_html = "".join(list_items)
        
        st.markdown(f"""
            <div class="info-card">
                <div class="info-card-title">⚠️ Hasil Penyelidikan Menunggu Feedback</div>
                {list_html}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="info-card">
                <div class="info-card-title">🎉 Semua Tugas Telah Dinilai</div>
                <p style="color:#64748b; font-size:14px;">Tidak ada hasil penyelidikan siswa yang menunggu feedback. Kerja bagus!</p>
            </div>
        """, unsafe_allow_html=True)

with detail_col2:
    total = max(jumlah_siswa, 1)

    if not progress_df.empty:
        p_materi = int((progress_df["materi_dibaca"].astype(int) == 1).sum())
        p_simulasi = int((progress_df["simulasi_dijalankan"].astype(int) == 1).sum())
        p_tanggapan = int((progress_df["tanggapan_dikirim"].astype(int) == 1).sum())
        p_feedback = int((progress_df["feedback_diterima"].astype(int) == 1).sum())
    else:
        p_materi = p_simulasi = p_tanggapan = p_feedback = 0

    pct_materi = min(int((p_materi / total) * 100), 100)
    pct_simulasi = min(int((p_simulasi / total) * 100), 100)
    pct_tanggapan = min(int((p_tanggapan / total) * 100), 100)
    pct_feedback = min(int((p_feedback / total) * 100), 100)

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-card-title">📈 Progress Guided Inquiry Kelas</div>
            <div class="progress-item">
                <div class="progress-label">
                    <span class="progress-text">🧭 Rencana Investigasi & Data Simulasi</span>
                    <span class="progress-count">{p_simulasi}/{total} Siswa</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill pb-blue" style="width:{pct_simulasi}%;"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span class="progress-text">📘 Membuka Materi Pendukung</span>
                    <span class="progress-count">{p_materi}/{total} Siswa</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill pb-green" style="width:{pct_materi}%;"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span class="progress-text">📝 Uji Hipotesis & Kesimpulan</span>
                    <span class="progress-count">{p_tanggapan}/{total} Siswa</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill pb-purple" style="width:{pct_tanggapan}%;"></div>
                </div>
            </div>
            <div class="progress-item">
                <div class="progress-label">
                    <span class="progress-text">✅ Feedback Diterima</span>
                    <span class="progress-count">{p_feedback}/{total} Siswa</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill pb-green" style="width:{pct_feedback}%;"></div>
                </div>
            </div>
            <hr style="border:0; border-top:1px dashed #cbd5e1; margin:20px 0;">
            <div style="font-size:13px; color:#64748b; line-height:1.5;">
                <strong>Panduan:</strong> Jika banyak siswa berhenti pada tahap rencana/simulasi, bantu mereka menajamkan rumusan masalah atau hipotesis. Jika berhenti pada tahap uji hipotesis, arahkan mereka memilih bukti data yang paling kuat.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
