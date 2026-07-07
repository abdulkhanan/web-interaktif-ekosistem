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
    page_title="Tanggapan Siswa",
    page_icon="📝",
    layout="wide"
)

load_css()
require_role(["siswa"])
role_navigation()

nama_siswa = st.session_state.get("nama_pengguna", "")

page_title(
    "📝 Tanggapan Siswa",
    "Tulis jawaban dengan alur sederhana: pertanyaan penyelidikan, dugaan, bukti data, dan kesimpulan."
)

materi_sudah = is_progress_done(nama_siswa, "materi_dibaca")
simulasi_sudah = is_progress_done(nama_siswa, "simulasi_dijalankan")



simulasi_sudah = is_progress_done(nama_siswa, "simulasi_dijalankan")
hasil = st.session_state.get("hasil_simulasi")

if not simulasi_sudah or hasil is None:
    info_card(
        "Data Simulasi Belum Tersedia",
        """
        Kamu harus menjalankan dan memilih salah satu simulasi terlebih dahulu sebelum menulis tanggapan.
        Silakan kembali ke halaman Simulasi Ekosistem, lalu klik tombol **Pilih Hasil Ini untuk Menjawab** pada salah satu simulasi.
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

section_title("Ringkasan Simulasi")

row_preview = {
    "jenis_simulasi": hasil["jenis_simulasi"],
    "input_simulasi": json.dumps(hasil["input_simulasi"], ensure_ascii=False),
    "hasil_simulasi": json.dumps(hasil["hasil_simulasi"], ensure_ascii=False)
}

generic_simulation_result_view(row_preview)





section_title("Pertanyaan Tanggapan")

info_card(
    "Petunjuk Mengisi Jawaban",
    """
    Gunakan bahasa sendiri. Tidak perlu panjang, yang penting jawaban menunjukkan hubungan sebab-akibat.
    Ikuti pola: **apa yang ditanyakan → apa dugaanmu → data apa buktinya → apa kesimpulannya**.
    """,
    "blue-card"
)

questions = get_guided_questions(jenis_simulasi)

form_key = f"form_tanggapan_{jenis_simulasi.replace(' ', '_').replace(':', '').replace('/', '_')}"

with st.form(key=form_key):
    jawaban_1 = st.text_area(
        questions["q1"],
        placeholder=questions.get("p1", "Tuliskan pertanyaan penyelidikanmu di sini."),
        height=110,
        key=f"jawaban_1_{form_key}"
    )

    jawaban_2 = st.text_area(
        questions["q2"],
        placeholder=questions.get("p2", "Tuliskan dugaan awalmu di sini."),
        height=110,
        key=f"jawaban_2_{form_key}"
    )

    jawaban_3 = st.text_area(
        questions["q3"],
        placeholder=questions.get("p3", "Tuliskan data penting dan cocokkan dengan dugaanmu."),
        height=140,
        key=f"jawaban_3_{form_key}"
    )

    kesimpulan = st.text_area(
        questions["q4"],
        placeholder=questions.get("p4", "Tuliskan kesimpulan dan tindakan nyata."),
        height=130,
        key=f"kesimpulan_{form_key}"
    )

    submit = st.form_submit_button("Kirim Tanggapan")

    if submit:
        if not jawaban_1 or not jawaban_2 or not jawaban_3 or not kesimpulan:
            st.error("Semua kolom perlu diisi. Gunakan kalimat bantu yang tersedia kalau masih bingung.")
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
                Tanggapan kamu sudah tersimpan. Guru dapat membaca pertanyaan penyelidikan,
                dugaan, bukti data, dan kesimpulan yang kamu tulis.
                """,
                "green-card"
            )