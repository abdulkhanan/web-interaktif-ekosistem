import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

from database.queries import get_or_create_google_user


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_SCOPE = "openid email profile"


def init_auth():
    from urllib.parse import unquote

    default_state = {
        "logged_in": False,
        "logout_triggered": False,
        "id_user": None,
        "nama_pengguna": "",
        "email": "",
        "role": None,
        "kelas": "",
    }

    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # 1. Restore auth state from read-only cookies (immediately available on refresh/load)
    if not st.session_state["logged_in"] and not st.session_state.get("logout_triggered"):
        try:
            cookies = st.context.cookies
            if cookies.get("logged_in") == "true":
                st.session_state["logged_in"] = True
                
                raw_id = cookies.get("id_user")
                try:
                    st.session_state["id_user"] = int(raw_id) if raw_id is not None else None
                except ValueError:
                    st.session_state["id_user"] = raw_id
                    
                st.session_state["nama_pengguna"] = unquote(cookies.get("nama_pengguna") or "")
                st.session_state["email"] = unquote(cookies.get("email") or "")
                st.session_state["role"] = cookies.get("role")
                st.session_state["kelas"] = unquote(cookies.get("kelas") or "")
        except Exception:
            pass

    # 2. Write auth state to cookies using CookieController if not already written
    if st.session_state["logged_in"]:
        try:
            cookies = st.context.cookies
            if cookies.get("logged_in") != "true" or unquote(cookies.get("email") or "") != st.session_state["email"]:
                from streamlit_cookies_controller import CookieController
                with st.container(key="hidden_cookies"):
                    controller = CookieController()
                    controller.set("logged_in", "true")
                    controller.set("id_user", str(st.session_state["id_user"]))
                    controller.set("nama_pengguna", st.session_state["nama_pengguna"])
                    controller.set("email", st.session_state["email"])
                    controller.set("role", st.session_state["role"])
                    controller.set("kelas", st.session_state["kelas"])
        except Exception:
            pass


def get_google_config():
    try:
        config = st.secrets["google_oauth"]

        return {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "redirect_uri": config["redirect_uri"],
            "default_admin_email": config.get("default_admin_email", ""),
        }

    except Exception:
        st.error(
            "Konfigurasi Google OAuth belum tersedia. "
            "Isi file .streamlit/secrets.toml terlebih dahulu."
        )
        st.stop()


def make_google_client():
    config = get_google_config()

    return OAuth2Session(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        scope=GOOGLE_SCOPE,
        redirect_uri=config["redirect_uri"],
        token_endpoint_auth_method="client_secret_post",
    )


def get_query_param(name):
    value = st.query_params.get(name)

    if isinstance(value, list):
        return value[0] if value else None

    return value


def make_google_login_url():
    client = make_google_client()

    authorization_url, _ = client.create_authorization_url(
        GOOGLE_AUTH_URL,
        prompt="select_account",
        access_type="online",
    )

    return authorization_url


def handle_google_callback():
    init_auth()

    code = get_query_param("code")

    if not code:
        return

    config = get_google_config()
    client = make_google_client()

    try:
        client.fetch_token(
            GOOGLE_TOKEN_URL,
            code=code,
        )

        response = client.get(GOOGLE_USERINFO_URL)
        profile = response.json()

        user = get_or_create_google_user(
            profile=profile,
            default_admin_email=config["default_admin_email"]
        )

        if user["status"] != "aktif":
            from components.ui import render_inactive_screen
            render_inactive_screen(
                message="Akun Google Anda berhasil dikenali oleh sistem, tetapi saat ini status akun Anda belum aktif. Silakan hubungi admin agar akun diaktifkan.",
                email=user["email"]
            )
            st.query_params.clear()
            st.stop()

        st.session_state["logged_in"] = True
        st.session_state["logout_triggered"] = False
        st.session_state["id_user"] = user["id_user"]
        st.session_state["nama_pengguna"] = user["nama"]
        st.session_state["email"] = user["email"]
        st.session_state["role"] = user["role"]
        st.session_state["kelas"] = user.get("kelas", "")

        st.query_params.clear()
        st.rerun()

    except Exception as error:
        st.error(f"Login Google gagal: {error}")
        st.query_params.clear()


def logout():
    st.session_state["logged_in"] = False
    st.session_state["logout_triggered"] = True
    st.session_state["id_user"] = None
    st.session_state["nama_pengguna"] = ""
    st.session_state["email"] = ""
    st.session_state["role"] = None
    st.session_state["kelas"] = ""

    if "hasil_simulasi" in st.session_state:
        del st.session_state["hasil_simulasi"]

    if "simulasi_dijalankan" in st.session_state:
        del st.session_state["simulasi_dijalankan"]

    # Clear cookies using CookieController
    try:
        from streamlit_cookies_controller import CookieController
        with st.container(key="hidden_cookies_logout"):
            controller = CookieController()
            controller.remove("logged_in")
            controller.remove("id_user")
            controller.remove("nama_pengguna")
            controller.remove("email")
            controller.remove("role")
            controller.remove("kelas")
    except Exception:
        pass

    st.query_params.clear()

    try:
        st.switch_page("app.py")
    except Exception:
        st.rerun()


def require_role(allowed_roles):
    init_auth()

    if not st.session_state.get("logged_in"):
        from components.ui import render_auth_warning
        render_auth_warning(
            title="Akses Dibatasi",
            message="Silakan login terlebih dahulu menggunakan akun Google untuk mengakses fitur pembelajaran.",
            icon="🔐",
            button_label="Masuk dengan Google",
            target_page="app.py"
        )
        st.stop()

    if st.session_state.get("role") not in allowed_roles:
        from components.ui import render_auth_warning
        role_map = {"admin": "Administrator", "guru": "Guru", "siswa": "Siswa"}
        allowed_labels = [role_map.get(r, r) for r in allowed_roles]
        render_auth_warning(
            title="Akses Ditolak",
            message=f"Halaman ini hanya dapat diakses oleh peran: {', '.join(allowed_labels)}.",
            icon="🚫",
            button_label="Kembali ke Dashboard",
            target_page="app.py"
        )
        st.stop()
