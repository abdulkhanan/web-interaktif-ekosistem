"""
Opsional: migrasi isi data/ekosistem.db lama ke Supabase.
Jalankan lokal setelah mengisi .streamlit/secrets.toml.

Perintah:
    python scripts/migrate_sqlite_to_supabase.py
"""
from pathlib import Path
import sqlite3
import tomllib
from supabase import create_client

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "ekosistem.db"
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"

TABLES = [
    "users",
    "tanggapan_siswa",
    "feedback_guru",
    "progress_siswa",
    "progress_materi",
]


def rows_from_sqlite(table_name):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database SQLite tidak ditemukan: {DB_PATH}")
    if not SECRETS_PATH.exists():
        raise FileNotFoundError(f"secrets.toml tidak ditemukan: {SECRETS_PATH}")

    secrets = tomllib.loads(SECRETS_PATH.read_text(encoding="utf-8"))
    supabase = create_client(secrets["supabase"]["url"], secrets["supabase"]["key"])

    for table in TABLES:
        rows = rows_from_sqlite(table)
        if not rows:
            print(f"{table}: tidak ada data")
            continue

        # Supabase/PostgREST lebih aman menerima batch kecil.
        for start in range(0, len(rows), 100):
            batch = rows[start:start + 100]
            supabase.table(table).upsert(batch).execute()

        print(f"{table}: {len(rows)} baris berhasil dikirim")


if __name__ == "__main__":
    main()
