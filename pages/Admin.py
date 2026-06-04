from html import escape

import matplotlib.pyplot as plt
import streamlit as st

from database.init_db import init_db
from database.queries import get_users_df, get_user_counts, get_dashboard_counts_with_status, get_progress_siswa_df, update_user_name, update_user_data as update_user_data_db
from modules.auth import require_role
from components.ui import load_css


st.set_page_config(
    page_title="Admin - Web Ekosistem",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================
# INIT
# =========================
init_db()
require_role(["admin"])
load_css()



# =========================
# DATABASE HELPER
# =========================
def update_admin_name(id_user, nama_baru):
    update_user_name(id_user, nama_baru)

    st.session_state["nama_pengguna"] = nama_baru.strip()
    st.session_state["nama"] = nama_baru.strip()
    st.session_state["name"] = nama_baru.strip()


def update_user_data(id_user, nama_baru, role_baru, status_baru):
    update_user_data_db(id_user, nama_baru, role_baru, status_baru)

# =========================
# SESSION MENU
# =========================
if "admin_menu" not in st.session_state:
    st.session_state["admin_menu"] = "Dashboard"


# =========================
# DATA
# =========================
df_users = get_users_df()
counts = get_user_counts()

current_user_id = int(st.session_state.get("id_user", 0))

current_name = (
    st.session_state.get("nama_pengguna")
    or st.session_state.get("nama")
    or st.session_state.get("name")
    or "Admin"
)

current_email = st.session_state.get("email", "-")
current_role = st.session_state.get("role", "admin")


def get_admin_login_data():
    if df_users.empty:
        return {
            "id_user": current_user_id,
            "nama": current_name,
            "email": current_email,
            "role": current_role,
            "status": "aktif"
        }

    if current_user_id:
        selected = df_users[df_users["id_user"].astype(int) == current_user_id]
        if not selected.empty:
            return selected.iloc[0].to_dict()

    admin_rows = df_users[df_users["role"].astype(str).str.lower() == "admin"]
    if not admin_rows.empty:
        return admin_rows.iloc[0].to_dict()

    return df_users.iloc[0].to_dict()


admin_data = get_admin_login_data()

current_name = str(admin_data.get("nama", "Admin"))
current_email = str(admin_data.get("email", "-"))
current_role = str(admin_data.get("role", "admin"))
current_status = str(admin_data.get("status", "aktif"))


# =========================
# ADMIN RESPONSIVE NAVIGATION
# =========================
def admin_navigation():
    menu_items = [
        ("📊 Dashboard", "Dashboard"),
        ("👤 Informasi Admin", "Informasi Admin"),
        ("👥 Daftar Pengguna", "Daftar Pengguna"),
    ]

    current_menu = st.session_state.get("admin_menu", "Dashboard")

    st.markdown(
        '<input type="checkbox" id="menu-toggle" class="menu-toggle-checkbox" style="display:none;">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<label for="menu-toggle" class="menu-backdrop-label"></label>',
        unsafe_allow_html=True
    )

    # Mobile header, tampil sebagai burger menu di layar kecil
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

    # Mobile drawer menu
    with st.container(key="mobile_menu_items"):
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

        for index, (label, value) in enumerate(menu_items):
            active = current_menu == value
            if st.button(
                label,
                key=f"admin_mnav_{index}_{value}",
                use_container_width=True,
                disabled=active
            ):
                st.session_state["admin_menu"] = value
                st.rerun()

        if st.button("🚪 Keluar", key="admin_mlogout", use_container_width=True):
            from modules.auth import logout
            logout()

    # Desktop navigation, tampil horizontal di layar besar
    with st.container(key="nav_bar"):
        columns = st.columns(len(menu_items) + 1)

        for index, (label, value) in enumerate(menu_items):
            with columns[index]:
                active = current_menu == value
                if st.button(
                    label,
                    key=f"admin_nav_{index}_{value}",
                    use_container_width=True,
                    disabled=active
                ):
                    st.session_state["admin_menu"] = value
                    st.rerun()

        with columns[-1]:
            if st.button("🚪 Keluar", key="admin_logout", use_container_width=True):
                from modules.auth import logout
                logout()

    st.markdown(
        '''
        <style>

.admin-nav-spacer {
            height: 28px !important;
        }

        .main-title {
            margin-top: 0 !important;
            margin-bottom: 8px !important;
        }

        .sub-text {
            margin-bottom: 22px !important;
        }

        @media (max-width: 768px) {
            .admin-nav-spacer {
                height: 14px !important;
            }

            .block-container {
                padding-top: 0.2rem !important;
            }

            .main-title {
                font-size: 36px !important;
                line-height: 1.1 !important;
                margin-top: 0 !important;
                margin-bottom: 12px !important;
            }

            .sub-text {
                font-size: 17px !important;
                line-height: 1.7 !important;
                margin-bottom: 28px !important;
            }
        }
        /* Judul section agar tidak putih */
        .admin-section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 30px;
            font-weight: 900;
            color: #000000 !important;
            margin: 8px 0 8px 0;
            line-height: 1.2;
        }

        .admin-section-subtitle {
            color: #64748b !important;
            font-size: 16px;
            margin-bottom: 22px;
            line-height: 1.6;
        }

        /* Label dan input pencarian */
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] label p {
            color: #334155 !important;
            font-weight: 800 !important;
            font-size: 15px !important;
        }

        div[data-testid="stTextInput"] input {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1.5px solid rgba(15, 23, 42, 0.18) !important;
            border-radius: 14px !important;
            min-height: 48px !important;
            font-size: 15px !important;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04) !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #94a3b8 !important;
            opacity: 1 !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.12) !important;
        }

        /* Card daftar pengguna */
        div[class*="st-key-user_card_"] {
            background: rgba(255, 255, 255, 0.92) !important;
            border: 1px solid rgba(226, 232, 240, 0.95) !important;
            border-radius: 22px !important;
            padding: 20px 22px !important;
            margin-bottom: 16px !important;
            box-shadow: 0 12px 28px -16px rgba(15, 23, 42, 0.18) !important;
        }

        .user-card-grid {
            display: grid;
            grid-template-columns: minmax(0, 1.8fr) minmax(160px, 0.55fr) minmax(160px, 0.55fr);
            gap: 18px;
            align-items: center;
        }

        .user-main-info {
            display: flex;
            align-items: center;
            gap: 14px;
            min-width: 0;
        }

        .user-avatar {
            width: 52px;
            height: 52px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(5, 150, 105, 0.12), rgba(2, 132, 199, 0.12));
            font-size: 24px;
            flex-shrink: 0;
        }

        .user-name {
            color: #0f172a !important;
            font-size: 18px;
            font-weight: 900;
            line-height: 1.3;
            word-break: break-word;
        }

        .user-email {
            color: #64748b !important;
            font-size: 14px;
            font-weight: 600;
            margin-top: 4px;
            word-break: break-word;
        }

        .user-field-label {
            color: #64748b !important;
            font-size: 11px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
        }

        .user-role-badge,
        .user-status-badge {
            display: inline-flex;
            align-items: center;
            width: fit-content;
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 900;
            text-transform: capitalize;
        }

        .role-admin {
            background: rgba(124, 58, 237, 0.12);
            color: #6d28d9;
        }

        .role-guru {
            background: rgba(2, 132, 199, 0.12);
            color: #0369a1;
        }

        .role-siswa {
            background: rgba(5, 150, 105, 0.12);
            color: #047857;
        }

        .status-aktif {
            background: rgba(22, 163, 74, 0.12);
            color: #15803d;
        }

        .status-nonaktif {
            background: rgba(239, 68, 68, 0.12);
            color: #b91c1c;
        }

        div[class*="st-key-user_card_"] button {
            border-radius: 14px !important;
            min-height: 40px !important;
            background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 900 !important;
            box-shadow: 0 8px 18px rgba(5, 150, 105, 0.22) !important;
        }

        div[class*="st-key-user_card_"] button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 10px 22px rgba(2, 132, 199, 0.28) !important;
        }

        @media (max-width: 768px) {
            .admin-section-title {
                font-size: 28px;
                color: #000000 !important;
            }

            .admin-section-subtitle {
                color: #64748b !important;
            }

            div[class*="st-key-user_card_"] {
                padding: 18px !important;
                border-radius: 20px !important;
            }

            .user-card-grid {
                grid-template-columns: 1fr;
                gap: 16px;
            }

            .user-main-info {
                align-items: flex-start;
            }

            .user-avatar {
                width: 48px;
                height: 48px;
                border-radius: 16px;
                font-size: 22px;
            }

            .user-name {
                font-size: 17px;
            }

            .user-email {
                font-size: 13px;
            }

            .user-field-label {
                margin-bottom: 6px;
            }
        }

        </style>
        ''',
        unsafe_allow_html=True
    )


admin_navigation()


# =========================
# STYLE TEMA LOGIN
# =========================
st.markdown(
    """
    <style>
        /* Header jangan dihapus agar tombol sidebar bawaan Streamlit tetap muncul */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(5, 150, 105, 0.08), transparent 24%),
                radial-gradient(circle at bottom right, rgba(2, 132, 199, 0.08), transparent 28%),
                linear-gradient(135deg, #f0fdf4 0%, #f0f9ff 100%);
            font-family: 'Outfit', 'Inter', sans-serif !important;
        }

        .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px;
        }

        /* Sidebar bawaan Streamlit */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f0fdf4 0%, #f0f9ff 100%) !important;
            border-right: 1px solid rgba(5, 150, 105, 0.1) !important;
        }

        section[data-testid="stSidebar"] h1 {
            color: #047857;
            font-size: 28px;
            font-weight: 900;
            line-height: 1.25;
            margin-bottom: 18px;
            font-family: 'Outfit', sans-serif;
        }

        /* Inactive Sidebar Buttons */
        div[class*="st-key-sidebar_"] button {
            width: 100%;
            border-radius: 14px !important;
            min-height: 46px !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            margin-bottom: 12px;
            background: #ffffff !important;
            color: #475569 !important;
            border: 1px solid rgba(226, 232, 240, 0.8) !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-align: left !important;
            padding-left: 18px !important;
        }

        div[class*="st-key-sidebar_"] button:hover {
            background: #f8fafc !important;
            color: #0284c7 !important;
            border-color: rgba(2, 132, 199, 0.3) !important;
            transform: translateX(2px) !important;
        }

        /* Active Sidebar Buttons */
        div[class*="st-key-active_sidebar_"] button {
            background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 6px 16px rgba(5, 150, 105, 0.25) !important;
            transform: translateX(4px) !important;
        }

        div[class*="st-key-active_sidebar_"] button:hover {
            color: #ffffff !important;
            box-shadow: 0 8px 20px rgba(2, 132, 199, 0.35) !important;
        }

        /* Logout Button Specific Styling */
        div.st-key-sidebar_logout button {
            border: 1px solid rgba(239, 68, 68, 0.15) !important;
            color: #ef4444 !important;
            margin-top: 24px;
        }

        div.st-key-sidebar_logout button:hover {
            background: rgba(239, 68, 68, 0.06) !important;
            color: #dc2626 !important;
            border-color: #ef4444 !important;
            transform: translateY(1px) !important;
        }

        /* Judul halaman */
        .main-title {
            font-family: 'Outfit', sans-serif;
            font-size: 40px;
            font-weight: 900;
            color: #0f172a;
            line-height: 1.15;
            margin-bottom: 8px;
        }

        .main-title span {
            color: #059669;
        }

        .sub-text {
            font-size: 17px;
            color: #64748b;
            line-height: 1.7;
            margin-bottom: 18px;
            max-width: 850px;
        }

        /* Card statistik */
        .metric-card {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 20px;
            box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
            padding: 22px 24px;
            min-height: 120px;
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
        }

        .metric-label {
            font-size: 15px;
            color: #64748b;
            font-weight: 800;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .metric-value {
            font-family: 'Outfit', sans-serif;
            font-size: 42px;
            color: #059669;
            font-weight: 900;
            line-height: 1;
        }

        /* Informasi admin */
        .admin-label {
            font-size: 15px;
            color: #64748b;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .admin-value {
            font-size: 18px;
            color: #0f172a;
            font-weight: 800;
            margin-bottom: 16px;
            word-break: break-word;
            overflow-wrap: anywhere;
        }

        .role-badge {
            display: inline-block;
            padding: 7px 14px;
            border-radius: 999px;
            background: #dbeafe;
            color: #1d4ed8;
            font-weight: 800;
            font-size: 14px;
        }

        .status-badge {
            display: inline-block;
            padding: 7px 14px;
            border-radius: 999px;
            background: #dcfce7;
            color: #15803d;
            font-weight: 800;
            font-size: 14px;
        }

        .status-badge-nonaktif {
            display: inline-block;
            padding: 7px 14px;
            border-radius: 999px;
            background: #fee2e2;
            color: #b91c1c;
            font-weight: 800;
            font-size: 14px;
        }

        /* Input */
        .stTextInput input,
        .stSelectbox div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            min-height: 44px;
            background-color: #ffffff !important;
            border: 1px solid rgba(226, 232, 240, 0.8) !important;
            transition: all 0.2s ease !important;
        }
        .stTextInput input:focus,
        .stSelectbox div[data-baseweb="select"] > div:focus {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.1) !important;
        }

        /* Hilangkan padding kolom agar tabel lebih menyatu */
        div[data-testid="column"] {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
        }

        /* Tabel pengguna modern */
        .user-table-head {
            background: transparent;
            border: none !important;
            padding: 12px 8px;
            font-weight: 950;
            color: #047857;
            margin: 0 !important;
            border-radius: 0 !important;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 0.5px;
        }

        .user-table-cell {
            background: transparent;
            border: none !important;
            padding: 12px 8px;
            min-height: 62px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: #0f172a;
            word-break: break-word;
            overflow-wrap: anywhere;
            margin: 0 !important;
            border-radius: 0 !important;
        }
        .user-name-text {
            font-size: 15px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.35;
        }

        .user-email-text {
            font-size: 13px;
            color: #64748b;
            line-height: 1.35;
            margin-top: 2px;
        }

        .role-pill {
            display: inline-block;
            width: fit-content;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(2, 132, 199, 0.1);
            color: #0284c7;
            font-size: 13px;
            font-weight: 800;
            text-transform: capitalize;
        }

        .status-pill-aktif {
            display: inline-block;
            width: fit-content;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(5, 150, 105, 0.1);
            color: #059669;
            font-size: 13px;
            font-weight: 800;
            text-transform: capitalize;
        }

        .status-pill-nonaktif {
            display: inline-block;
            width: fit-content;
            padding: 6px 12px;
            border-radius: 999px;
            background: #fee2e2;
            color: #b91c1c;
            font-size: 13px;
            font-weight: 800;
            text-transform: capitalize;
        }

        /* Cell aksi agar baris ikut menyatu */
        div[class*="st-key-user_action_cell_"] {
            border: none !important;
            min-height: 62px;
            display: flex;
            align-items: center;
            padding: 10px 8px;
        }

        /* Tombol edit kecil */
        div[class*="st-key-user_action_cell_"] button {
            background-color: #ef4444 !important;
            color: white !important;
            border: 1px solid #ef4444 !important;
            border-radius: 10px !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            min-height: 34px !important;
            padding: 0.15rem 0.65rem !important;
            width: auto !important;
        }

        div[class*="st-key-user_action_cell_"] button:hover {
            background-color: #dc2626 !important;
            border-color: #dc2626 !important;
            color: white !important;
            transform: translateY(-1px);
        }

        /* Form edit pengguna */
        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
        }

        /* Tombol form */
        .stButton button,
        .stFormSubmitButton button {
            border-radius: 14px !important;
            min-height: 44px !important;
            font-weight: 800 !important;
            transition: all 0.25s ease !important;
        }

        .stFormSubmitButton button {
            background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(5, 150, 105, 0.2) !important;
        }

        .stFormSubmitButton button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px rgba(2, 132, 199, 0.3) !important;
        }

        div[data-testid="stPyplot"] {
            background: #ffffff;
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
            width: fit-content;
        }

            /* ===== DASHBOARD V2 ENHANCED STYLES ===== */
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

            /* Card color variants */
            .mc-blue .mc-icon { background: rgba(2, 132, 199, 0.1); }
            .mc-blue .mc-value { color: #0284c7; }
            .mc-green .mc-icon { background: rgba(5, 150, 105, 0.1); }
            .mc-green .mc-value { color: #059669; }
            .mc-teal .mc-icon { background: rgba(20, 184, 166, 0.1); }
            .mc-teal .mc-value { color: #0d9488; }
            .mc-purple .mc-icon { background: rgba(124, 58, 237, 0.1); }
            .mc-purple .mc-value { color: #7c3aed; }
            .mc-emerald .mc-icon { background: rgba(16, 185, 129, 0.1); }
            .mc-emerald .mc-value { color: #10b981; }
            .mc-amber .mc-icon { background: rgba(245, 158, 11, 0.1); }
            .mc-amber .mc-value { color: #f59e0b; }

            /* Alert Banner */
            .alert-banner {
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), rgba(239, 68, 68, 0.06));
                border: 1px solid rgba(245, 158, 11, 0.25);
                border-left: 4px solid #f59e0b;
                border-radius: 14px;
                padding: 16px 20px;
                font-size: 15px;
                color: #92400e;
                font-weight: 600;
                margin-bottom: 8px;
                line-height: 1.6;
            }

            /* Info Card */
            .info-card {
                background: #ffffff;
                border: 1px solid rgba(226, 232, 240, 0.8);
                border-radius: 20px;
                box-shadow: 0 10px 25px -10px rgba(15, 23, 42, 0.05);
                padding: 24px;
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

            /* Recent users mini-table */
            .recent-user-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid rgba(226, 232, 240, 0.5);
            }
            .recent-user-item:last-child { border-bottom: none; }
            .recent-user-info { flex: 1; }
            .recent-user-name {
                font-size: 14px;
                font-weight: 700;
                color: #0f172a;
            }
            .recent-user-email {
                font-size: 12px;
                color: #94a3b8;
                margin-top: 1px;
            }
            .recent-user-badge {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 11px;
                font-weight: 700;
                text-transform: capitalize;
            }
            .recent-user-badge-admin { background: rgba(124, 58, 237, 0.1); color: #7c3aed; }
            .recent-user-badge-guru { background: rgba(2, 132, 199, 0.1); color: #0284c7; }
            .recent-user-badge-siswa { background: rgba(5, 150, 105, 0.1); color: #059669; }

            /* Progress bars */
            .progress-item { margin-bottom: 18px; }
            .progress-item:last-child { margin-bottom: 0; }
            .progress-label {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 6px;
            }
            .progress-text {
                font-size: 14px;
                font-weight: 600;
                color: #334155;
            }
            .progress-count {
                font-size: 13px;
                font-weight: 700;
                color: #64748b;
            }
            .progress-bar-bg {
                width: 100%;
                height: 10px;
                background: rgba(226, 232, 240, 0.6);
                border-radius: 999px;
                overflow: hidden;
            }
            .progress-bar-fill {
                height: 100%;
                border-radius: 999px;
                transition: width 0.6s ease;
            }
            .pb-green { background: linear-gradient(90deg, #059669, #10b981); }
            .pb-blue { background: linear-gradient(90deg, #0284c7, #38bdf8); }
            .pb-purple { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
            .pb-amber { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

            @media (max-width: 768px) {
                .metric-card-v2 { min-height: 85px; padding: 16px 18px; }
                .mc-value { font-size: 26px; }
                .mc-icon { width: 44px; height: 44px; font-size: 20px; }
                .info-card { padding: 18px; }
            }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        /* Paksa tulisan halaman Admin jadi hitam */
        .admin-section-title,
        .admin-section-subtitle,
        .admin-label,
        .admin-value,
        .user-field-label,
        .user-name,
        .user-email,
        .user-role-badge,
        .user-status-badge,
        .role-admin,
        .role-guru,
        .role-siswa,
        .status-aktif,
        .status-nonaktif {
            color: #0f172a !important;
        }

        /* Judul Informasi Admin dan Daftar Pengguna */
        .admin-section-title {
            color: #0f172a !important;
        }

        /* Teks kecil di bawah judul */
        .admin-section-subtitle {
            color: #0f172a !important;
        }

        /* Label Role dan Status */
        .user-field-label {
            color: #0f172a !important;
        }

        /* Isi badge siswa, admin, guru, aktif */
        .user-role-badge,
        .user-status-badge {
            color: #0f172a !important;
        }

        /* Label input seperti Cari pengguna */
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] label p {
            color: #0f172a !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class="main-title">Dashboard <span>Admin</span></div>
    <div class="sub-text">
        Kelola data pengguna, pantau jumlah akun, dan atur akses pembelajaran ekosistem.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# MENU 1: DASHBOARD
# =========================
if st.session_state["admin_menu"] == "Dashboard":

    # Ambil data tambahan untuk dashboard
    dashboard_counts = get_dashboard_counts_with_status()
    jml_siswa_tgp, jml_tanggapan, jml_feedback, jml_belum_fb, jml_sudah_fb = dashboard_counts

    try:
        progress_df = get_progress_siswa_df()
    except Exception:
        import pandas as pd
        progress_df = pd.DataFrame()

    # ---- Alert Banner ----
    if jml_belum_fb > 0:
        st.markdown(
            f"""
            <div class="alert-banner">
                ⚠️ Terdapat <strong>{jml_belum_fb} tanggapan siswa</strong> yang belum
                diberi feedback oleh guru. Segera ingatkan guru untuk memberikan feedback.
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---- Row 1: 6 Metric Cards ----
    st.markdown(
        '<div class="dashboard-section-title">📊 Ringkasan Statistik</div>',
        unsafe_allow_html=True
    )

    r1c1, r1c2, r1c3 = st.columns(3)

    with r1c1:
        st.markdown(
            f"""
            <div class="metric-card-v2 mc-blue">
                <div class="mc-icon">👥</div>
                <div class="mc-content">
                    <div class="mc-label">Total Pengguna</div>
                    <div class="mc-value">{counts.get("total", 0)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r1c2:
        st.markdown(
            f"""
            <div class="metric-card-v2 mc-green">
                <div class="mc-icon">🎓</div>
                <div class="mc-content">
                    <div class="mc-label">Siswa Terdaftar</div>
                    <div class="mc-value">{counts.get("siswa", 0)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r1c3:
        st.markdown(
            f"""
            <div class="metric-card-v2 mc-teal">
                <div class="mc-icon">👨‍🏫</div>
                <div class="mc-content">
                    <div class="mc-label">Guru</div>
                    <div class="mc-value">{counts.get("guru", 0)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    r2c1, r2c2, r2c3 = st.columns(3)

    with r2c1:
        st.markdown(
            f"""
            <div class="metric-card-v2 mc-purple">
                <div class="mc-icon">📝</div>
                <div class="mc-content">
                    <div class="mc-label">Total Tanggapan</div>
                    <div class="mc-value">{jml_tanggapan}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r2c2:
        st.markdown(
            f"""
            <div class="metric-card-v2 mc-emerald">
                <div class="mc-icon">✅</div>
                <div class="mc-content">
                    <div class="mc-label">Sudah Feedback</div>
                    <div class="mc-value">{jml_sudah_fb}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r2c3:
        st.markdown(
            f"""
            <div class="metric-card-v2 mc-amber">
                <div class="mc-icon">⏳</div>
                <div class="mc-content">
                    <div class="mc-label">Menunggu Feedback</div>
                    <div class="mc-value">{jml_belum_fb}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---- Row 2: Charts ----
    st.write("")
    st.markdown(
        '<div class="dashboard-section-title">📈 Visualisasi Data</div>',
        unsafe_allow_html=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        admin_count = int(counts.get("admin", 0))
        guru_count = int(counts.get("guru", 0))
        siswa_count = int(counts.get("siswa", 0))

        role_values = [admin_count, guru_count, siswa_count]
        role_labels = ["Admin", "Guru", "Siswa"]

        if sum(role_values) == 0:
            st.info("Belum ada data pengguna.")
        else:
            fig, ax = plt.subplots(figsize=(4.2, 4.2))
            colors_role = ["#7c3aed", "#0284c7", "#059669"]

            wedges, texts, autotexts = ax.pie(
                role_values,
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors_role,
                pctdistance=0.78,
                wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 3}
            )

            ax.text(0, 0.08, str(sum(role_values)),
                    ha="center", va="center", fontsize=26,
                    fontweight="bold", color="#0f172a")
            ax.text(0, -0.13, "Pengguna",
                    ha="center", va="center", fontsize=11, color="#64748b")

            ax.legend(wedges, role_labels, title="Role",
                      loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False)

            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
                autotext.set_fontsize(10)

            ax.set_title("Distribusi Role", fontsize=14,
                         fontweight="bold", color="#0f172a", pad=16)
            ax.axis("equal")
            st.pyplot(fig, use_container_width=False)
            plt.close(fig)

    with chart_col2:
        aktif_count = int(counts.get("aktif", 0))
        nonaktif_count = int(counts.get("nonaktif", 0))

        status_values = [aktif_count, nonaktif_count]
        status_labels = ["Aktif", "Nonaktif"]

        if sum(status_values) == 0:
            st.info("Belum ada data pengguna.")
        else:
            fig2, ax2 = plt.subplots(figsize=(4.2, 4.2))
            colors_status = ["#10b981", "#ef4444"]

            wedges2, texts2, autotexts2 = ax2.pie(
                status_values,
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors_status,
                pctdistance=0.78,
                wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 3}
            )

            ax2.text(0, 0.08, str(sum(status_values)),
                     ha="center", va="center", fontsize=26,
                     fontweight="bold", color="#0f172a")
            ax2.text(0, -0.13, "Pengguna",
                     ha="center", va="center", fontsize=11, color="#64748b")

            ax2.legend(wedges2, status_labels, title="Status",
                       loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False)

            for autotext in autotexts2:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
                autotext.set_fontsize(10)

            ax2.set_title("Status Pengguna", fontsize=14,
                          fontweight="bold", color="#0f172a", pad=16)
            ax2.axis("equal")
            st.pyplot(fig2, use_container_width=False)
            plt.close(fig2)

    # ---- Row 3: Recent Users + Progress ----
    st.write("")
    st.markdown(
        '<div class="dashboard-section-title">📋 Detail & Aktivitas</div>',
        unsafe_allow_html=True
    )

    detail_col1, detail_col2 = st.columns(2, gap="large")

    with detail_col1:
        recent_users = df_users.head(5)
        user_rows = []
        for _, u_row in recent_users.iterrows():
            r_nama = escape(str(u_row["nama"]))
            r_email = escape(str(u_row["email"]))
            r_role = str(u_row["role"]).lower()
            badge_cls = f"recent-user-badge-{r_role}"
            user_rows.append(
                f'<div class="recent-user-item">'
                f'<div class="recent-user-info">'
                f'<div class="recent-user-name">{r_nama}</div>'
                f'<div class="recent-user-email">{r_email}</div>'
                f'</div>'
                f'<span class="recent-user-badge {badge_cls}">{r_role.capitalize()}</span>'
                f'</div>'
            )
        user_rows_html = "".join(user_rows)

        if not recent_users.empty:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-card-title">👤 Pengguna Terbaru</div>
                    {user_rows_html}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="info-card">
                    <div class="info-card-title">👤 Pengguna Terbaru</div>
                    <p style="color:#94a3b8;font-size:14px;">Belum ada pengguna terdaftar.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with detail_col2:
        total_siswa = max(int(counts.get("siswa", 0)), 1)

        if not progress_df.empty:
            p_materi = int((progress_df["materi_dibaca"].astype(int) == 1).sum())
            p_simulasi = int((progress_df["simulasi_dijalankan"].astype(int) == 1).sum())
            p_tanggapan = int((progress_df["tanggapan_dikirim"].astype(int) == 1).sum())
            p_feedback = int((progress_df["feedback_diterima"].astype(int) == 1).sum())
        else:
            p_materi = p_simulasi = p_tanggapan = p_feedback = 0

        pct_materi = min(int((p_materi / total_siswa) * 100), 100)
        pct_simulasi = min(int((p_simulasi / total_siswa) * 100), 100)
        pct_tanggapan = min(int((p_tanggapan / total_siswa) * 100), 100)
        pct_feedback = min(int((p_feedback / total_siswa) * 100), 100)

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">📊 Progress Pembelajaran Siswa</div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span class="progress-text">📖 Materi Dibaca</span>
                        <span class="progress-count">{p_materi}/{total_siswa}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill pb-green" style="width:{pct_materi}%;"></div>
                    </div>
                </div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span class="progress-text">🔬 Simulasi Dijalankan</span>
                        <span class="progress-count">{p_simulasi}/{total_siswa}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill pb-blue" style="width:{pct_simulasi}%;"></div>
                    </div>
                </div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span class="progress-text">📝 Tanggapan Dikirim</span>
                        <span class="progress-count">{p_tanggapan}/{total_siswa}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill pb-purple" style="width:{pct_tanggapan}%;"></div>
                    </div>
                </div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span class="progress-text">💬 Feedback Diterima</span>
                        <span class="progress-count">{p_feedback}/{total_siswa}</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill pb-amber" style="width:{pct_feedback}%;"></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# MENU 2: INFORMASI ADMIN
# =========================
elif st.session_state["admin_menu"] == "Informasi Admin":
    st.markdown(
        '<div style="color:#0f172a !important;font-size:30px;font-weight:900;margin:8px 0 6px 0;">Informasi Admin</div>'
        '<div style="color:#64748b !important;font-size:16px;font-weight:700;margin-bottom:22px;">Data Admin</div>',
        unsafe_allow_html=True
    )

    admin_id = int(admin_data.get("id_user", current_user_id))
    admin_nama = str(admin_data.get("nama", current_name))
    admin_email = str(admin_data.get("email", current_email))
    admin_role = str(admin_data.get("role", "admin"))
    admin_status = str(admin_data.get("status", "aktif"))

    col_info, col_edit = st.columns([1.3, 1], gap="large")

    with col_info:

        st.markdown('<div class="admin-label">Nama Admin</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="admin-value">{escape(admin_nama)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="admin-label">Email</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="admin-value">{escape(admin_email)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="admin-label">Role</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="role-badge">{escape(admin_role)}</div>', unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="admin-label">Status</div>', unsafe_allow_html=True)

        if admin_status.lower() == "aktif":
            st.markdown(
                f'<div class="status-badge">{escape(admin_status)}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="status-badge-nonaktif">{escape(admin_status)}</div>',
                unsafe_allow_html=True
            )

    with col_edit:
        st.markdown(
            '<div class="admin-section-title" style="font-size:24px;">Edit Nama Admin</div>',
            unsafe_allow_html=True
        )

        nama_baru = st.text_input(
            "Nama Admin",
            value=admin_nama
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("Simpan", use_container_width=True, key="btn_simpan_admin"):
                if not nama_baru.strip():
                    st.error("Nama admin tidak boleh kosong.")
                else:
                    update_admin_name(admin_id, nama_baru)
                    st.success("Nama admin berhasil diperbarui.")
                    st.rerun()

        with col_btn2:
            if st.button("Reset", use_container_width=True, key="btn_reset_admin"):
                st.rerun()


# =========================
# MENU 3: DAFTAR PENGGUNA
# =========================
elif st.session_state["admin_menu"] == "Daftar Pengguna":
    st.markdown(
        '<div style="color:#0f172a !important;font-size:30px;font-weight:900;margin:8px 0 6px 0;">Daftar Pengguna</div>'
        '<div style="color:#64748b !important;font-size:16px;font-weight:700;margin-bottom:22px;">'
        'Kelola data akun, role, status, dan akses pengguna pada web pembelajaran ekosistem.'
        '</div>',
        unsafe_allow_html=True
    )

    if df_users.empty:
        st.info("Belum ada pengguna yang terdaftar.")

    else:
        search = st.text_input(
            "Cari pengguna",
            placeholder="Cari berdasarkan nama, email, role, atau status..."
        )

        display_df = df_users.copy()

        if search.strip():
            keyword = search.strip().lower()
            display_df = display_df[
                display_df["nama"].astype(str).str.lower().str.contains(keyword, na=False)
                | display_df["email"].astype(str).str.lower().str.contains(keyword, na=False)
                | display_df["role"].astype(str).str.lower().str.contains(keyword, na=False)
                | display_df["status"].astype(str).str.lower().str.contains(keyword, na=False)
            ]

        if display_df.empty:
            st.warning("Data pengguna tidak ditemukan.")

        else:
            # Tampilan pengguna dibuat card agar rapi di desktop dan HP
            for _, row in display_df.iterrows():
                row_id = int(row["id_user"])
                nama = escape(str(row["nama"]))
                email = escape(str(row["email"]))
                role_raw = str(row["role"]).lower()
                status_raw = str(row["status"]).lower()

                role_class = {
                    "admin": "role-admin",
                    "guru": "role-guru",
                    "siswa": "role-siswa"
                }.get(role_raw, "role-siswa")

                status_class = "status-aktif" if status_raw == "aktif" else "status-nonaktif"

                avatar_icon = {
                    "admin": "🛠️",
                    "guru": "👨‍🏫",
                    "siswa": "🎓"
                }.get(role_raw, "👤")

                with st.container(key=f"user_card_{row_id}"):
                    card_html = (
                        '<div class="user-card-grid">'
                        '<div class="user-main-info">'
                        f'<div class="user-avatar">{avatar_icon}</div>'
                        '<div>'
                        '<div class="user-field-label">Pengguna</div>'
                        f'<div class="user-name">{nama}</div>'
                        f'<div class="user-email">{email}</div>'
                        '</div>'
                        '</div>'
                        '<div>'
                        '<div class="user-field-label">Role</div>'
                        f'<span class="user-role-badge {role_class}">{role_raw.capitalize()}</span>'
                        '</div>'
                        '<div>'
                        '<div class="user-field-label">Status</div>'
                        f'<span class="user-status-badge {status_class}">{status_raw.capitalize()}</span>'
                        '</div>'
                        '</div>'
                    )
                
                    st.markdown(card_html, unsafe_allow_html=True)

                    col_edit, col_empty = st.columns([1, 3])

                    with col_edit:
                        if st.button("Edit", key=f"btn_edit_user_{row_id}", use_container_width=True):
                            st.session_state["selected_edit_user_id"] = row_id
                            st.rerun()

        st.divider()

        if "selected_edit_user_id" in st.session_state:
            selected_id = int(st.session_state["selected_edit_user_id"])
            selected_rows = df_users[df_users["id_user"].astype(int) == selected_id]

            if not selected_rows.empty:
                selected_user = selected_rows.iloc[0]

                st.markdown(
                    '<div class="admin-section-title" style="font-size:24px;margin-top:24px;">Edit Pengguna</div>',
                    unsafe_allow_html=True
                )

                with st.form("form_edit_pengguna"):
                    nama_baru = st.text_input(
                        "Nama",
                        value=str(selected_user["nama"])
                    )

                    st.text_input(
                        "Email",
                        value=str(selected_user["email"]),
                        disabled=True
                    )

                    role_options = ["admin", "guru", "siswa"]
                    role_lama = str(selected_user["role"]).lower()

                    role_baru = st.selectbox(
                        "Role",
                        role_options,
                        index=role_options.index(role_lama) if role_lama in role_options else 0
                    )

                    status_options = ["aktif", "nonaktif"]
                    status_lama = str(selected_user["status"]).lower()

                    status_baru = st.selectbox(
                        "Status",
                        status_options,
                        index=status_options.index(status_lama) if status_lama in status_options else 0
                    )

                    col_simpan, col_batal = st.columns(2)

                    with col_simpan:
                        simpan = st.form_submit_button("Simpan Perubahan", use_container_width=True)

                    with col_batal:
                        batal = st.form_submit_button("Batal", use_container_width=True)

                    if simpan:
                        if not nama_baru.strip():
                            st.error("Nama pengguna tidak boleh kosong.")

                        elif int(selected_user["id_user"]) == current_user_id and status_baru == "nonaktif":
                            st.error("Akun admin yang sedang digunakan tidak boleh dinonaktifkan.")

                        elif int(selected_user["id_user"]) == current_user_id and role_baru != "admin":
                            st.error("Role akun admin yang sedang digunakan tidak boleh diubah.")

                        else:
                            update_user_data(
                                int(selected_user["id_user"]),
                                nama_baru,
                                role_baru,
                                status_baru
                            )

                            st.success("Data pengguna berhasil diperbarui.")
                            del st.session_state["selected_edit_user_id"]
                            st.rerun()

                    if batal:
                        del st.session_state["selected_edit_user_id"]
                        st.rerun()
