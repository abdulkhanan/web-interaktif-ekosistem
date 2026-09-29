import streamlit as st
from authlib.integrations.requests_client import OAuth2Session

from database.queries import get_or_create_google_user, get_user_by_email

# Kompatibilitas dengan database/queries.py versi lama pada deployment.
try:
    from database.queries import get_user_by_id
except ImportError:
    from database.connection import get_supabase_client

    def get_user_by_id(id_user):
        if id_user is None:
            return None
        try:
            id_user = int(id_user)
        except (TypeError, ValueError):
            return None

        db = get_supabase_client()
        fields_with_password = (
            "id_user,nama,email,google_sub,role,kelas,status,"
            "password_hash,created_at,updated_at"
        )
        fields_without_password = (
            "id_user,nama,email,google_sub,role,kelas,status,created_at,updated_at"
        )
        try:
            response = (
                db.table("users")
                .select(fields_with_password)
                .eq("id_user", id_user)
                .limit(1)
                .execute()
            )
        except Exception:
            response = (
                db.table("users")
                .select(fields_without_password)
                .eq("id_user", id_user)
                .limit(1)
                .execute()
            )

        rows = response.data or []
        return rows[0] if rows else None

from modules.security import verify_password


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_SCOPE = "openid email profile"


def _clear_local_auth_state(remove_cookies=True):
    """Kosongkan sesi lokal tanpa memaksa navigasi halaman."""
    st.session_state["logged_in"] = False
    st.session_state["logout_triggered"] = True
    st.session_state["id_user"] = None
    st.session_state["nama_pengguna"] = ""
    st.session_state["email"] = ""
    st.session_state["role"] = None
    st.session_state["kelas"] = ""

    if remove_cookies:
        try:
            from streamlit_cookies_controller import CookieController
            with st.container(key="hidden_cookies_invalid"):
                controller = CookieController()
                for cookie_name in ["logged_in", "id_user", "nama_pengguna", "email", "role", "kelas"]:
                    controller.remove(cookie_name)
        except Exception:
            pass


def _refresh_and_validate_logged_in_user():
    """Sinkronkan sesi dengan database dan cabut akses akun yang dihapus/nonaktif."""
    if not st.session_state.get("logged_in"):
        return

    try:
        user = get_user_by_id(st.session_state.get("id_user"))
        if user is None and st.session_state.get("email"):
            user = get_user_by_email(st.session_state.get("email"))
    except Exception:
        # Jika database sedang tidak dapat dijangkau, jangan otomatis mengeluarkan pengguna.
        return

    if user is None or str(user.get("status", "")).lower() != "aktif":
        _clear_local_auth_state(remove_cookies=True)
        return

    # Perubahan nama/role/kelas dari admin langsung tersinkron pada interaksi berikutnya.
    st.session_state["id_user"] = user.get("id_user")
    st.session_state["nama_pengguna"] = user.get("nama", "") or ""
    st.session_state["email"] = user.get("email", "") or ""
    st.session_state["role"] = user.get("role")
    st.session_state["kelas"] = user.get("kelas", "") or ""


def init_auth():
    from urllib.parse import unquote

    st.markdown(
        """
        <style>
            /* Sembunyikan loading skeleton dari komponen cookie */
            .st-key-hidden_cookies,
            .st-key-hidden_cookies_logout,
            .st-key-hidden_cookies_invalid,
            .st-key-hidden_cookies *,
            .st-key-hidden_cookies_logout *,
            .st-key-hidden_cookies_invalid *,
            div[data-testid="stSkeleton"],
            [data-testid="stSkeleton"],
            .stSkeleton,
            .element-container:has(iframe[height="0"]),
            .element-container:has(iframe[height="0px"]),
            iframe[height="0"],
            iframe[height="0px"] {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                min-height: 0 !important;
                max-height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                overflow: hidden !important;
                pointer-events: none !important;
            }

            header[data-testid="stHeader"],
            div[data-testid="stToolbar"],
            div[data-testid="stDecoration"],
            div[data-testid="stStatusWidget"],
            #MainMenu,
            footer {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
            }

            .block-container {
                padding-top: 0rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

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

    # 2. Validasi ulang ke database. Jika akun sudah dihapus/nonaktif oleh admin,
    #    sesi pengguna langsung dicabut pada interaksi/navigasi berikutnya.
    _refresh_and_validate_logged_in_user()

    # 3. Write auth state to cookies using CookieController if not already written
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


def set_login_session(user):
    st.session_state["logged_in"] = True
    st.session_state["logout_triggered"] = False
    st.session_state["id_user"] = user["id_user"]
    st.session_state["nama_pengguna"] = user["nama"]
    st.session_state["email"] = user["email"]
    st.session_state["role"] = user["role"]
    st.session_state["kelas"] = user.get("kelas", "") or ""


def login_with_email_password(email, password):
    email = (email or "").strip().lower()
    password = password or ""

    if not email or not password:
        return False, "Email dan password wajib diisi."

    user = get_user_by_email(email)

    if user is None:
        return False, "Email atau password salah."

    if str(user.get("status", "")).lower() != "aktif":
        return False, "Akun ditemukan, tetapi statusnya belum aktif. Silakan hubungi admin/guru."

    password_hash = user.get("password_hash")
    if not password_hash:
        return False, "Akun ini belum memiliki password. Admin dapat menambahkan password pada menu Daftar Pengguna."

    if not verify_password(password, password_hash):
        return False, "Email atau password salah."

    set_login_session(user)
    return True, "Login berhasil."


def is_google_login_available():
    try:
        config = st.secrets["google_oauth"]
        required_keys = ["client_id", "client_secret", "redirect_uri"]
        return all(str(config.get(key, "")).strip() for key in required_keys)
    except Exception:
        return False


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

        set_login_session(user)

        st.query_params.clear()
        st.rerun()

    except Exception as error:
        st.error(f"Login Google gagal: {error}")
        st.query_params.clear()


def logout():
    _clear_local_auth_state(remove_cookies=False)

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
            message="Silakan login terlebih dahulu menggunakan email dan password, atau akun Google jika tersedia, untuk mengakses fitur pembelajaran.",
            icon="🔐",
            button_label="Masuk",
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
