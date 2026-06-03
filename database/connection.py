import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """Membuat koneksi Supabase dari Streamlit secrets.

    Isi secrets di Streamlit Community Cloud:

    [supabase]
    url = "https://PROJECT_ID.supabase.co"
    key = "sb_secret_xxx_atau_service_role_key"
    """
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
    except Exception as exc:
        st.error(
            "Konfigurasi Supabase belum tersedia. "
            "Isi [supabase].url dan [supabase].key pada Secrets Streamlit Cloud."
        )
        st.stop()

    return create_client(url, key)


def get_connection():
    """Alias lama agar struktur aplikasi tetap kompatibel."""
    return get_supabase_client()
