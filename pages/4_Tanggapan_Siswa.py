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
    "📝 Klaim Ilmiah Siswa",
    "Susun hasil investigasi dalam bentuk rumusan masalah, dugaan awal, pola data, dan klaim ilmiah berbasis bukti."
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
        Silakan kembali ke halaman Investigasi Ekosistem, lalu klik tombol **Gunakan Data Ini untuk Klaim Ilmiah** pada salah satu simulasi.
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





section_title("Lembar Klaim Ilmiah")

info_card(
    "Petunjuk Mengisi Jawaban",
    """
    Tulis seperti laporan investigasi singkat. Jangan menyalin teks pada halaman simulasi.
    Gunakan data yang dipilih untuk membangun klaim: apa pernyataan ilmiahmu, bukti datanya apa,
    dan alasan ekologinya bagaimana.
    """,
    "blue-card"
)

st.markdown(
    """
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:18px; padding:16px; margin:6px 0 20px 0;">
        <b>Struktur jawaban:</b> Rumusan masalah → Dugaan awal → Pola data → Klaim, bukti, alasan, dan implikasi.
    </div>
    """,
    unsafe_allow_html=True
)

questions = get_guided_questions(jenis_simulasi)

form_key = f"form_tanggapan_{jenis_simulasi.replace(' ', '_').replace(':', '').replace('/', '_')}"

with st.form(key=form_key):
    jawaban_1 = st.text_area(
        questions["q1"],
        placeholder=questions.get("p1", "Rumuskan masalah penyelidikan secara mandiri."),
        height=110,
        key=f"jawaban_1_{form_key}"
    )

    jawaban_2 = st.text_area(
        questions["q2"],
        placeholder=questions.get("p2", "Tuliskan hipotesis dan alasan ilmiahnya."),
        height=110,
        key=f"jawaban_2_{form_key}"
    )

    jawaban_3 = st.text_area(
        questions["q3"],
        placeholder=questions.get("p3", "Analisis data dan tentukan apakah hipotesis didukung."),
        height=140,
        key=f"jawaban_3_{form_key}"
    )

    kesimpulan = st.text_area(
        questions["q4"],
        placeholder=questions.get("p4", "Tuliskan kesimpulan berbasis bukti."),
        height=130,
        key=f"kesimpulan_{form_key}"
    )

    submit = st.form_submit_button("Kirim Tanggapan")

    if submit:
        if not jawaban_1 or not jawaban_2 or not jawaban_3 or not kesimpulan:
            st.error("Semua kolom perlu diisi agar alur guided inquiry lengkap.")
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
                "Klaim Ilmiah Berhasil Dikirim",
                """
                Jawaban kamu sudah tersimpan. Guru dapat membaca rumusan masalah,
                dugaan awal, analisis pola data, dan klaim ilmiah yang kamu tulis.
                """,
                "green-card"
            )