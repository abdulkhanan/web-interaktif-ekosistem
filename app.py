import os
import streamlit as st

from database.init_db import init_db
from modules.auth import init_auth, handle_google_callback, make_google_login_url, login_with_email_password, is_google_login_available
from database.queries import create_user_manual

from components.ui import global_page_loader


st.set_page_config(
    page_title="Login Web Pembelajaran Ekosistem",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def redirect_by_role():
    role = st.session_state.get("role")
    if role == "admin":
        st.switch_page("pages/Admin.py")
    elif role == "guru":
        st.switch_page("pages/6_Dashboard_Guru.py")
    elif role == "siswa":
        st.switch_page("pages/1_Dashboard_Siswa.py")


def apply_login_ui_style():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

            @keyframes fadeInUp {
                0%   { opacity: 0; transform: translateY(28px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            /* ── Hide Streamlit chrome ── */
            .st-key-hidden_cookies,
            .st-key-hidden_cookies_logout,
            .st-key-hidden_cookies [data-testid="stSkeleton"],
            .st-key-hidden_cookies_logout [data-testid="stSkeleton"],
            .element-container:has(iframe[height="0"]),
            .element-container:has(iframe[height="0px"]) { display: none !important; }

            [data-testid="stSidebar"],
            [data-testid="collapsedControl"] { display: none !important; }

            header, footer { visibility: hidden !important; }

            /* ── Page background ── */
            .stApp {
                background: linear-gradient(150deg, #daeef6 0%, #e2f4ec 55%, #d8eef5 100%) !important;
                font-family: 'Outfit', 'Inter', sans-serif !important;
            }

            /* ── Center narrow container ── */
            .block-container {
                padding-top: 3rem !important;
                padding-bottom: 3rem !important;
                max-width: 660px !important;
            }

            /* ── Outer white card ── */
            .st-key-login_shell {
                animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
                background: #ffffff !important;
                border-radius: 28px !important;
                padding: 0 !important;
                overflow: hidden !important;
                box-shadow: 0 24px 64px -12px rgba(15, 23, 42, 0.15) !important;
                border: 1px solid rgba(226, 232, 240, 0.5) !important;
            }

            /* ── Image section ── */
            .login-image-section {
                width: 100%;
                overflow: hidden;
                border-radius: 28px 28px 0 0;
            }
            .login-image-section img {
                width: 100%;
                height: 330px;
                object-fit: cover;
                object-position: center 30%;
                display: block;
            }

            /* ── Form section ── */
            .st-key-login_form_panel {
                padding: 42px 48px 48px 48px !important;
            }

            /* ── Brand row ── */
            .brand-row {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 14px;
            }
            .brand-logo {
                width: 38px;
                height: 38px;
                border-radius: 10px;
                background: linear-gradient(135deg, #059669 0%, #0d9488 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #ffffff;
                font-size: 19px;
                flex-shrink: 0;
                box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
            }
            .brand-name {
                font-family: 'Outfit', sans-serif;
                font-size: 19px;
                font-weight: 900;
                letter-spacing: 1.8px;
                color: #059669;
                line-height: 1;
            }

            /* ── Title & subtitle ── */
            .login-title {
                font-family: 'Outfit', sans-serif;
                font-size: 23px;
                font-weight: 800;
                color: #0f172a;
                line-height: 1.25;
                margin-bottom: 5px;
                letter-spacing: -0.3px;
            }
            .login-subtitle {
                font-size: 13px;
                color: #64748b;
                line-height: 1.55;
                margin-bottom: 18px;
            }

            /* ── Tabs ── */
            div[data-testid="stTabs"] [data-baseweb="tab-list"] {
                gap: 0 !important;
                border-bottom: 1.5px solid #e2e8f0 !important;
                margin-bottom: 14px !important;
                background: transparent !important;
            }
            div[data-testid="stTabs"] [data-baseweb="tab"] {
                font-weight: 700 !important;
                font-size: 14px !important;
                color: #94a3b8 !important;
                padding: 8px 20px 10px 0 !important;
                border: none !important;
                background: transparent !important;
                margin-right: 12px !important;
            }
            div[data-testid="stTabs"] [aria-selected="true"] {
                color: #059669 !important;
                border-bottom: 2.5px solid #059669 !important;
            }
            div[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }
            div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }

            /* ── Form ── */
            div[data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                box-shadow: none !important;
            }

            /* ── Input labels ── */
            div[data-testid="stTextInput"] label,
            div[data-testid="stTextInput"] label p {
                color: #1e293b !important;
                font-weight: 700 !important;
                font-size: 13px !important;
                margin-bottom: 4px !important;
            }

            /* ── Input fields ── */
            div[data-testid="stTextInput"] div[data-baseweb="input"] {
                border-radius: 10px !important;
                border: 1.5px solid #e2e8f0 !important;
                background-color: #f8fafc !important;
                overflow: hidden !important;
                transition: border-color 0.2s, box-shadow 0.2s, background-color 0.2s !important;
            }
            div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
                border-color: #059669 !important;
                box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.12) !important;
                background-color: #ffffff !important;
            }
            div[data-testid="stTextInput"] input {
                background-color: transparent !important;
                color: #0f172a !important;
                min-height: 44px !important;
                border: none !important;
                box-shadow: none !important;
                font-size: 14px !important;
                padding-left: 14px !important;
                padding-right: 14px !important;
            }

            /* ── Selectbox ── */
            div[data-testid="stSelectbox"] label,
            div[data-testid="stSelectbox"] label p {
                color: #1e293b !important;
                font-weight: 700 !important;
                font-size: 13px !important;
            }
            div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
                border-radius: 10px !important;
                border: 1.5px solid #e2e8f0 !important;
                background-color: #f8fafc !important;
                min-height: 44px !important;
                font-size: 14px !important;
            }

            /* ── Submit button ── */
            .stFormSubmitButton button {
                width: 100% !important;
                border-radius: 10px !important;
                min-height: 46px !important;
                font-size: 15px !important;
                font-weight: 800 !important;
                color: #ffffff !important;
                border: none !important;
                background: linear-gradient(135deg, #059669 0%, #0d9488 100%) !important;
                box-shadow: 0 4px 16px rgba(5, 150, 105, 0.32) !important;
                transition: all 0.25s ease !important;
                margin-top: 6px !important;
            }
            .stFormSubmitButton button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 22px rgba(5, 150, 105, 0.4) !important;
                background: linear-gradient(135deg, #047857 0%, #0f766e 100%) !important;
            }

            /* ── Divider ── */
            .login-divider {
                display: flex;
                align-items: center;
                gap: 10px;
                margin: 12px 0;
                color: #94a3b8;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 0.4px;
            }
            .login-divider::before,
            .login-divider::after {
                content: "";
                flex: 1;
                height: 1px;
                background: #e2e8f0;
            }

            /* ── Google button ── */
            div[data-testid="stLinkButton"] a {
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 10px !important;
                width: 100% !important;
                border-radius: 10px !important;
                padding: 11px 20px !important;
                font-size: 14px !important;
                font-weight: 700 !important;
                background-color: #ffffff !important;
                color: #334155 !important;
                border: 1.5px solid #e2e8f0 !important;
                box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05) !important;
                text-decoration: none !important;
                transition: all 0.2s ease !important;
            }
            div[data-testid="stLinkButton"] a::before {
                content: "" !important;
                width: 18px !important;
                height: 18px !important;
                display: inline-block !important;
                background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 48 48' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%23FFC107' d='M43.611 20.083H42V20H24v8h11.303C33.651 32.657 29.223 36 24 36c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z'/%3E%3Cpath fill='%23FF3D00' d='M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 16.318 4 9.656 8.337 6.306 14.691z'/%3E%3Cpath fill='%234CAF50' d='M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238C29.211 35.091 26.715 36 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z'/%3E%3Cpath fill='%231976D2' d='M43.611 20.083H42V20H24v8h11.303c-.792 2.237-2.231 4.166-4.087 5.571l.003-.002 6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z'/%3E%3C/svg%3E") !important;
                background-size: contain !important;
                background-repeat: no-repeat !important;
                background-position: center !important;
                flex-shrink: 0 !important;
            }
            div[data-testid="stLinkButton"] a:hover {
                background-color: #f8fafc !important;
                border-color: #cbd5e1 !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 16px rgba(15, 23, 42, 0.09) !important;
            }

            /* ── Footer note ── */
            .login-note {
                margin-top: 12px;
                font-size: 12px;
                color: #94a3b8;
                font-weight: 500;
                display: flex;
                align-items: flex-start;
                gap: 5px;
                line-height: 1.5;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_login_page(google_login_url=None):
    # Outer card wrapper
    with st.container(key="login_shell"):

        # ── Image on top ──
        image_path = "assets/images/login_illustration.png"
        if os.path.exists(image_path):
            st.markdown(
                f"""
                <div class="login-image-section">
                    <img src="data:image/png;base64,{_img_to_b64(image_path)}" alt="Ekosistem" />
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="height:220px; background:linear-gradient(135deg,#d1fae5,#cffafe); border-radius:28px 28px 0 0; display:flex; align-items:center; justify-content:center; font-size:80px;">🌿</div>',
                unsafe_allow_html=True
            )

        # ── Form below image ──
        with st.container(key="login_form_panel"):
            st.markdown(
                """
                <div class="brand-row">
                    <div class="brand-logo">🌿</div>
                    <div class="brand-name">EKOSISTEM</div>
                </div>
                <div class="login-title">Web Pembelajaran Ekosistem</div>
                <div class="login-subtitle">Belajar, memahami, dan menjaga keseimbangan alam bersama. Jelajahi ekosistem di sekitarmu!</div>
                """,
                unsafe_allow_html=True
            )

            tab_login, tab_register = st.tabs(["Masuk", "Daftar Akun"])

            with tab_login:
                with st.form("form_login_email_password"):
                    email = st.text_input("Email", placeholder="✉️  Masukkan email Anda")
                    password = st.text_input("Password", type="password", placeholder="🔒  Masukkan password Anda")
                    submit = st.form_submit_button("Masuk dengan Email & Password", use_container_width=True)

                    if submit:
                        success, message = login_with_email_password(email, password)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

                if google_login_url:
                    st.markdown('<div class="login-divider">atau</div>', unsafe_allow_html=True)
                    st.link_button("Masuk dengan Google", google_login_url, use_container_width=True)

                st.markdown(
                    '<div class="login-note">🛡️ Pengguna baru dapat mendaftar dan menunggu aktivasi admin.</div>',
                    unsafe_allow_html=True
                )

            with tab_register:
                with st.form("form_daftar_akun"):
                    nama_daftar = st.text_input("Nama lengkap", placeholder="👤  Masukkan nama lengkap")
                    email_daftar = st.text_input("Email pendaftaran", placeholder="✉️  nama@email.com")
                    password_daftar = st.text_input("Password", type="password", placeholder="🔒  Minimal 6 karakter")
                    konfirmasi_password = st.text_input("Konfirmasi password", type="password", placeholder="🔒  Ulangi password")
                    role_daftar = st.selectbox("Daftar sebagai", ["siswa", "guru"], index=0)
                    kelas_daftar = st.text_input("Kelas / Instansi", placeholder="🏫  Contoh: XI IPA 1 / Guru Biologi")
                    daftar = st.form_submit_button("Daftar Akun", use_container_width=True)

                    if daftar:
                        if not nama_daftar.strip() or not email_daftar.strip():
                            st.error("Nama dan email wajib diisi.")
                        elif len(password_daftar) < 6:
                            st.error("Password minimal 6 karakter.")
                        elif password_daftar != konfirmasi_password:
                            st.error("Konfirmasi password tidak sama.")
                        else:
                            try:
                                create_user_manual(
                                    nama=nama_daftar,
                                    email=email_daftar,
                                    role=role_daftar,
                                    kelas=kelas_daftar,
                                    status="nonaktif",
                                    password=password_daftar,
                                )
                                st.success("Pendaftaran berhasil. Akun Anda menunggu aktivasi admin sebelum dapat digunakan.")
                            except Exception as error:
                                st.error(f"Pendaftaran gagal: {error}")

                st.markdown(
                    '<div class="login-note">🛡️ Akun baru akan ditinjau dan diaktifkan oleh admin.</div>',
                    unsafe_allow_html=True
                )


def _img_to_b64(path):
    import base64
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


init_db()
init_auth()

global_page_loader()
apply_login_ui_style()

handle_google_callback()

if st.session_state.get("logged_in"):
    redirect_by_role()

google_login_url = make_google_login_url() if is_google_login_available() else None
render_login_page(google_login_url)