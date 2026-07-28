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
            margin-top: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        }

        div[data-testid="stImage"] {
            width: 100%;
            height: 420px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-radius: 14px;
            background: #ffffff;
        }

        div[data-testid="stImage"] img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            object-position: center;
            border-radius: 14px;
            display: block;
        }
        
        .materi-text p {
            text-align: justify;
            text-justify: inter-word;
            font-size: 16px;
            line-height: 1.9;
            color: #334155;
            margin: 0 0 16px 0;
        }

        .materi-text p:last-child {
            margin-bottom: 0;
        }

        .materi-text ul {
            margin: 10px 0 0 22px;
            padding: 0;
        }

        .materi-text li {
            font-size: 16px;
            line-height: 1.8;
            color: #334155;
            margin-bottom: 8px;
        }

        .materi-section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 30px;
            margin-bottom: 6px;
            color: #0f5132;
        }

        .materi-section-letter {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: #dcfce7;
            border: 1px solid #86efac;
            color: #047857;
            font-weight: 800;
            flex-shrink: 0;
        }

        .materi-section-name {
            font-size: 23px;
            line-height: 1.35;
            font-weight: 800;
        }

        .materi-subtitle {
            font-size: 19px;
            line-height: 1.45;
            color: #0f5132;
            font-weight: 800;
            margin: 4px 0 10px 0;
        }

        .materi-caption {
            min-height: 52px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 14px;
            font-weight: 700;
            color: #475569;
            margin-top: 8px;
            line-height: 1.55;
        }

        .materi-source {
            min-height: 58px;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            text-align: center;
            font-size: 13px;
            font-style: italic;
            color: #64748b;
            margin-top: 3px;
            margin-bottom: 16px;
            line-height: 1.5;
            overflow-wrap: anywhere;
            word-break: break-word;
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

        .materi-overview {
            background: linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%);
            border: 1px solid #a7f3d0;
            border-radius: 18px;
            padding: 20px 24px;
            color: #334155;
            line-height: 1.8;
            margin: 8px 0 20px 0;
        }

        .materi-callout {
            background: #fff7ed;
            border-left: 5px solid #f97316;
            border-radius: 14px;
            padding: 16px 20px;
            color: #7c2d12;
            line-height: 1.75;
            margin: 10px 0 22px 0;
        }

        .materi-flow {
            background: #f0fdf4;
            border: 1px dashed #22c55e;
            border-radius: 16px;
            padding: 18px 20px;
            text-align: center;
            color: #166534;
            font-size: 17px;
            font-weight: 800;
            line-height: 1.7;
            margin: 6px 0 22px 0;
        }

        .materi-reference {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 18px;
            padding: 22px 26px;
            margin-top: 28px;
            margin-bottom: 22px;
        }

        .materi-reference h3 {
            color: #0f5132;
            margin: 0 0 12px 0;
            font-size: 22px;
        }

        .materi-reference ol {
            margin: 0 0 0 22px;
            padding: 0;
        }

        .materi-reference li {
            color: #334155;
            font-size: 15px;
            line-height: 1.75;
            margin-bottom: 9px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


IMAGE_MAP = {
    "materi_2_aliran_energi": {
        "path": "assets/images/rantai_makanan_piramida_energi.png",
        "judul": "Diagram rantai makanan dan piramida energi pada ekosistem.",
        "sumber": "Aset gambar yang tersedia dalam proyek web interaktif ekosistem."
    },
    "materi_3_daur_air_karbon_oksigen": {
        "path": "assets/images/daur_air_co2_o2.png",
        "judul": "Diagram daur air serta peran tumbuhan terhadap karbon dioksida dan oksigen.",
        "sumber": "Aset gambar yang tersedia dalam proyek web interaktif ekosistem."
    },
    "materi_4_daur_nitrogen_fosfor": {
        "path": "assets/images/daur_nitrogen_fosfor.png",
        "judul": "Diagram daur nitrogen, daur fosfor, dan dampak pupuk berlebih pada perairan.",
        "sumber": "Aset gambar yang tersedia dalam proyek web interaktif ekosistem."
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


def normalize_paragraphs(content):
    if isinstance(content, list):
        return [str(item).strip() for item in content if str(item).strip()]

    return [
        paragraph.strip()
        for paragraph in str(content or "").split("\n\n")
        if paragraph.strip()
    ]


def render_text_block(paragraphs, points=None):
    safe_paragraphs = "".join(
        f"<p>{escape(paragraph)}</p>"
        for paragraph in normalize_paragraphs(paragraphs)
    )

    safe_points = ""
    if points:
        list_items = "".join(
            f"<li>{escape(str(point))}</li>"
            for point in points
            if str(point).strip()
        )
        safe_points = f"<ul>{list_items}</ul>"

    st.markdown(
        f"""
        <div class="materi-text">
            {safe_paragraphs}
            {safe_points}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_image_with_source(image_data):
    if not image_data:
        return

    image_path = image_data.get("path", "")
    title = image_data.get("judul") or image_data.get("caption", "")
    source = image_data.get("sumber", "Sumber belum dicantumkan.")

    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
        st.markdown(
            f"""
            <div class="materi-caption">{escape(title)}</div>
            <div class="materi-source">Sumber: {escape(source)}</div>
            """,
            unsafe_allow_html=True
        )
    else:
        info_card(
            "Gambar Belum Ditemukan",
            f"""
            File gambar belum tersedia. Simpan gambar pada lokasi berikut:<br>
            <strong>{escape(image_path)}</strong>
            """,
            "yellow-card"
        )


def render_section_heading(letter, title):
    st.markdown(
        f"""
        <div class="materi-section-title">
            <span class="materi-section-letter">{escape(letter)}</span>
            <span class="materi-section-name">{escape(title)}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_subsection(subsection):
    number = subsection.get("nomor", "")
    title = subsection.get("judul", "")
    image_path = subsection.get("gambar", "")

    st.markdown(
        f'<div class="materi-subtitle">{escape(number)}. {escape(title)}</div>',
        unsafe_allow_html=True
    )

    if image_path:
        render_image_with_source({
            "path": image_path,
            "judul": subsection.get("caption", ""),
            "sumber": subsection.get("sumber", "")
        })

    render_text_block(subsection.get("paragraf", []))


def render_references(references):
    if not references:
        return

    list_items = "".join(
        f"<li>{escape(str(reference))}</li>"
        for reference in references
        if str(reference).strip()
    )

    st.markdown(
        f"""
        <div class="materi-reference">
            <h3>📚 Referensi</h3>
            <ol>{list_items}</ol>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_structured_materi(materi):
    summary = materi.get("ringkasan", "")
    if summary:
        st.markdown(
            f'<div class="materi-overview"><strong>Gambaran materi:</strong> {escape(summary)}</div>',
            unsafe_allow_html=True
        )

    render_image_with_source(materi.get("gambar_utama"))

    for section in materi.get("bagian", []):
        render_section_heading(
            section.get("huruf", ""),
            section.get("judul", "")
        )

        render_text_block(
            section.get("paragraf", []),
            section.get("poin", [])
        )

        section_image = section.get("gambar")
        if section_image:
            render_image_with_source(section_image)
        
        subsections = section.get("subbagian", [])

        if subsections:
            # Membuat kolom baru untuk setiap pasangan subbagian
            for index in range(0, len(subsections), 2):
                columns = st.columns(2, gap="large")

                # Bagian sebelah kiri
                with columns[0]:
                    render_subsection(subsections[index])

                # Bagian sebelah kanan
                if index + 1 < len(subsections):
                    with columns[1]:
                        render_subsection(subsections[index + 1])

                # Jarak antarbaris kartu
                st.markdown(
                    '<div style="height: 24px;"></div>',
                    unsafe_allow_html=True
                )

    render_references(materi.get("referensi", []))


def render_legacy_materi(materi):
    kode = materi.get("kode", "")
    image_data = IMAGE_MAP.get(kode)
    render_image_with_source(image_data)
    render_text_block(materi.get("isi", ""))


def render_materi_item(materi, nomor):
    kode = materi.get("kode", "")
    judul = materi.get("judul", f"Bahan Penyelidikan {nomor}")
    sudah_dibaca = is_materi_done(nama_siswa, kode)

    section_title(judul)

    if materi.get("bagian"):
        render_structured_materi(materi)
    else:
        render_legacy_materi(materi)

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
        col1, _ = st.columns([1, 3])
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
        Pilih bahan penyelidikan sesuai urutan materi. Amati setiap gambar dan sumbernya,
        baca penjelasan pada setiap subbagian, lalu lanjutkan ke halaman Simulasi Ekosistem.
    </div>
    """,
    unsafe_allow_html=True
)


tab_labels = []
for index, material in enumerate(materi_list):
    kode = material.get("kode", "")
    status = "✅" if kode in materi_selesai_codes else "⏳"
    tab_labels.append(f"{status} {index + 1}. Bahan Penyelidikan")

tabs = st.tabs(tab_labels)

for index, tab in enumerate(tabs):
    with tab:
        render_materi_item(materi_list[index], index + 1)


st.divider()

if st.button("➡️ Lanjut ke Simulasi Ekosistem", use_container_width=True):
    st.switch_page("pages/3_Simulasi_Ekosistem.py")
