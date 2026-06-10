import json
import inspect
import os
import pandas as pd
import streamlit as st
from html import escape


# ============================================================
# GLOBAL STYLE
# ============================================================

def load_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

            /* Hide Streamlit iframe wrapper gaps and skeletons for hidden cookies component */
            .st-key-hidden_cookies,
            .st-key-hidden_cookies_logout,
            .st-key-hidden_cookies [data-testid="stSkeleton"],
            .st-key-hidden_cookies .stSkeleton,
            .st-key-hidden_cookies_logout [data-testid="stSkeleton"],
            .st-key-hidden_cookies_logout .stSkeleton,
            .element-container:has(iframe[height="0"]),
            .element-container:has(iframe[height="0px"]) {
                display: none !important;
            }

            /* Global resets & typography */
            html, body, [data-testid="stAppViewContainer"] {
                font-family: 'Outfit', 'Inter', sans-serif !important;
            }

            [data-testid="stSidebar"] {
                display: none !important;
            }

            [data-testid="collapsedControl"] {
                display: none !important;
            }

            header {
                visibility: hidden !important;
            }

            footer {
                visibility: hidden !important;
            }

            .stApp {
                background: 
                    radial-gradient(circle at 10% 20%, rgba(2, 132, 199, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(5, 150, 105, 0.08) 0%, transparent 40%),
                    linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            }

            /* Custom Nav Bar Shell */
            .st-key-nav_bar {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                right: 0 !important;
                z-index: 999999 !important;
                background: rgba(255, 255, 255, 0.85) !important;
                backdrop-filter: blur(12px) !important;
                border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
                border-top: none !important;
                border-left: none !important;
                border-right: none !important;
                border-radius: 0 0 20px 20px !important;
                padding: 10px 40px !important;
                margin: 0 !important;
                box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.08) !important;
            }

            .st-key-nav_bar div[data-testid="column"] {
                padding: 0 4px !important;
            }

            .st-key-nav_bar button {
                border-radius: 14px !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                min-height: 42px !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                text-transform: none !important;
                letter-spacing: 0.2px !important;
                white-space: nowrap !important;
            }

            /* Active Tab Nav */
            .st-key-nav_bar button[disabled] {
                background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
                color: white !important;
                opacity: 1 !important;
                box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25) !important;
                border: none !important;
            }

            /* Inactive Tab Nav */
            .st-key-nav_bar button:not([disabled]) {
                background: transparent !important;
                color: #475569 !important;
                border: 1px solid transparent !important;
                box-shadow: none !important;
            }

            .st-key-nav_bar button:not([disabled]):hover {
                background: rgba(2, 132, 199, 0.08) !important;
                color: #0284c7 !important;
                transform: translateY(-1px) !important;
            }

            /* Logout Button special styling */
            .st-key-nav_bar button[key*="logout"] {
                border: 1px solid rgba(239, 68, 68, 0.2) !important;
                color: #ef4444 !important;
            }
            .st-key-nav_bar button[key*="logout"]:hover {
                background: rgba(239, 68, 68, 0.08) !important;
                color: #dc2626 !important;
                border-color: #ef4444 !important;
            }

            /* Hide mobile elements on desktop by default (screen width > 992px) */
            .st-key-mobile_nav,
            .st-key-mobile_menu_items,
            .menu-backdrop-label,
            .menu-toggle-checkbox {
                display: none !important;
            }

            /* Mobile/Tablet Responsive (max-width: 992px) */
            @media (max-width: 992px) {
                /* Frosted Glass Mobile Navigation Bar at the absolute top */
                .st-key-mobile_nav {
                    display: block !important;
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                    right: 0 !important;
                    z-index: 999999 !important;
                    background: rgba(255, 255, 255, 0.8) !important;
                    backdrop-filter: blur(20px) -webkit-backdrop-filter: blur(20px) !important;
                    border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
                    border-radius: 0 0 20px 20px !important;
                    padding: 20px 25px !important;
                    box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.08) !important;
                    margin: 0 !important;
                }

                .st-key-nav_bar {
                    display: none !important;
                }

                /* Mobile Header Flex Container */
                .mobile-header-container {
                    display: flex !important;
                    flex-direction: row !important;
                    align-items: center !important;
                    justify-content: flex-start !important;
                    gap: 16px !important;
                    width: 100% !important;
                    height: 44px !important;
                }

                /* Premium Hamburger Button with soft green gradient theme */
                .hamburger-label-btn {
                    background: linear-gradient(135deg, rgba(5, 150, 105, 0.08) 0%, rgba(2, 132, 199, 0.08) 100%) !important;
                    border: 1.5px solid rgba(5, 150, 105, 0.15) !important;
                    border-radius: 12px !important;
                    font-size: 20px !important;
                    font-weight: 800 !important;
                    color: #047857 !important;
                    height: 40px !important;
                    width: 40px !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    cursor: pointer !important;
                    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    user-select: none !important;
                    flex-shrink: 0 !important;
                    box-shadow: 0 4px 10px -2px rgba(5, 150, 105, 0.05) !important;
                }
                .hamburger-label-btn:hover {
                    background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
                    color: #ffffff !important;
                    border-color: transparent !important;
                    box-shadow: 0 8px 16px -4px rgba(5, 150, 105, 0.25) !important;
                    transform: translateY(-1px) !important;
                }
                .hamburger-label-btn:active {
                    transform: translateY(1px) scale(0.95) !important;
                }

                /* Logo with Emerald to Blue Premium Gradient */
                .mobile-header-brand {
                    font-family: 'Outfit', sans-serif !important;
                    font-size: 20px !important;
                    font-weight: 900 !important;
                    letter-spacing: 0.8px !important;
                    background: linear-gradient(135deg, #047857 0%, #0284c7 100%) !important;
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                    height: 44px !important;
                    display: flex !important;
                    align-items: center !important;
                }

                /* Modern Frosted Sidebar Drawer */
                .st-key-mobile_menu_items {
                    display: flex !important;
                    position: fixed !important;
                    top: 0 !important;
                    left: 0 !important;
                    bottom: 0 !important;
                    width: 300px !important;
                    height: 100vh !important;
                    z-index: 9999999 !important;
                    background: rgba(255, 255, 255, 0.95) !important;
                    backdrop-filter: blur(25px) -webkit-backdrop-filter: blur(25px) !important;
                    border-right: 1px solid rgba(226, 232, 240, 0.8) !important;
                    box-shadow: 20px 0 50px rgba(15, 23, 42, 0.12) !important;
                    padding: 28px 24px !important;
                    flex-direction: column !important;
                    gap: 14px !important;
                    margin: 0 !important;
                    border-radius: 0 24px 24px 0 !important;
                    overflow-y: auto !important;
                    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease, visibility 0.3s ease !important;
                }
                
                body:not(:has(#menu-toggle:checked)) .st-key-mobile_menu_items {
                    transform: translateX(-100%) !important;
                    opacity: 0 !important;
                    visibility: hidden !important;
                    pointer-events: none !important;
                }

                body:has(#menu-toggle:checked) .st-key-mobile_menu_items {
                    transform: translateX(0) !important;
                    opacity: 1 !important;
                    visibility: visible !important;
                }
                
                /* Premium Drawer Nav Buttons */
                .st-key-mobile_menu_items button {
                    border-radius: 16px !important;
                    font-weight: 700 !important;
                    font-size: 14px !important;
                    min-height: 48px !important;
                    margin-bottom: 6px !important;
                    border: 1px solid transparent !important;
                    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    text-align: left !important;
                    padding: 10px 20px !important;
                    justify-content: flex-start !important;
                }
                /* Active state link */
                .st-key-mobile_menu_items button[disabled] {
                    background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
                    color: white !important;
                    opacity: 1 !important;
                    border: none !important;
                    box-shadow: 0 8px 20px -4px rgba(5, 150, 105, 0.3) !important;
                    transform: translateX(4px) !important;
                }
                /* Inactive state link */
                .st-key-mobile_menu_items button:not([disabled]) {
                    background: rgba(15, 23, 42, 0.02) !important;
                    color: #475569 !important;
                    border: 1px solid rgba(15, 23, 42, 0.04) !important;
                    box-shadow: none !important;
                }
                .st-key-mobile_menu_items button:not([disabled]):hover {
                    background: linear-gradient(135deg, rgba(5, 150, 105, 0.06) 0%, rgba(2, 132, 199, 0.06) 100%) !important;
                    color: #0284c7 !important;
                    border-color: rgba(2, 132, 199, 0.15) !important;
                    transform: translateX(4px) !important;
                }

                /* Drawer Header Container */
                .drawer-header-container {
                    display: flex !important;
                    flex-direction: row !important;
                    align-items: center !important;
                    justify-content: space-between !important;
                    width: 100% !important;
                    height: 44px !important;
                    margin-bottom: 20px !important;
                    border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
                    padding-bottom: 14px !important;
                }

                .drawer-brand {
                    font-family: 'Outfit', sans-serif !important;
                    font-size: 22px !important;
                    font-weight: 900 !important;
                    letter-spacing: 0.8px !important;
                    background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
                    -webkit-background-clip: text !important;
                    -webkit-text-fill-color: transparent !important;
                    display: flex !important;
                    align-items: center !important;
                    height: 44px !important;
                }

                /* Circular Glass Close Button */
                .drawer-close-label-btn {
                    background: rgba(15, 23, 42, 0.04) !important;
                    border-radius: 50% !important;
                    font-size: 14px !important;
                    font-weight: 800 !important;
                    color: #64748b !important;
                    height: 34px !important;
                    width: 34px !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    cursor: pointer !important;
                    transition: all 0.25s ease !important;
                    user-select: none !important;
                    flex-shrink: 0 !important;
                    margin-right: 4px !important;
                    border: 1px solid rgba(15, 23, 42, 0.05) !important;
                }
                .drawer-close-label-btn:hover {
                    background: rgba(239, 68, 68, 0.1) !important;
                    color: #ef4444 !important;
                    border-color: rgba(239, 68, 68, 0.15) !important;
                    transform: rotate(90deg) !important;
                }
            }

            /* Backdrop overlay with blur */
            .menu-backdrop-label {
                position: fixed !important;
                inset: 0 !important;
                z-index: 999998 !important;
                background: rgba(15, 23, 42, 0.3) !important;
                backdrop-filter: blur(8px) -webkit-backdrop-filter: blur(8px) !important;
                opacity: 0 !important;
                visibility: hidden !important;
                transition: opacity 0.3s ease, visibility 0.3s ease !important;
                cursor: pointer !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            body:has(#menu-toggle:checked) .menu-backdrop-label {
                display: block !important;
                opacity: 1 !important;
                visibility: visible !important;
            }

            .identity-card-hover {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            .identity-card-hover:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 12px 30px -4px var(--role-glow) !important;
                border-color: rgba(0, 0, 0, 0.08) !important;
            }

            .hero-card {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(240, 253, 244, 0.8) 100%) !important;
                backdrop-filter: blur(8px);
                border: 1px solid rgba(5, 150, 105, 0.15) !important;
                padding: 32px !important;
                border-radius: 24px !important;
                box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.05) !important;
                margin-bottom: 28px !important;
                transition: transform 0.3s ease !important;
            }

            .hero-card h1 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 34px !important;
                font-weight: 800 !important;
                color: #047857 !important;
                margin: 0 0 10px 0 !important;
                line-height: 1.2 !important;
            }

            .small-muted {
                color: #64748b !important;
                font-size: 15px !important;
                font-weight: 500 !important;
                line-height: 1.6 !important;
            }

            .block-container {
                padding-top: 0.5rem !important;
                padding-bottom: 3rem !important;
                max-width: 1200px !important;
                transition: padding-top 0.3s ease;
            }
            @media (max-width: 992px) {
                .block-container {
                    padding-top: 0.5rem !important;
                }
            }

            .main-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: 36px !important;
                font-weight: 800 !important;
                color: #0f172a !important;
                margin-bottom: 10px !important;
                line-height: 1.2 !important;
            }

            .subtitle {
                font-size: 16px !important;
                color: #475569 !important;
                line-height: 1.7 !important;
                margin-bottom: 28px !important;
            }

            .section-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: 22px !important;
                font-weight: 800 !important;
                color: #0f172a !important;
                margin-top: 32px !important;
                margin-bottom: 16px !important;
                padding-left: 16px !important;
                border-left: 4px solid #059669 !important;
            }

            /* Premium Card Component Overhaul */
            .card,
            .green-card,
            .blue-card,
            .yellow-card,
            .danger-card {
                padding: 24px !important;
                border-radius: 20px !important;
                margin-bottom: 20px !important;
                box-shadow: 0 8px 24px -10px rgba(15, 23, 42, 0.05) !important;
                transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease, border-color 0.25s ease !important;
                border: 1px solid rgba(226, 232, 240, 0.8) !important;
            }

            .card:hover,
            .green-card:hover,
            .blue-card:hover,
            .yellow-card:hover,
            .danger-card:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 16px 32px -12px rgba(15, 23, 42, 0.08) !important;
            }

            .card {
                background: #ffffff !important;
            }

            .green-card {
                background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%) !important;
                border-color: rgba(5, 150, 105, 0.18) !important;
            }
            .green-card:hover {
                border-color: rgba(5, 150, 105, 0.35) !important;
            }

            .blue-card {
                background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%) !important;
                border-color: rgba(2, 132, 199, 0.18) !important;
            }
            .blue-card:hover {
                border-color: rgba(2, 132, 199, 0.35) !important;
            }

            .yellow-card {
                background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%) !important;
                border-color: rgba(217, 119, 6, 0.18) !important;
            }
            .yellow-card:hover {
                border-color: rgba(217, 119, 6, 0.35) !important;
            }

            .danger-card {
                background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%) !important;
                border-color: rgba(220, 38, 38, 0.18) !important;
            }
            .danger-card:hover {
                border-color: rgba(220, 38, 38, 0.35) !important;
            }

            .card-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: 18px !important;
                font-weight: 750 !important;
                color: #0f172a !important;
                margin-bottom: 8px !important;
                letter-spacing: -0.2px !important;
            }

            .card-text {
                font-size: 15px !important;
                color: #475569 !important;
                line-height: 1.7 !important;
            }

            .status-done {
                background: linear-gradient(135deg, #ecfdf5 0%, #dcfce7 100%) !important;
                color: #047857 !important;
                padding: 14px 18px !important;
                border-radius: 16px !important;
                font-weight: 750 !important;
                text-align: center;
                border: 1px solid rgba(5, 150, 105, 0.18) !important;
                box-shadow: 0 4px 12px rgba(5, 150, 105, 0.05) !important;
            }

            .status-wait {
                background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
                color: #b45309 !important;
                padding: 14px 18px !important;
                border-radius: 16px !important;
                font-weight: 750 !important;
                text-align: center;
                border: 1px solid rgba(217, 119, 6, 0.18) !important;
                box-shadow: 0 4px 12px rgba(217, 119, 6, 0.05) !important;
            }

            /* Custom Metrics Styling */
            div[data-testid="stMetric"] {
                background: #ffffff !important;
                border: 1px solid rgba(226, 232, 240, 0.8) !important;
                padding: 20px 24px !important;
                border-radius: 20px !important;
                box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.04) !important;
                transition: transform 0.25s ease, border-color 0.25s ease !important;
            }
            div[data-testid="stMetric"]:hover {
                transform: translateY(-2px);
                border-color: rgba(5, 150, 105, 0.25) !important;
                box-shadow: 0 16px 32px -12px rgba(15, 23, 42, 0.08) !important;
            }
            div[data-testid="stMetricLabel"] {
                font-size: 13px !important;
                font-weight: 700 !important;
                letter-spacing: 0.5px !important;
                text-transform: uppercase !important;
                color: #64748b !important;
            }
            div[data-testid="stMetricValue"] {
                font-family: 'Outfit', sans-serif !important;
                font-size: 32px !important;
                font-weight: 800 !important;
                color: #0f172a !important;
            }

            div[data-testid="stDataFrame"] {
                border-radius: 20px !important;
                overflow: hidden !important;
                border: 1px solid rgba(226, 232, 240, 0.8) !important;
                box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.04) !important;
            }

            textarea, input {
                border-radius: 14px !important;
                border: 1px solid #cbd5e1 !important;
                transition: all 0.2s ease !important;
            }
            textarea:focus, input:focus {
                border-color: #0284c7 !important;
                box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.1) !important;
            }

            /* Custom submit & standard button overrides */
            div.stButton > button,
            div[data-testid="stFormSubmitButton"] button {
                border-radius: 14px !important;
                font-weight: 700 !important;
                padding: 12px 28px !important;
                background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 4px 14px rgba(5, 150, 105, 0.2) !important;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
                font-size: 15px !important;
                min-height: 46px !important;
            }
            div.stButton > button:hover,
            div[data-testid="stFormSubmitButton"] button:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px rgba(2, 132, 199, 0.35) !important;
            }
            
            /* Custom styled tabs for general usage */
            div[data-testid="stTabBar"] {
                background: rgba(255, 255, 255, 0.6) !important;
                padding: 6px !important;
                border-radius: 16px !important;
                border: 1px solid rgba(226, 232, 240, 0.8) !important;
                gap: 6px !important;
            }
            div[data-testid="stTabBar"] button {
                border-radius: 12px !important;
                font-weight: 600 !important;
                color: #475569 !important;
                transition: all 0.2s ease !important;
            }
            div[data-testid="stTabBar"] button[aria-selected="true"] {
                background: #ffffff !important;
                color: #059669 !important;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BASIC UI
# ============================================================

def page_title(title, subtitle=None):
    subtitle_html = subtitle if subtitle else ""

    st.markdown(
        f"""
        <div class="hero-card">
            <h1>{title}</h1>
            <div class="small-muted">{subtitle_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_title(title):
    st.markdown(
        f"<div class='section-title'>{title}</div>",
        unsafe_allow_html=True
    )


def info_card(title, text, card_type="card"):
    st.markdown(
        f"""
        <div class="{card_type}">
            <div class="card-title">{title}</div>
            <div class="card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def status_card(label, status):
    css_class = "status-done" if status else "status-wait"
    status_text = "Sudah" if status else "Belum"

    st.markdown(
        f"<div class='{css_class}'>{label}: {status_text}</div>",
        unsafe_allow_html=True
    )


# ============================================================
# PROGRESS TABLE
# ============================================================

def progress_summary(df):
    total_siswa = len(df)
    selesai_materi = len(df[df["materi_dibaca"] == 1])
    selesai_simulasi = len(df[df["simulasi_dijalankan"] == 1])
    selesai_tanggapan = len(df[df["tanggapan_dikirim"] == 1])
    sudah_feedback = len(df[df["feedback_diterima"] == 1])

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Siswa", total_siswa)

    with col2:
        st.metric("Materi", selesai_materi)

    with col3:
        st.metric("Simulasi", selesai_simulasi)

    with col4:
        st.metric("Tanggapan", selesai_tanggapan)

    with col5:
        st.metric("Feedback", sudah_feedback)


def prepare_progress_table(df):
    df_tampil = df.copy()

    kolom_progress = [
        "materi_dibaca",
        "simulasi_dijalankan",
        "tanggapan_dikirim",
        "feedback_diterima"
    ]

    df_tampil["persentase_progres"] = (
        df_tampil[kolom_progress].sum(axis=1) / len(kolom_progress) * 100
    ).astype(int)

    for kolom in kolom_progress:
        df_tampil[kolom] = df_tampil[kolom].apply(
            lambda x: "✅ Sudah" if x == 1 else "⏳ Belum"
        )

    df_tampil = df_tampil.rename(columns={
        "nama": "Nama Siswa",
        "materi_dibaca": "Materi",
        "simulasi_dijalankan": "Simulasi",
        "tanggapan_dikirim": "Tanggapan",
        "feedback_diterima": "Feedback",
        "updated_at": "Terakhir Update",
        "jumlah_tanggapan": "Jumlah Tanggapan",
        "jumlah_feedback": "Jumlah Feedback",
        "persentase_progres": "Progres (%)"
    })

    kolom_urut = [
        "Nama Siswa",
        "Materi",
        "Simulasi",
        "Tanggapan",
        "Feedback",
        "Progres (%)",
        "Jumlah Tanggapan",
        "Jumlah Feedback",
        "Terakhir Update"
    ]

    return df_tampil[kolom_urut]


def progress_table(df):
    df_tampil = prepare_progress_table(df)

    st.dataframe(
        df_tampil,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nama Siswa": st.column_config.TextColumn("Nama Siswa", width="medium"),
            "Materi": st.column_config.TextColumn("Materi", width="small"),
            "Simulasi": st.column_config.TextColumn("Simulasi", width="small"),
            "Tanggapan": st.column_config.TextColumn("Tanggapan", width="small"),
            "Feedback": st.column_config.TextColumn("Feedback", width="small"),
            "Progres (%)": st.column_config.ProgressColumn(
                "Progres",
                min_value=0,
                max_value=100,
                format="%d%%"
            ),
            "Jumlah Tanggapan": st.column_config.NumberColumn("Tanggapan", width="small"),
            "Jumlah Feedback": st.column_config.NumberColumn("Feedback", width="small"),
            "Terakhir Update": st.column_config.TextColumn("Terakhir Update", width="medium")
        }
    )


def status_legend():
    col1, col2 = st.columns(2)

    with col1:
        info_card(
            "✅ Sudah",
            "Siswa sudah menyelesaikan tahap tersebut.",
            "green-card"
        )

    with col2:
        info_card(
            "⏳ Belum",
            "Siswa belum menyelesaikan tahap tersebut.",
            "yellow-card"
        )


# ============================================================
# FEEDBACK
# ============================================================

def feedback_status_card(status_feedback):
    if status_feedback == "Sudah diberi feedback":
        info_card(
            "Status Feedback",
            "✅ Sudah diberi feedback",
            "green-card"
        )
    else:
        info_card(
            "Status Feedback",
            "⏳ Belum diberi feedback",
            "yellow-card"
        )


# ============================================================
# FORMATTER
# ============================================================

def json_to_dict(value):
    if isinstance(value, dict):
        return value

    try:
        return json.loads(value)
    except Exception:
        return {}


def format_label(key):
    label_map = {
        "penyerapan_karbon_dioksida": "Penyerapan Karbon Dioksida",
        "produksi_oksigen": "Produksi Oksigen",
        "tingkat_limbah_industri": "Tingkat Limbah Industri",
        "tingkat_pencemaran": "Tingkat Pencemaran",
        "tingkat_limbah": "Tingkat Limbah",
        "status_limbah": "Status Limbah",
        "konsentrasi_limbah_ppm": "Konsentrasi Limbah",
        "nilai_do": "Oksigen Terlarut",
        "status_do": "Status DO",
        "kualitas_air": "Kualitas Air",
        "makroinvertebrata": "Makroinvertebrata",
        "populasi_ikan": "Populasi Ikan",
        "status_populasi_ikan": "Status Populasi Ikan",
        "kondisi": "Kondisi Ekosistem",

        "energi_awal": "Energi Awal",
        "efisiensi_transfer": "Efisiensi Transfer",
        "produsen": "Produsen",
        "konsumen_1": "Konsumen I",
        "konsumen_2": "Konsumen II",
        "konsumen_3": "Konsumen III",
        "keterangan": "Keterangan",

        "intensitas_panas": "Intensitas Panas",
        "curah_hujan": "Curah Hujan",
        "tutupan_vegetasi": "Tutupan Vegetasi",
        "evaporasi": "Evaporasi",
        "kondensasi": "Kondensasi",
        "presipitasi": "Presipitasi",
        "infiltrasi": "Infiltrasi",
        "limpasan_permukaan": "Limpasan Permukaan",
        "status": "Status"
    }

    return label_map.get(key, key.replace("_", " ").title())


def format_value(key, value):
    try:
        angka = float(value)

        if key in ["tingkat_limbah_industri", "tingkat_limbah"]:
            return f"{angka * 100:.0f}%"

        if key in [
            "tingkat_pencemaran",
            "kualitas_air",
            "makroinvertebrata",
            "populasi_ikan",
            "intensitas_panas",
            "curah_hujan",
            "tutupan_vegetasi",
            "evaporasi",
            "kondensasi",
            "presipitasi",
            "infiltrasi",
            "limpasan_permukaan"
            "penyerapan_karbon_dioksida",
            "produksi_oksigen",
        ]:
            return f"{angka:.1f}%"

        if key == "nilai_do":
            return f"{angka:.2f} mg/L"

        if key == "konsentrasi_limbah_ppm":
            return f"{angka:.2f} ppm"

        if key in [
            "energi_awal",
            "produsen",
            "konsumen_1",
            "konsumen_2",
            "konsumen_3"
        ]:
            return f"{angka:,.0f} kkal"

        if key == "efisiensi_transfer":
            return f"{angka:.0f}%"

        return f"{angka:g}"

    except Exception:
        return str(value)


def get_status_color(key, value):
    value_text = str(value).lower()

    if key in ["status_limbah", "status_do", "status_populasi_ikan", "kondisi", "status"]:
        if (
            "stabil" in value_text
            or "normal" in value_text
            or "rendah" in value_text
            or "baik" in value_text
            or "seimbang" in value_text
        ):
            return "#ecfdf5", "#15803d", "#bbf7d0"

        if (
            "sedang" in value_text
            or "menurun" in value_text
            or "terganggu" in value_text
        ):
            return "#fff7ed", "#ea580c", "#fed7aa"

        if (
            "tinggi" in value_text
            or "kritis" in value_text
            or "berat" in value_text
            or "risiko" in value_text
        ):
            return "#fef2f2", "#dc2626", "#fecaca"

    return "#f8fafc", "#334155", "#e2e8f0"


# ============================================================
# SIMULATION RESULT VIEW
# ============================================================

def result_card(label, value, key_name="default"):
    bg_color, text_color, border_color = get_status_color(key_name, value)

    st.markdown(
        f"""
        <div style="
            background:{bg_color};
            border:1px solid {border_color};
            border-radius:18px;
            padding:20px;
            margin-bottom:16px;
            box-shadow:0 4px 12px rgba(15,23,42,0.06);
            min-height:110px;
        ">
            <div style="
                font-size:14px;
                color:#64748b;
                font-weight:700;
                margin-bottom:10px;
            ">
                {label}
            </div>
            <div style="
                font-size:25px;
                color:{text_color};
                font-weight:800;
                line-height:1.3;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def input_card(label, value):
    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            border:1px solid #e5e7eb;
            border-radius:16px;
            padding:18px 20px;
            margin-bottom:14px;
            box-shadow:0 2px 8px rgba(15,23,42,0.04);
        ">
            <div style="
                font-size:14px;
                color:#64748b;
                font-weight:700;
                margin-bottom:8px;
            ">
                {label}
            </div>
            <div style="
                font-size:22px;
                color:#0f172a;
                font-weight:800;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def generic_simulation_result_view(row):
    input_data = json_to_dict(row["input_simulasi"])
    hasil_data = json_to_dict(row["hasil_simulasi"])
    jenis_simulasi = row["jenis_simulasi"]

    info_card(
        "Jenis Simulasi",
        jenis_simulasi,
        "blue-card"
    )

    st.markdown("### Input Simulasi")

    if input_data:
        input_items = list(input_data.items())
        input_cols = st.columns(2)

        for index, (key, value) in enumerate(input_items):
            with input_cols[index % 2]:
                input_card(
                    format_label(key),
                    format_value(key, value)
                )
    else:
        info_card(
            "Input Simulasi",
            "Tidak ada data input.",
            "yellow-card"
        )

    st.markdown("### Hasil Simulasi")

    if not hasil_data:
        info_card(
            "Hasil Simulasi",
            "Tidak ada data hasil.",
            "yellow-card"
        )
        return

    if jenis_simulasi == "Pencemaran Sungai":
        col1, col2, col3 = st.columns(3)

        with col1:
            result_card(
                "Status Limbah",
                hasil_data.get("status_limbah", "-"),
                "status_limbah"
            )

        with col2:
            result_card(
                "Status DO",
                hasil_data.get("status_do", "-"),
                "status_do"
            )

        with col3:
            result_card(
                "Populasi Ikan",
                f"{hasil_data.get('status_populasi_ikan', '-')} ({hasil_data.get('populasi_ikan', '-')}%)",
                "status_populasi_ikan"
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            result_card(
                "Oksigen Terlarut",
                format_value("nilai_do", hasil_data.get("nilai_do", "-")),
                "nilai_do"
            )

        with col5:
            result_card(
                "Kualitas Air",
                format_value("kualitas_air", hasil_data.get("kualitas_air", "-")),
                "kualitas_air"
            )

        with col6:
            result_card(
                "Makroinvertebrata",
                format_value("makroinvertebrata", hasil_data.get("makroinvertebrata", "-")),
                "makroinvertebrata"
            )

        result_card(
            "Kondisi Ekosistem",
            hasil_data.get("kondisi", "-"),
            "kondisi"
        )

    elif jenis_simulasi == "Aliran Energi dan Piramida Ekologi":
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            result_card(
                "Produsen",
                format_value("produsen", hasil_data.get("produsen", "-")),
                "produsen"
            )

        with col2:
            result_card(
                "Konsumen I",
                format_value("konsumen_1", hasil_data.get("konsumen_1", "-")),
                "konsumen_1"
            )

        with col3:
            result_card(
                "Konsumen II",
                format_value("konsumen_2", hasil_data.get("konsumen_2", "-")),
                "konsumen_2"
            )

        with col4:
            result_card(
                "Konsumen III",
                format_value("konsumen_3", hasil_data.get("konsumen_3", "-")),
                "konsumen_3"
            )

        info_card(
            "Keterangan",
            hasil_data.get("keterangan", "-"),
            "yellow-card"
        )

    elif jenis_simulasi == "Daur Biogeokimia: Daur Air":
        col1, col2, col3 = st.columns(3)

        with col1:
            result_card(
                "Evaporasi",
                format_value("evaporasi", hasil_data.get("evaporasi", "-")),
                "evaporasi"
            )

        with col2:
            result_card(
                "Presipitasi",
                format_value("presipitasi", hasil_data.get("presipitasi", "-")),
                "presipitasi"
            )

        with col3:
            result_card(
                "Infiltrasi",
                format_value("infiltrasi", hasil_data.get("infiltrasi", "-")),
                "infiltrasi"
            )

        col4, col5 = st.columns(2)

        with col4:
            result_card(
                "Limpasan Permukaan",
                format_value("limpasan_permukaan", hasil_data.get("limpasan_permukaan", "-")),
                "limpasan_permukaan"
            )

        with col5:
            result_card(
                "Status",
                hasil_data.get("status", "-"),
                "status"
            )

        info_card(
            "Keterangan",
            hasil_data.get("keterangan", "-"),
            "yellow-card"
        )

    else:
        hasil_items = list(hasil_data.items())
        cols = st.columns(3)

        for index, (key, value) in enumerate(hasil_items):
            with cols[index % 3]:
                result_card(
                    format_label(key),
                    format_value(key, value),
                    key
                )


# ============================================================
# GUIDED INQUIRY
# ============================================================


def get_guided_questions(jenis_simulasi):
    if jenis_simulasi == "Pencemaran Sungai Akibat Limbah Pabrik":
        return {
            "q1": "1. Jelaskan apa yang terjadi pada ekosistem sungai ketika limbah pabrik masuk ke air.",
            "q2": "2. Berdasarkan grafik atau tabel, data apa yang menunjukkan bahwa kondisi sungai mulai terganggu?",
            "q3": "3. Mengapa penurunan oksigen air dapat mengganggu ikan dan organisme air lainnya?",
            "q4": "4. Tuliskan kesimpulan dan satu tindakan nyata untuk mengurangi pencemaran sungai."
        }

    if jenis_simulasi == "Rantai Makanan Saat Kemarau":
        return {
            "q1": "1. Jelaskan apa yang terjadi pada rantai makanan ketika rumput berkurang saat kemarau.",
            "q2": "2. Berdasarkan data simulasi, tingkatan rantai makanan mana yang memiliki energi paling besar dan paling kecil?",
            "q3": "3. Mengapa berkurangnya produsen dapat memengaruhi konsumen dalam ekosistem?",
            "q4": "4. Tuliskan kesimpulan dan satu tindakan nyata untuk menjaga keseimbangan ekosistem."
        }

    if jenis_simulasi == "Daur Air Saat Pohon Berkurang":
        return {
            "q1": "1. Jelaskan apa yang terjadi pada daur air ketika jumlah pohon berkurang.",
            "q2": "2. Berdasarkan data simulasi, bagaimana tutupan vegetasi memengaruhi infiltrasi dan limpasan permukaan?",
            "q3": "3. Mengapa keberadaan pohon penting bagi keseimbangan air di lingkungan?",
            "q4": "4. Tuliskan kesimpulan dan satu tindakan nyata untuk menjaga keseimbangan daur air."
        }

    if jenis_simulasi == "Peningkatan Alga Akibat Pupuk Berlebih":
        return {
            "q1": "1. Jelaskan apa yang terjadi ketika pupuk berlebih masuk ke sungai atau danau.",
            "q2": "2. Berdasarkan grafik atau tabel, data apa yang menunjukkan bahwa alga tumbuh terlalu banyak?",
            "q3": "3. Mengapa pertumbuhan alga yang berlebihan dapat mengganggu organisme air?",
            "q4": "4. Tuliskan kesimpulan dan satu tindakan nyata untuk mengurangi masuknya pupuk berlebih ke perairan."
        }

    return {
        "q1": "1. Jelaskan fenomena lingkungan yang terjadi pada simulasi.",
        "q2": "2. Jelaskan data penting yang kamu temukan dari grafik atau tabel.",
        "q3": "3. Mengapa fenomena tersebut perlu diperhatikan?",
        "q4": "4. Tuliskan kesimpulan dan satu tindakan nyata yang dapat kamu lakukan."
    }



def guided_inquiry_answer_view_generic(row):
    st.markdown("### Jawaban Literasi Sains dan Sikap Peduli Lingkungan")

    with st.expander("1. Penjelasan Fenomena Ilmiah", expanded=True):
        st.write(row["jawaban_1"])

    with st.expander("2. Interpretasi Data atau Bukti Simulasi", expanded=True):
        st.write(row["jawaban_2"])

    with st.expander("3. Refleksi Sikap Peduli Lingkungan", expanded=True):
        st.write(row["jawaban_3"])

    with st.expander("4. Kesimpulan Ilmiah dan Aksi Nyata", expanded=True):
        st.write(row["kesimpulan"])


# ============================================================
# COMPATIBILITY
# ============================================================

def guided_inquiry_answer_view(row):
    guided_inquiry_answer_view_generic(row)


def simulation_result_view(row):
    generic_simulation_result_view(row)


def simulation_metric_cards(nilai_do, kualitas_air, makroinvertebrata):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("DO", f"{nilai_do} mg/L")

    with col2:
        st.metric("Kualitas Air", f"{kualitas_air}%")

    with col3:
        st.metric("Makroinvertebrata", f"{makroinvertebrata}%")


def ecosystem_condition_card(kondisi, tingkat_pencemaran=None):
    if tingkat_pencemaran is not None:
        if tingkat_pencemaran <= 30:
            card_type = "green-card"
        elif tingkat_pencemaran <= 70:
            card_type = "yellow-card"
        else:
            card_type = "danger-card"
    else:
        card_type = "blue-card"

    info_card(
        "Kondisi Ekosistem",
        kondisi,
        card_type
    )

# ============================================================
# LOGIN DAN NAVIGASI ROLE DARI P1
# ============================================================

def apply_login_style():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .stApp {
        background: linear-gradient(135deg, #4f8df7 0%, #6c63ff 45%, #d7f3f5 100%);
    }



    .st-key-login_card {
        background: white;
        border-radius: 26px;
        padding: 42px 46px;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.18);
        text-align: center;
        min-width: 480px;
    }

    .login-logo {
        font-size: 38px;
        font-weight: 900;
        color: #1f2937;
        margin-bottom: 28px;
        letter-spacing: 3px;
        text-align: center;
        white-space: nowrap;
    }

    .login-title {
        font-size: 30px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 16px;
        text-align: center;
    }

    .login-subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 30px;
        line-height: 1.6;
        text-align: center;
    }

    .login-note {
        font-size: 14px;
        color: #6b7280;
        margin-top: 26px;
        line-height: 1.7;
        text-align: center;
    }

    div[data-testid="stLinkButton"] a {
        width: 100%;
        justify-content: center;
        border-radius: 14px;
        padding-top: 15px;
        padding-bottom: 15px;
        font-size: 17px;
        font-weight: 800;
        background-color: white;
        color: #374151;
        border: 1px solid #d1d5db;
    }

    div[data-testid="stLinkButton"] a:hover {
        background-color: #f3f4f6;
        border-color: #9ca3af;
    }
    </style>
    """, unsafe_allow_html=True)


def login_header():
    st.markdown("""
    <div class="login-logo">🌿 ECOSYSTEM</div>
    <div class="login-title">Welcome Studentss</div>
    <div class="login-subtitle">
        Masuk untuk mengakses web pembelajaran ekosistem.
    </div>
    """, unsafe_allow_html=True)


def login_note():
    st.markdown("""
    """, unsafe_allow_html=True)


def _get_caller_page_name():
    for frame in inspect.stack():
        filename = frame.filename.replace("\\", "/")

        if "components/ui.py" not in filename:
            return os.path.basename(filename)

    return ""


def role_navigation():
       role_pages = {
        "admin": [
            ("🛠️ Admin", "pages/Admin.py"),
            ("📖 Panduan", "pages/10_Panduan_Penggunaan.py"),
        ],
        "guru": [
            ("📊 Dashboard", "pages/6_Dashboard_Guru.py"),
            ("👥 Data Siswa", "pages/7_Data_Siswa.py"),
            ("📝 Jawaban", "pages/8_Jawaban_Siswa.py"),
            ("💬 Feedback", "pages/9_Feedback_Guru.py"),
            ("📖 Panduan Guru", "pages/10_Panduan_Penggunaan.py"),
        ],
        "siswa": [
            ("📊 Dashboard", "pages/1_Dashboard_Siswa.py"),
            ("📚 Materi", "pages/2_Materi_Ekosistem.py"),
            ("🔬 Simulasi", "pages/3_Simulasi_Ekosistem.py"),
            ("✍️ Tanggapan", "pages/4_Tanggapan_Siswa.py"),
            ("💬 Feedback", "pages/5_Feedback_Siswa.py"),
            ("📖 Panduan Siswa", "pages/10_Panduan_Penggunaan.py"),
        ],
    }

    pages = role_pages.get(role, [])

    # === Mobile hamburger navigation (hidden on desktop via CSS) ===
    if pages:
        # Checkbox for CSS-only state
        st.markdown(
            '<input type="checkbox" id="menu-toggle" class="menu-toggle-checkbox" style="display:none;">',
            unsafe_allow_html=True
        )
        
        # Backdrop (acting as a label to close the drawer)
        st.markdown(
            '<label for="menu-toggle" class="menu-backdrop-label"></label>',
            unsafe_allow_html=True
        )

        with st.container(key="mobile_nav"):
            st.markdown(
                '''
                <div class="mobile-header-container">
                    <label for="menu-toggle" class="hamburger-label-btn">☰</label>
                    <div class="mobile-header-brand">🌿 ECOSYSTEM</div>
                </div>
                ''',
                unsafe_allow_html=True
            )

        # Always render the drawer container in Python so it exists in DOM, and let CSS handle show/hide
        with st.container(key="mobile_menu_items"):
            # Drawer Header with Brand and Close Button
            st.markdown(
                '''
                <div class="drawer-header-container">
                    <div class="drawer-brand">🌿 ECOSYSTEM</div>
                    <label for="menu-toggle" class="drawer-close-label-btn">✕</label>
                </div>
                ''',
                unsafe_allow_html=True
            )
            
            st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

            for index, (label, target) in enumerate(pages):
                active = os.path.basename(target) == current_page

                if st.button(
                    label,
                    key=f"mnav_{role}_{index}_{current_page}",
                    use_container_width=True,
                    disabled=active
                ):
                    st.switch_page(target)

            if st.button(
                "🚪 Keluar",
                key=f"mlogout_{role}_{current_page}",
                use_container_width=True
            ):
                from modules.auth import logout
                logout()

    # === Desktop navigation (hidden on mobile via CSS) ===
    if pages:
        with st.container(key="nav_bar"):
            columns = st.columns(len(pages) + 1)

            for index, (label, target) in enumerate(pages):
                with columns[index]:
                    active = os.path.basename(target) == current_page

                    if st.button(
                        label,
                        key=f"nav_{role}_{index}_{current_page}",
                        use_container_width=True,
                        disabled=active
                    ):
                        st.switch_page(target)

            with columns[-1]:
                if st.button(
                    "🚪 Keluar",
                    key=f"logout_{role}_{current_page}",
                    use_container_width=True
                ):
                    from modules.auth import logout
                    logout()

    login_status_card()

    st.divider()

def login_status_card():
    role = st.session_state.get("role", "pengguna")
    nama = (
        st.session_state.get("nama_pengguna")
        or st.session_state.get("name")
        or "Pengguna"
    )
    email = st.session_state.get("email", "-")

    role_lower = str(role).lower()

    role_config = {
        "admin": {
            "label": "Administrator",
            "icon": "🛡️",
            "bg": "linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(243, 232, 255, 0.8) 100%)",
            "border": "rgba(168, 85, 247, 0.2)",
            "text": "#9333ea",
            "glow": "rgba(168, 85, 247, 0.15)",
        },
        "guru": {
            "label": "Guru Pengampu",
            "icon": "👩‍🏫",
            "bg": "linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(224, 242, 254, 0.8) 100%)",
            "border": "rgba(14, 165, 233, 0.2)",
            "text": "#0284c7",
            "glow": "rgba(14, 165, 233, 0.15)",
        },
        "siswa": {
            "label": "Siswa Terdaftar",
            "icon": "🎓",
            "bg": "linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(220, 252, 231, 0.8) 100%)",
            "border": "rgba(34, 197, 94, 0.2)",
            "text": "#16a34a",
            "glow": "rgba(34, 197, 94, 0.15)",
        },
    }

    config = role_config.get(
        role_lower,
        {
            "label": str(role).title(),
            "icon": "👤",
            "bg": "linear-gradient(135deg, rgba(255, 255, 255, 0.8) 0%, rgba(248, 250, 252, 0.8) 100%)",
            "border": "rgba(100, 116, 139, 0.18)",
            "text": "#475569",
            "glow": "rgba(100, 116, 139, 0.1)",
        }
    )

    safe_nama = escape(str(nama))
    safe_email = escape(str(email))
    safe_label = escape(str(config["label"]))
    safe_icon = escape(str(config["icon"]))

    card_html = (
        f"<div class='identity-card-hover' style='"
        f"background:{config['bg']};"
        f"border:1px solid {config['border']};"
        "border-radius:24px;"
        "padding:18px 24px;"
        "margin-bottom:24px;"
        "backdrop-filter: blur(12px);"
        "box-shadow:0 8px 30px rgba(15,23,42,0.03);"
        "display:flex;"
        "align-items:center;"
        "justify-content:space-between;"
        "gap:16px;"
        "flex-wrap:wrap;"
        f"--role-glow:{config['glow']};"
        "'>"

        "<div style='display:flex; align-items:center; gap:16px;'>"

        f"<div style='"
        f"background:linear-gradient(135deg, {config['text']} 0%, #ffffff 200%);"
        "color:white;"
        "width:54px;"
        "height:54px;"
        "border-radius:50%;"
        "display:flex;"
        "align-items:center;"
        "justify-content:center;"
        "font-size:26px;"
        "box-shadow: 0 4px 14px rgba(0,0,0,0.08);"
        "border: 2px solid white;"
        f"'>{safe_icon}</div>"

        "<div>"
        "<div style='font-size:11px; color:#64748b; font-weight:800; text-transform:uppercase; letter-spacing:1px;'>Identitas Akun</div>"
        f"<div style='font-size:19px; color:#0f172a; font-weight:800; font-family:\"Outfit\", sans-serif; margin-top:2px; letter-spacing:-0.3px;'>{safe_nama}</div>"
        f"<div style='font-size:13px; color:#64748b; margin-top:1px;'>{safe_email}</div>"
        "</div>"

        "</div>"

        f"<div style='"
        f"background:{config['text']}15;"
        f"color:{config['text']};"
        f"border:1px solid {config['border']};"
        "border-radius:999px;"
        "padding:6px 14px;"
        "font-size:13px;"
        "font-weight:800;"
        "letter-spacing:0.2px;"
        "'>"
        f"{safe_label}"
        "</div>"

        "</div>"
    )

    st.markdown(card_html, unsafe_allow_html=True)


def global_page_loader():
    import streamlit as st

    st.markdown(
        """
        <style>
            .global-loader {
                position: fixed;
                inset: 0;
                z-index: 999999;
                background: rgba(248, 251, 255, 0.92);
                display: flex;
                align-items: center;
                justify-content: center;
                animation: loaderFadeOut 0.35s ease forwards;
                animation-delay: 1.6s;
                pointer-events: none;
            }

            .global-loader-card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 22px 30px;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.12);
                text-align: center;
                min-width: 200px;
            }

            .global-loader-icon {
                width: 52px;
                height: 52px;
                margin: 0 auto 12px auto;
                border-radius: 16px;
                background: linear-gradient(135deg, #2563eb, #60a5fa);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 27px;
                animation: loaderFloat 1.1s ease-in-out infinite;
                box-shadow: 0 10px 22px rgba(37, 99, 235, 0.25);
            }

            .global-loader-text {
                font-size: 15px;
                font-weight: 800;
                color: #0f172a;
                margin-bottom: 10px;
            }

            .global-loader-dots {
                display: flex;
                justify-content: center;
                gap: 6px;
            }

            .global-loader-dots span {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #2563eb;
                animation: loaderDot 1s infinite ease-in-out;
            }

            .global-loader-dots span:nth-child(2) {
                animation-delay: 0.12s;
            }

            .global-loader-dots span:nth-child(3) {
                animation-delay: 0.24s;
            }

            @keyframes loaderFloat {
                0%, 100% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-6px);
                }
            }

            @keyframes loaderDot {
                0%, 80%, 100% {
                    opacity: 0.35;
                    transform: scale(0.75);
                }
                40% {
                    opacity: 1;
                    transform: scale(1);
                }
            }

            @keyframes loaderFadeOut {
                from {
                    opacity: 1;
                    visibility: visible;
                }
                to {
                    opacity: 0;
                    visibility: hidden;
                }
            }
        </style>

        <div class="global-loader">
            <div class="global-loader-card">
                <div class="global-loader-icon">🌿</div>
                <div class="global-loader-text">Memuat halaman</div>
                <div class="global-loader-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_auth_warning(message, title="Akses Dibatasi", icon="🔐", button_label="Kembali ke Halaman Login", target_page="app.py"):
    load_css()
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 48px 32px;
            background: linear-gradient(135deg, #ffffff 0%, #fffbf2 100%);
            border: 1px solid rgba(217, 119, 6, 0.18);
            border-radius: 28px;
            box-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.08);
            max-width: 540px;
            margin: 60px auto 20px auto;
        ">
            <div style="
                width: 68px;
                height: 68px;
                background: linear-gradient(135deg, #ea580c 0%, #f59e0b 100%);
                color: white;
                border-radius: 22px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 32px;
                margin-bottom: 24px;
                box-shadow: 0 10px 22px rgba(234, 88, 12, 0.2);
            ">
                {icon}
            </div>
            <h2 style="
                font-family: 'Outfit', sans-serif;
                font-size: 24px;
                font-weight: 850;
                color: #1e293b;
                margin: 0 0 12px 0;
                letter-spacing: -0.5px;
            ">
                {title}
            </h2>
            <p style="
                font-size: 15px;
                color: #64748b;
                line-height: 1.6;
                margin: 0;
            ">
                {message}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button(button_label, key="btn_auth_warning_redirect", use_container_width=True):
            st.switch_page(target_page)


def render_inactive_screen(message, email=None):
    load_css()
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 48px 32px;
            background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
            border: 1px solid rgba(220, 38, 38, 0.18);
            border-radius: 28px;
            box-shadow: 0 20px 45px -10px rgba(15, 23, 42, 0.08);
            max-width: 540px;
            margin: 60px auto 20px auto;
        ">
            <div style="
                width: 68px;
                height: 68px;
                background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
                color: white;
                border-radius: 22px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 32px;
                margin-bottom: 24px;
                box-shadow: 0 10px 22px rgba(220, 38, 38, 0.2);
            ">
                🚫
            </div>
            <h2 style="
                font-family: 'Outfit', sans-serif;
                font-size: 24px;
                font-weight: 850;
                color: #1e293b;
                margin: 0 0 12px 0;
                letter-spacing: -0.5px;
            ">
                Akun Belum Aktif
            </h2>
            <p style="
                font-size: 15px;
                color: #64748b;
                line-height: 1.6;
                margin: 0 0 14px 0;
            ">
                {message}
            </p>
            {f'<div style="background:#fef2f2; border:1px solid #fee2e2; border-radius:12px; padding:8px 16px; font-size:14px; color:#dc2626; font-weight:700; display:inline-block;">{email}</div>' if email else ''}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button("Kembali ke Halaman Login", key="btn_inactive_redirect", use_container_width=True):
            st.query_params.clear()
            st.switch_page("app.py")
