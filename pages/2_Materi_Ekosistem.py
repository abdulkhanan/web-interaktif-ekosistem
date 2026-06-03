import json
import os
from html import escape

import streamlit as st

from modules.auth import require_role
from database.init_db import init_db
from database.queries import mark_materi_selesai, is_materi_done, get_materi_selesai_codes
from components.ui import load_css, page_title, section_title, info_card, role_navigation


st.set_page_config(
    page_title="Bahan Penyelidikan",
    page_icon="📘",
    layout="wide"
)

init_db()
load_css()
require_role(["siswa"])
role_navigation()


nama_siswa = (
    st.session_state.get("nama_pengguna")
    or st.session_state.get("name")
    or st.session_state.get("email")
    or "siswa"
)


page_title(
    "📘 Bahan Penyelidikan",
    "Baca bahan penyelidikan berikut untuk membantu memahami fenomena sebelum menjalankan simulasi ekosistem."
)


st.markdown(
    """
    <style>
        .materi-text {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 24px 28px;
            margin-top: 18px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        }

        .materi-text p {
            text-align: justify;
            text-justify: inter-word;
            font-size: 16px;
            line-height: 1.9;
            color: #334155;
            margin-bottom: 16px;
        }


        .materi-caption {
            text-align: center;
            font-size: 14px;
            color: #64748b;
            margin-top: 10px;
            line-height: 1.6;
        }

        .materi-helper {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 16px;
            padding: 18px 20px;
            color: #334155;
            line-height: 1.7;
            margin-bottom: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


IMAGE_MAP = {
    "materi_1_komponen_ekosistem": {
        "path": "assets/images/komponen_ekosistem.png",
        "caption": "Gambar komponen biotik dan abiotik pada ekosistem sungai."
    },
    "materi_2_aliran_energi": {
        "path": "assets/images/rantai_makanan_piramida_energi.png",
        "caption": "Diagram rantai makanan dan piramida energi pada ekosistem."
    },
    "materi_3_daur_air_karbon_oksigen": {
        "path": "assets/images/daur_air_co2_o2.png",
        "caption": "Diagram daur air serta peran tumbuhan terhadap karbon dioksida dan oksigen."
    },
    "materi_4_daur_nitrogen_fosfor": {
        "path": "assets/images/daur_nitrogen_fosfor.png",
        "caption": "Diagram daur nitrogen, daur fosfor, dan dampak pupuk berlebih pada perairan."
    }
}


def load_materi():
    file_path = "data/materi_ekosistem.json"

    if not os.path.exists(file_path):
        st.error("File data/materi_ekosistem.json tidak ditemukan.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as error:
        st.error(f"Gagal membaca file materi: {error}")
        return []


def render_justified_text(text):
    paragraphs = [
        paragraph.strip()
        for paragraph in str(text).split("\n\n")
        if paragraph.strip()
    ]

    html_paragraphs = ""

    for paragraph in paragraphs:
        safe_paragraph = escape(paragraph)
        html_paragraphs += f"<p>{safe_paragraph}</p>"

    st.markdown(
        f"""
        <div class="materi-text">
            {html_paragraphs}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_materi_image(kode_materi):
    image_data = IMAGE_MAP.get(kode_materi)

    if not image_data:
        return

    image_path = image_data["path"]
    caption = image_data["caption"]

    if os.path.exists(image_path):
        st.image(
            image_path,
            caption=caption,
            use_container_width=True
        )
    else:
        info_card(
            "Gambar Belum Ditemukan",
            f"""
            File gambar belum tersedia. Simpan gambar pada lokasi berikut:<br>
            <strong>{image_path}</strong>
            """,
            "yellow-card"
        )

def render_materi_item(materi, nomor):
    kode = materi.get("kode", "")
    judul = materi.get("judul", f"Bahan Penyelidikan {nomor}")
    isi = materi.get("isi", "")

    sudah_dibaca = is_materi_done(nama_siswa, kode)

    section_title(judul)

    render_materi_image(kode)

    render_justified_text(isi)

    if sudah_dibaca:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #ecfdf5 0%, #dcfce7 100%);
                border: 1px solid rgba(5, 150, 105, 0.2);
                border-radius: 14px;
                padding: 14px 20px;
                color: #047857;
                font-weight: 700;
                font-size: 15px;
                text-align: center;
            ">✅ Materi ini sudah ditandai sebagai dibaca</div>
            """,
            unsafe_allow_html=True
        )
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(
                "📖 Tandai Sudah Dibaca",
                key=f"selesai_{kode}",
                use_container_width=True
            ):
                mark_materi_selesai(nama_siswa, kode, judul)
                st.rerun()



materi_list = load_materi()

if not materi_list:
    st.stop()


# --- Progress summary card ---
materi_selesai_codes = get_materi_selesai_codes(nama_siswa)
jumlah_selesai = sum(
    1 for m in materi_list
    if m.get("kode", "") in materi_selesai_codes
)
jumlah_total = len(materi_list)
persen = int(jumlah_selesai / jumlah_total * 100) if jumlah_total > 0 else 0

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border: 1px solid rgba(5, 150, 105, 0.18);
        border-radius: 20px;
        padding: 22px 28px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px -10px rgba(15, 23, 42, 0.05);
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
                <div style="font-size:13px; color:#64748b; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">Progress Bahan Penyelidikan</div>
                <div style="font-size:28px; font-weight:800; color:#047857; font-family:'Outfit',sans-serif; margin-top:4px;">{jumlah_selesai} dari {jumlah_total} Selesai</div>
            </div>
            <div style="
                background: linear-gradient(135deg, #059669 0%, #0284c7 100%);
                color: white;
                border-radius: 999px;
                padding: 8px 20px;
                font-weight: 800;
                font-size: 15px;
            ">{persen}%</div>
        </div>
        <div style="background:#e2e8f0; border-radius:999px; height:8px; margin-top:16px; overflow:hidden;">
            <div style="background:linear-gradient(90deg, #059669, #0284c7); height:100%; width:{persen}%; border-radius:999px; transition:width 0.5s ease;"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="materi-helper">
        <strong>Petunjuk:</strong>
        Pilih bahan penyelidikan sesuai urutan materi. Amati gambar, baca penjelasan,
        lalu lanjutkan ke halaman Simulasi Ekosistem untuk menyelidiki fenomena yang berkaitan.
    </div>
    """,
    unsafe_allow_html=True
)


tab_labels = []
for index, m in enumerate(materi_list):
    kode = m.get("kode", "")
    status = "✅" if kode in materi_selesai_codes else "⏳"
    tab_labels.append(f"{status} {index + 1}. Bahan Penyelidikan")

tabs = st.tabs(tab_labels)

for index, tab in enumerate(tabs):
    with tab:
        render_materi_item(materi_list[index], index + 1)


st.divider()

if st.button("➡️ Lanjut ke Simulasi Ekosistem", use_container_width=True):
    st.switch_page("pages/3_Simulasi_Ekosistem.py")