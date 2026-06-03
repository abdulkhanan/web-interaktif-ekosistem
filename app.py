import os
import streamlit as st

from database.init_db import init_db
from modules.auth import init_auth, handle_google_callback, make_google_login_url

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

            /* Compact Desktop/Laptop Layout */
            .block-container {
                padding-top: 3.5rem !important;
                padding-bottom: 3.5rem !important;
                max-width: 940px !important;
                transition: all 0.3s ease;
            }

            .st-key-login_shell {
                background: rgba(255, 255, 255, 0.8) !important;
                backdrop-filter: blur(20px) !important;
                border-radius: 32px !important;
                padding: 0 !important;
                overflow: hidden !important;
                box-shadow: 0 30px 80px -20px rgba(15, 23, 42, 0.12) !important;
                border: 1px solid rgba(255, 255, 255, 0.6) !important;
            }

            .st-key-login_shell > div {
                gap: 0 !important;
            }

            .st-key-login_form_panel {
                background: rgba(255, 255, 255, 0.95) !important;
                min-height: 520px !important;
                padding: 42px 38px !important;
                border-radius: 0 32px 32px 0 !important;
                display: flex;
                flex-direction: column;
                justify-content: center;
                transition: all 0.3s ease;
            }

            .st-key-login_image_panel {
                background: #ffffff !important;
                min-height: 520px !important;
                padding: 0 !important;
                border-radius: 32px 0 0 32px !important;
                display: flex !important;
                align-items: stretch !important;
                justify-content: stretch !important;
                overflow: hidden !important;
                position: relative !important;
                transition: all 0.3s ease;
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
                margin-bottom: 38px;
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
                line-height: 1.7;
                margin-bottom: 28px;
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
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }

            .image-placeholder {
                min-height: 520px;
                background: #f8fafc;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 90px;
            }

            /* Responsive Breakpoint: Tablet & Small Screens */
            @media (max-width: 1024px) {
                .block-container {
                    max-width: 90% !important;
                    padding-top: 2.5rem !important;
                }
            }

            @media (max-width: 768px) {
                .st-key-login_image_panel {
                    display: none !important; /* Hide image column */
                }
                .st-key-login_form_panel {
                    border-radius: 32px !important; /* Round all corners */
                    min-height: auto !important;
                    padding: 42px 32px !important;
                }
                .st-key-login_shell div[data-testid="column"] {
                    width: 100% !important;
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


def render_login_page(google_login_url):
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
                        Masuk menggunakan akun Google untuk melanjutkan pembelajaran.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.link_button(
                    "Masuk dengan Google",
                    google_login_url,
                    use_container_width=True
                )




init_db()
init_auth()

global_page_loader()
apply_login_ui_style()

handle_google_callback()

if st.session_state.get("logged_in"):
    redirect_by_role()

google_login_url = make_google_login_url()
render_login_page(google_login_url)