import pandas as pd
from datetime import datetime
from database.connection import get_supabase_client


VALID_ROLES = ["admin", "guru", "siswa"]
VALID_STATUS = ["aktif", "nonaktif"]
PROGRESS_COLUMNS = [
    "materi_dibaca",
    "simulasi_dijalankan",
    "tanggapan_dikirim",
    "feedback_diterima",
]


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def client():
    return get_supabase_client()


def _data(response):
    return response.data or []


def _df(rows, columns=None):
    if rows:
        return pd.DataFrame(rows)
    return pd.DataFrame(columns=columns or [])


def _first(rows):
    return rows[0] if rows else None


def _normalize_email(email):
    return (email or "").strip().lower()


def _normalize_text(value):
    return (value or "").strip()


# =====================================================
# AUTH DAN USER MANAGEMENT
# =====================================================

def get_user_by_email(email):
    email = _normalize_email(email)
    if not email:
        return None

    response = (
        client()
        .table("users")
        .select("id_user,nama,email,google_sub,role,kelas,status,created_at,updated_at")
        .eq("email", email)
        .limit(1)
        .execute()
    )
    return _first(_data(response))


def get_or_create_google_user(profile, default_admin_email=""):
    email = _normalize_email(profile.get("email", ""))
    nama = _normalize_text(profile.get("name", ""))
    google_sub = _normalize_text(profile.get("sub", ""))
    email_verified = profile.get("email_verified", False)

    if not email:
        raise ValueError("Email Google tidak ditemukan.")

    if not email_verified:
        raise ValueError("Email Google belum terverifikasi.")

    if not nama:
        nama = email.split("@")[0]

    default_admin_email = _normalize_email(default_admin_email)
    user = get_user_by_email(email)

    if user is not None:
        client().table("users").update({
            "nama": nama,
            "google_sub": google_sub or None,
            "updated_at": now(),
        }).eq("id_user", user["id_user"]).execute()
        return get_user_by_email(email)

    role = "admin" if email == default_admin_email else "siswa"
    status = "aktif" if role == "admin" else "nonaktif"

    payload = {
        "nama": nama,
        "email": email,
        "google_sub": google_sub or None,
        "role": role,
        "kelas": "",
        "status": status,
        "created_at": now(),
        "updated_at": now(),
    }
    client().table("users").insert(payload).execute()
    return get_user_by_email(email)


def create_user_manual(nama, email, role, kelas="", status="aktif"):
    nama = _normalize_text(nama)
    email = _normalize_email(email)
    kelas = _normalize_text(kelas)
    role = _normalize_text(role).lower()
    status = _normalize_text(status).lower()

    if not nama:
        raise ValueError("Nama tidak boleh kosong.")
    if not email:
        raise ValueError("Email tidak boleh kosong.")
    if role not in VALID_ROLES:
        raise ValueError("Role tidak valid.")
    if status not in VALID_STATUS:
        raise ValueError("Status tidak valid.")

    payload = {
        "nama": nama,
        "email": email,
        "google_sub": None,
        "role": role,
        "kelas": kelas,
        "status": status,
        "created_at": now(),
        "updated_at": now(),
    }
    client().table("users").insert(payload).execute()


def get_users_df():
    response = (
        client()
        .table("users")
        .select("id_user,nama,email,role,kelas,status,created_at,updated_at")
        .order("created_at", desc=True)
        .execute()
    )
    return _df(_data(response), ["id_user", "nama", "email", "role", "kelas", "status", "created_at", "updated_at"])


def update_user_role_status(id_user, role, status, kelas=""):
    role = _normalize_text(role).lower()
    status = _normalize_text(status).lower()
    kelas = _normalize_text(kelas)

    if role not in VALID_ROLES:
        raise ValueError("Role tidak valid.")
    if status not in VALID_STATUS:
        raise ValueError("Status tidak valid.")

    client().table("users").update({
        "role": role,
        "status": status,
        "kelas": kelas,
        "updated_at": now(),
    }).eq("id_user", int(id_user)).execute()


def update_user_name(id_user, nama_baru):
    nama_baru = _normalize_text(nama_baru)
    if not nama_baru:
        raise ValueError("Nama tidak boleh kosong.")

    client().table("users").update({
        "nama": nama_baru,
        "updated_at": now(),
    }).eq("id_user", int(id_user)).execute()


def update_user_data(id_user, nama_baru, role_baru, status_baru, kelas=""):
    nama_baru = _normalize_text(nama_baru)
    role_baru = _normalize_text(role_baru).lower()
    status_baru = _normalize_text(status_baru).lower()
    kelas = _normalize_text(kelas)

    if not nama_baru:
        raise ValueError("Nama tidak boleh kosong.")
    if role_baru not in VALID_ROLES:
        raise ValueError("Role tidak valid.")
    if status_baru not in VALID_STATUS:
        raise ValueError("Status tidak valid.")

    client().table("users").update({
        "nama": nama_baru,
        "role": role_baru,
        "status": status_baru,
        "kelas": kelas,
        "updated_at": now(),
    }).eq("id_user", int(id_user)).execute()


