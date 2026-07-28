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

            [data-testid="stSidebar"],
            [data-testid="collapsedControl"] {
                display: none !important;
            }

            header,
            footer {
                visibility: hidden !important;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(5, 150, 105, 0.12), transparent 30%),
                    radial-gradient(circle at bottom right, rgba(2, 132, 199, 0.12), transparent 35%),
                    linear-gradient(135deg, #f0fdf4 0%, #f0f9ff 100%) !important;
                font-family: 'Outfit', 'Inter', sans-serif !important;
            }

            /* Login card: memenuhi viewport tanpa menyisakan ruang kosong */
            .block-container {
                min-height: 100vh !important;
                max-width: 1180px !important;
                padding: 2rem 1.5rem !important;
                display: flex !important;
                align-items: center !important;
                transition: all 0.3s ease;
            }

            .st-key-login_shell {
                width: 100% !important;
                height: min(760px, calc(100vh - 4rem)) !important;
                min-height: 620px !important;
                background: rgba(255, 255, 255, 0.82) !important;
                backdrop-filter: blur(20px) !important;
                border-radius: 32px !important;
                padding: 0 !important;
                overflow: hidden !important;
                box-shadow: 0 30px 80px -20px rgba(15, 23, 42, 0.12) !important;
                border: 1px solid rgba(255, 255, 255, 0.72) !important;
            }

            .st-key-login_shell > div,
            .st-key-login_shell div[data-testid="stHorizontalBlock"] {
                width: 100% !important;
                height: 100% !important;
                min-height: 0 !important;
                gap: 0 !important;
                align-items: stretch !important;
            }

            .st-key-login_shell div[data-testid="column"] {
                min-width: 0 !important;
                height: 100% !important;
                display: flex !important;
                align-items: stretch !important;
            }

            .st-key-login_form_panel {
                width: 100% !important;
                height: 100% !important;
                min-height: 0 !important;
                overflow-y: auto !important;
                overscroll-behavior: contain !important;
                scrollbar-width: thin !important;
                scrollbar-color: rgba(148, 163, 184, 0.55) transparent !important;
                background: rgba(255, 255, 255, 0.97) !important;
                padding: 34px 42px !important;
                border-radius: 0 32px 32px 0 !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: flex-start !important;
                transition: all 0.3s ease;
            }

            .st-key-login_form_panel::-webkit-scrollbar {
                width: 7px;
            }

            .st-key-login_form_panel::-webkit-scrollbar-thumb {
                background: rgba(148, 163, 184, 0.42);
                border-radius: 999px;
            }

            .st-key-login_image_panel {
                width: 100% !important;
                height: 100% !important;
                min-height: 0 !important;
                background: #e8f6f4 !important;
                padding: 0 !important;
                border-radius: 32px 0 0 32px !important;
                display: flex !important;
                align-items: stretch !important;
                justify-content: stretch !important;
                overflow: hidden !important;
                position: relative !important;
                transition: all 0.3s ease;
            }

            .st-key-login_image_panel > div,
            .st-key-login_image_panel [data-testid="stImage"],
            .st-key-login_image_panel [data-testid="stImage"] > div {
                width: 100% !important;
                height: 100% !important;
                min-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            .st-key-login_image_panel::after {
                content: "" !important;
                position: absolute !important;
                inset: 0 !important;
                background: linear-gradient(135deg, rgba(5, 150, 105, 0.15) 0%, rgba(2, 132, 199, 0.15) 100%) !important;
                pointer-events: none !important;
            }

            .brand-row {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 24px;
                transition: all 0.3s ease;
            }

            .brand-logo {
                width: 40px;
                height: 40px;
                border-radius: 12px;
                background: linear-gradient(135deg, #059669, #0284c7);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #ffffff;
                font-size: 20px;
                box-shadow: 0 8px 20px rgba(5, 150, 105, 0.25);
            }

            .brand-name {
                font-family: 'Outfit', sans-serif;
                font-size: 22px;
                font-weight: 900;
                letter-spacing: 1px;
                background: linear-gradient(135deg, #047857 0%, #0284c7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.1;
            }

            .brand-sub {
                font-size: 12px;
                color: #64748b;
                margin-top: 2px;
                font-weight: 600;
            }

            .login-title {
                font-family: 'Outfit', sans-serif;
                font-size: 32px;
                font-weight: 800;
                color: #0f172a;
                line-height: 1.25;
                margin-bottom: 14px;
                letter-spacing: -0.8px;
                transition: all 0.3s ease;
            }

            .login-subtitle {
                font-size: 15px;
                color: #64748b;
                line-height: 1.65;
                margin-bottom: 20px;
                max-width: 420px;
                transition: all 0.3s ease;
            }

            div[data-testid="stLinkButton"] a {
                width: 100%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                border-radius: 14px;
                padding-top: 14px;
                padding-bottom: 14px;
                font-size: 15px;
                font-weight: 700;
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #e2e8f0;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
                text-decoration: none;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            }

            div[data-testid="stLinkButton"] a::before {
                content: "";
                width: 20px;
                height: 20px;
                display: inline-block;
                background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 48 48' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%23FFC107' d='M43.611 20.083H42V20H24v8h11.303C33.651 32.657 29.223 36 24 36c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z'/%3E%3Cpath fill='%23FF3D00' d='M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 16.318 4 9.656 8.337 6.306 14.691z'/%3E%3Cpath fill='%234CAF50' d='M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238C29.211 35.091 26.715 36 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z'/%3E%3Cpath fill='%231976D2' d='M43.611 20.083H42V20H24v8h11.303c-.792 2.237-2.231 4.166-4.087 5.571l.003-.002 6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z'/%3E%3C/svg%3E");
                background-size: contain;
                background-repeat: no-repeat;
                background-position: center;
            }

            div[data-testid="stLinkButton"] a:hover {
                background-color: #f8fafc;
                border-color: #cbd5e1;
                color: #0f172a;
                transform: translateY(-2px);
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
            }

            div[data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
                box-shadow: none !important;
            }

            div[data-testid="stTextInput"] label,
            div[data-testid="stTextInput"] label p {
                color: #334155 !important;
                font-weight: 800 !important;
                font-size: 14px !important;
            }

            div[data-testid="stTextInput"] input {
                background-color: #ffffff !important;
                color: #0f172a !important;
                border: 1.5px solid #e2e8f0 !important;
                border-radius: 14px !important;
                min-height: 46px !important;
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: #0284c7 !important;
                box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.12) !important;
            }

            .stFormSubmitButton button {
                width: 100% !important;
                border-radius: 14px !important;
                min-height: 46px !important;
                font-size: 15px !important;
                font-weight: 800 !important;
                color: #ffffff !important;
                border: none !important;
                background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
                box-shadow: 0 8px 20px rgba(5, 150, 105, 0.24) !important;
            }

            .login-divider {
                display: flex;
                align-items: center;
                gap: 12px;
                margin: 18px 0;
                color: #94a3b8;
                font-size: 13px;
                font-weight: 700;
            }

            .login-divider::before,
            .login-divider::after {
                content: "";
                flex: 1;
                height: 1px;
                background: #e2e8f0;
            }

            .login-footnote {
                margin-top: 20px;
                font-size: 13px;
                color: #64748b;
                line-height: 1.7;
                text-align: center;
            }

            .login-image-wrap img {
                width: 100%;
                height: auto;
                border-radius: 24px;
                display: block;
            }
            .st-key-login_image_panel img {
                width: 100% !important;
                height: 100% !important;
                max-height: none !important;
                object-fit: cover !important;
                object-position: center center !important;
                display: block !important;
                border-radius: 0 !important;
            }

            .image-placeholder {
                width: 100%;
                height: 100%;
                min-height: 100%;
                background: #f8fafc;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 90px;
            }

            /* Responsive Breakpoint: Tablet & Small Screens */
            @media (max-width: 1024px) {
                .block-container {
                    max-width: 94% !important;
                    padding: 1.5rem 1rem !important;
                }

                .st-key-login_shell {
                    height: min(720px, calc(100vh - 3rem)) !important;
                    min-height: 600px !important;
                }

                .st-key-login_form_panel {
                    padding: 30px 32px !important;
                }
            }

            @media (max-width: 768px) {
                .block-container {
                    min-height: 100vh !important;
                    padding: 1rem !important;
                    align-items: flex-start !important;
                }

                .st-key-login_shell {
                    height: auto !important;
                    min-height: 0 !important;
                    border-radius: 26px !important;
                }

                .st-key-login_image_panel {
                    display: none !important;
                }

                .st-key-login_form_panel {
                    height: auto !important;
                    min-height: 0 !important;
                    overflow: visible !important;
                    border-radius: 26px !important;
                    padding: 36px 28px !important;
                }

                .st-key-login_shell div[data-testid="column"] {
                    width: 100% !important;
                    height: auto !important;
                    flex: 1 1 100% !important;
                }
            }

            /* Responsive Breakpoint: Mobile Phones */
            @media (max-width: 480px) {
                .block-container {
                    padding-top: 1.5rem !important;
                    padding-bottom: 1.5rem !important;
                }
                .st-key-login_form_panel {
                    padding: 32px 20px !important;
                }
                .brand-row {
                    margin-bottom: 32px !important;
                }
                .login-title {
                    font-size: 26px !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_login_page(google_login_url=None):
    with st.container(key="login_shell"):
        col_image, col_login = st.columns([1.38, 0.92], gap=None)

        with col_image:
            with st.container(key="login_image_panel"):
                image_path = "assets/images/login_illustration.webp"

                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.markdown(
                        """
                        <div class="image-placeholder">🌿</div>
                        """,
                        unsafe_allow_html=True
                    )

        with col_login:
            with st.container(key="login_form_panel"):
                st.markdown(
                    """
                    <div class="brand-row">
                        <div class="brand-logo">🌿</div>
                        <div>
                            <div class="brand-name">ECOSYSTEM</div>
                            <div class="brand-sub">Guided Inquiry Learning</div>
                        </div>
                    </div>

                    <div class="login-title">
                        Web Pembelajaran Ekosistem
                    </div>

                    <div class="login-subtitle">
                        Masuk dengan email-password atau Google. Pengguna baru dapat mendaftar, lalu menunggu akun diaktifkan oleh admin.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                tab_login, tab_register = st.tabs(["Masuk", "Daftar Akun"])

                with tab_login:
                    with st.form("form_login_email_password"):
                        email = st.text_input("Email", placeholder="nama@email.com")
                        password = st.text_input("Password", type="password", placeholder="Masukkan password")
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
                        st.link_button(
                            "Masuk dengan Google",
                            google_login_url,
                            use_container_width=True
                        )

                with tab_register:
                    with st.form("form_daftar_akun"):
                        nama_daftar = st.text_input("Nama lengkap", placeholder="Masukkan nama lengkap")
                        email_daftar = st.text_input("Email pendaftaran", placeholder="nama@email.com")
                        password_daftar = st.text_input("Password", type="password", placeholder="Minimal 6 karakter")
                        konfirmasi_password = st.text_input("Konfirmasi password", type="password", placeholder="Ulangi password")
                        role_daftar = st.selectbox("Daftar sebagai", ["siswa", "guru"], index=0)
                        kelas_daftar = st.text_input("Kelas / Instansi", placeholder="Contoh: XI IPA 1 / Guru Biologi")
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
                    '<div class="login-footnote">Role yang tersedia: siswa, guru, dan admin. Akun admin dibuat atau diubah melalui menu Daftar Pengguna.</div>',
                    unsafe_allow_html=True
                )




init_db()
init_auth()

global_page_loader()
apply_login_ui_style()

handle_google_callback()

if st.session_state.get("logged_in"):
    redirect_by_role()

google_login_url = make_google_login_url() if is_google_login_available() else None
render_login_page(google_login_url)