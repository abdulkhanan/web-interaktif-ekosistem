import streamlit as st
import json
from datetime import datetime
from database.init_db import init_db
from database.queries import insert_tanggapan, update_progress, is_progress_done
from modules.auth import require_role
from components.ui import (
    role_navigation,
    load_css,
    page_title,
    section_title,
    info_card,
    generic_simulation_result_view,
    get_guided_questions
)

init_db()

st.set_page_config(
    page_title="Uji Hipotesis",
    page_icon="📝",
    layout="wide"
)

load_css()
require_role(["siswa"])
role_navigation()

nama_siswa = st.session_state.get("nama_pengguna", "")

page_title(
    "📝 Uji Hipotesis dan Kesimpulan",
    "Gunakan data simulasi dan materi pendukung untuk menguji hipotesis, menyusun kesimpulan, dan menentukan tindakan nyata."
)

materi_sudah = is_progress_done(nama_siswa, "materi_dibaca")
simulasi_sudah = is_progress_done(nama_siswa, "simulasi_dijalankan")



simulasi_sudah = is_progress_done(nama_siswa, "simulasi_dijalankan")
hasil = st.session_state.get("hasil_simulasi")

if not simulasi_sudah or hasil is None:
    info_card(
        "Data Simulasi Belum Tersedia",
        """
        Kamu harus merumuskan masalah, menyusun hipotesis, menjalankan simulasi, dan menyimpan data terlebih dahulu.
        Silakan kembali ke halaman Simulasi Ekosistem, lalu klik tombol Simpan Data untuk Uji Hipotesis.
        """,
        "danger-card"
    )

    if st.button("⬅️ Kembali ke Simulasi Ekosistem"):
        st.switch_page("pages/3_Simulasi_Ekosistem.py")

    st.stop()
    
jenis_simulasi = hasil["jenis_simulasi"]

section_title("Identitas Siswa")

info_card(
    "Nama Siswa",
    nama_siswa,
    "green-card"
)

section_title("Ringkasan Rencana Investigasi dan Data Simulasi")

row_preview = {
    "jenis_simulasi": hasil["jenis_simulasi"],
    "input_simulasi": json.dumps(hasil["input_simulasi"], ensure_ascii=False),
    "hasil_simulasi": json.dumps(hasil["hasil_simulasi"], ensure_ascii=False)
}

generic_simulation_result_view(row_preview)

info_card(
    "Tahap Akhir Penyelidikan",
    """
    Bandingkan hipotesis awal dengan data simulasi. Jika perlu, buka kembali materi ekosistem
    sebagai bahan konsep untuk memperkuat alasan ilmiah sebelum menulis kesimpulan.
    """,
    "yellow-card"
)

if st.button("📘 Buka Materi Pendukung", key="materi_dari_tanggapan"):
    st.switch_page("pages/2_Materi_Ekosistem.py")

section_title("Uji Hipotesis, Kesimpulan, dan Tindakan Nyata")

questions = get_guided_questions(jenis_simulasi)

form_key = f"form_tanggapan_{jenis_simulasi.replace(' ', '_').replace(':', '').replace('/', '_')}"

with st.form(key=form_key):
    jawaban_1 = st.text_area(
        questions["q1"],
        key=f"jawaban_1_{form_key}"
    )

    jawaban_2 = st.text_area(
        questions["q2"],
        key=f"jawaban_2_{form_key}"
    )

    jawaban_3 = st.text_area(
        questions["q3"],
        key=f"jawaban_3_{form_key}"
    )

    kesimpulan = st.text_area(
        questions["q4"],
        key=f"kesimpulan_{form_key}"
    )

    submit = st.form_submit_button("Kirim Hasil Penyelidikan")

    if submit:
        if not jawaban_1 or not jawaban_2 or not jawaban_3 or not kesimpulan:
            st.error("Semua kolom jawaban harus diisi.")
        else:
            data = {
                "id_tanggapan": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nama": nama_siswa,
                "jenis_simulasi": jenis_simulasi,
                "input_simulasi": json.dumps(hasil["input_simulasi"], ensure_ascii=False),
                "hasil_simulasi": json.dumps(hasil["hasil_simulasi"], ensure_ascii=False),
                "jawaban_1": jawaban_1,
                "jawaban_2": jawaban_2,
                "jawaban_3": jawaban_3,
                "kesimpulan": kesimpulan
            }

            insert_tanggapan(data)
            update_progress(nama_siswa, "tanggapan_dikirim")

            info_card(
                "Tanggapan Berhasil Dikirim",
                """
                Hasil penyelidikan kamu sudah tersimpan. Jawaban ini memuat uji hipotesis,
                kesimpulan ilmiah, dan tindakan nyata. Silakan menunggu feedback dari guru.
                """,
                "green-card"
            )