def get_user_counts():
    df = get_users_df()
    if df.empty:
        return {"total": 0, "admin": 0, "guru": 0, "siswa": 0, "aktif": 0, "nonaktif": 0}

    role_series = df["role"].astype(str).str.lower()
    status_series = df["status"].astype(str).str.lower()

    return {
        "total": int(len(df)),
        "admin": int((role_series == "admin").sum()),
        "guru": int((role_series == "guru").sum()),
        "siswa": int((role_series == "siswa").sum()),
        "aktif": int((status_series == "aktif").sum()),
        "nonaktif": int((status_series == "nonaktif").sum()),
    }


# =====================================================
# TANGGAPAN SISWA
# =====================================================

def insert_tanggapan(data):
    payload = dict(data)
    client().table("tanggapan_siswa").insert(payload).execute()


def get_tanggapan_df():
    response = client().table("tanggapan_siswa").select("*").order("waktu", desc=True).execute()
    return _df(_data(response), [
        "id_tanggapan", "waktu", "nama", "jenis_simulasi", "input_simulasi",
        "hasil_simulasi", "jawaban_1", "jawaban_2", "jawaban_3", "kesimpulan"
    ])


def get_tanggapan_by_nama_df(nama):
    nama = _normalize_text(nama)
    df = get_tanggapan_df()
    if df.empty or not nama:
        return df.iloc[0:0].copy()

    mask = df["nama"].astype(str).str.lower() == nama.lower()
    return df[mask].sort_values("waktu", ascending=False).reset_index(drop=True)


def get_tanggapan_status_df():
    tanggapan = get_tanggapan_df()
    if tanggapan.empty:
        tanggapan["jumlah_feedback"] = []
        tanggapan["status_feedback"] = []
        return tanggapan

    feedback = get_feedback_df()
    if feedback.empty:
        tanggapan["jumlah_feedback"] = 0
    else:
        counts = feedback.groupby("id_tanggapan")["id_feedback"].nunique()
        tanggapan["jumlah_feedback"] = tanggapan["id_tanggapan"].map(counts).fillna(0).astype(int)

    tanggapan["status_feedback"] = tanggapan["jumlah_feedback"].apply(
        lambda x: "Sudah diberi feedback" if int(x) > 0 else "Belum diberi feedback"
    )
    return tanggapan.sort_values("waktu", ascending=False).reset_index(drop=True)


# =====================================================
# FEEDBACK GURU
# =====================================================

def insert_feedback(data):
    payload = dict(data)
    client().table("feedback_guru").insert(payload).execute()


def get_feedback_df():
    response = client().table("feedback_guru").select("*").order("waktu_feedback", desc=True).execute()
    return _df(_data(response), [
        "id_feedback", "id_tanggapan", "waktu_feedback", "nama_siswa", "nama_guru", "isi_feedback"
    ])


def get_feedback_by_nama_df(nama):
    nama = _normalize_text(nama)
    df = get_feedback_df()
    if df.empty or not nama:
        return df.iloc[0:0].copy()

    mask = df["nama_siswa"].astype(str).str.lower() == nama.lower()
    return df[mask].sort_values("waktu_feedback", ascending=False).reset_index(drop=True)


# =====================================================
# DASHBOARD DAN PROGRESS
# =====================================================

def get_dashboard_counts_with_status():
    tanggapan = get_tanggapan_df()
    feedback = get_feedback_df()

    jumlah_siswa = int(tanggapan["nama"].nunique()) if not tanggapan.empty else 0
    jumlah_tanggapan = int(len(tanggapan))
    jumlah_feedback = int(len(feedback))

    if tanggapan.empty:
        jumlah_belum_feedback = 0
        jumlah_sudah_feedback = 0
    elif feedback.empty:
        jumlah_belum_feedback = jumlah_tanggapan
        jumlah_sudah_feedback = 0
    else:
        tanggapan_ids = set(tanggapan["id_tanggapan"].astype(str))
        feedback_ids = set(feedback["id_tanggapan"].astype(str))
        jumlah_sudah_feedback = len(tanggapan_ids & feedback_ids)
        jumlah_belum_feedback = jumlah_tanggapan - jumlah_sudah_feedback

    return (
        jumlah_siswa,
        jumlah_tanggapan,
        jumlah_feedback,
        jumlah_belum_feedback,
        jumlah_sudah_feedback,
    )


def _ensure_progress_row(nama, waktu=None):
    nama = _normalize_text(nama)
    waktu = waktu or now()
    if not nama:
        raise ValueError("Nama tidak boleh kosong.")

    existing = get_progress_by_nama(nama)
    if existing.empty:
        client().table("progress_siswa").insert({
            "nama": nama,
            "materi_dibaca": 0,
            "simulasi_dijalankan": 0,
            "tanggapan_dikirim": 0,
            "feedback_diterima": 0,
            "updated_at": waktu,
        }).execute()


def update_progress(nama, kolom):
    nama = _normalize_text(nama)
    if kolom not in PROGRESS_COLUMNS:
        raise ValueError("Kolom progress tidak valid.")

    waktu = now()
    _ensure_progress_row(nama, waktu)

    client().table("progress_siswa").update({
        kolom: 1,
        "updated_at": waktu,
    }).eq("nama", nama).execute()


def get_progress_by_nama(nama):
    nama = _normalize_text(nama)
    if not nama:
        return _df([], ["id_progress", "nama", *PROGRESS_COLUMNS, "updated_at"])

    response = client().table("progress_siswa").select("*").eq("nama", nama).limit(1).execute()
    return _df(_data(response), ["id_progress", "nama", *PROGRESS_COLUMNS, "updated_at"])


def get_progress_siswa_df():
    response = client().table("progress_siswa").select("*").order("updated_at", desc=True).execute()
    progress = _df(_data(response), ["id_progress", "nama", *PROGRESS_COLUMNS, "updated_at"])

    if progress.empty:
        progress["jumlah_tanggapan"] = []
        progress["jumlah_feedback"] = []
        return progress

    tanggapan = get_tanggapan_df()
    feedback = get_feedback_df()

    if tanggapan.empty:
        progress["jumlah_tanggapan"] = 0
    else:
        tanggapan_counts = tanggapan.groupby(tanggapan["nama"].astype(str).str.lower())["id_tanggapan"].nunique()
        progress["jumlah_tanggapan"] = progress["nama"].astype(str).str.lower().map(tanggapan_counts).fillna(0).astype(int)

    if feedback.empty:
        progress["jumlah_feedback"] = 0
    else:
        feedback_counts = feedback.groupby(feedback["nama_siswa"].astype(str).str.lower())["id_feedback"].nunique()
        progress["jumlah_feedback"] = progress["nama"].astype(str).str.lower().map(feedback_counts).fillna(0).astype(int)

    return progress.sort_values("updated_at", ascending=False).reset_index(drop=True)


def is_progress_done(nama, kolom):
    df = get_progress_by_nama(nama)
    if df.empty or kolom not in df.columns:
        return False
    return int(df.iloc[0][kolom] or 0) == 1


# =====================================================
# PROGRESS MATERI
# =====================================================

def mark_materi_selesai(nama, kode_materi, judul_materi):
    nama = _normalize_text(nama)
    kode_materi = _normalize_text(kode_materi)
    judul_materi = _normalize_text(judul_materi)
    waktu = now()

    _ensure_progress_row(nama, waktu)

    response = (
        client()
        .table("progress_materi")
        .select("id_progress_materi")
        .eq("nama", nama)
        .eq("kode_materi", kode_materi)
        .limit(1)
        .execute()
    )
    existing = _first(_data(response))

    payload = {
        "nama": nama,
        "kode_materi": kode_materi,
        "judul_materi": judul_materi,
        "status_selesai": 1,
        "updated_at": waktu,
    }

    if existing:
        client().table("progress_materi").update(payload).eq(
            "id_progress_materi", existing["id_progress_materi"]
        ).execute()
    else:
        client().table("progress_materi").insert(payload).execute()

    client().table("progress_siswa").update({
        "materi_dibaca": 1,
        "updated_at": waktu,
    }).eq("nama", nama).execute()


def is_materi_done(nama, kode_materi):
    nama = _normalize_text(nama)
    kode_materi = _normalize_text(kode_materi)
    if not nama or not kode_materi:
        return False

    response = (
        client()
        .table("progress_materi")
        .select("id_progress_materi")
        .eq("nama", nama)
        .eq("kode_materi", kode_materi)
        .eq("status_selesai", 1)
        .limit(1)
        .execute()
    )
    return bool(_data(response))


def get_materi_selesai_codes(nama):
    nama = _normalize_text(nama)
    if not nama:
        return []

    response = (
        client()
        .table("progress_materi")
        .select("kode_materi")
        .eq("nama", nama)
        .eq("status_selesai", 1)
        .execute()
    )
    return [row["kode_materi"] for row in _data(response)]


def get_progress_materi_by_nama_df(nama):
    nama = _normalize_text(nama)
    if not nama:
        return _df([], ["id_progress_materi", "nama", "kode_materi", "judul_materi", "status_selesai", "updated_at"])

    response = (
        client()
        .table("progress_materi")
        .select("*")
        .eq("nama", nama)
        .order("updated_at", desc=True)
        .execute()
    )
    return _df(_data(response), ["id_progress_materi", "nama", "kode_materi", "judul_materi", "status_selesai", "updated_at"])
