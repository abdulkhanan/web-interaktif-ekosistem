import streamlit as st
import pandas as pd
import os
import altair as alt

from modules.simulation import (
    hitung_pencemaran_sungai,
    buat_tren_pencemaran_sungai,
    hitung_aliran_energi,
    hitung_daur_air,
    buat_tren_daur_air,
    hitung_eutrofikasi,
    buat_tren_eutrofikasi
)

from modules.auth import require_role
from database.init_db import init_db
from database.queries import update_progress
from components.ui import load_css, page_title, section_title, info_card, role_navigation


st.set_page_config(
    page_title="Simulasi Ekosistem",
    page_icon="🌏",
    layout="wide"
)

@st.cache_resource
def cached_init_db():
    init_db()

cached_init_db()
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
    "🌏 Simulasi Ekosistem",
    "Amati fenomena lingkungan, ubah variabel simulasi, lalu gunakan data untuk memahami konsep ekosistem."
)


info_card(
    "Bahan Penyelidikan",
    """
    Sebelum menjalankan simulasi, siswa dapat membaca materi terlebih dahulu sebagai bahan pengetahuan.
    Materi tidak menjadi syarat untuk membuka simulasi, tetapi digunakan untuk membantu siswa memahami konsep dasar sebelum melakukan penyelidikan.
    """,
    "blue-card"
)

col_bahan, col_keterangan = st.columns([1, 3])

with col_bahan:
    if st.button("📘 Pelajari Bahan Penyelidikan"):
        st.switch_page("pages/2_Materi_Ekosistem.py")

st.divider()


# ============================================================
# FUNGSI BANTUAN
# ============================================================

def simpan_hasil_simulasi(jenis_simulasi, input_simulasi, hasil_simulasi):
    st.session_state["hasil_simulasi"] = {
        "jenis_simulasi": jenis_simulasi,
        "input_simulasi": input_simulasi,
        "hasil_simulasi": hasil_simulasi
    }

    update_progress(nama_siswa, "simulasi_dijalankan")
    st.session_state["simulasi_tersimpan"] = jenis_simulasi


def tampilkan_grafik_kurva(df, x_col, y_cols, warna_map, judul, ylabel="Nilai Parameter"):
    """Menampilkan grafik garis interaktif yang cepat menggunakan st.altair_chart tanpa zoom/pan."""
    cols_to_plot = [c for c in y_cols if c in df.columns]
    warna_list = [warna_map.get(col, "#64748b") for col in cols_to_plot]
    
    # Melt df to long format for Altair plotting
    df_melted = df.melt(id_vars=[x_col], value_vars=cols_to_plot, var_name='Parameter', value_name='Nilai')
    
    chart = alt.Chart(df_melted).mark_line(
        strokeWidth=3,
        point=alt.OverlayMarkDef(size=60, filled=True)
    ).encode(
        x=alt.X(f'{x_col}:Q', 
                scale=alt.Scale(domain=[0, 30], nice=False, clamp=True), 
                axis=alt.Axis(title=x_col, values=[0, 5, 10, 15, 20, 25, 30], grid=True)),
        y=alt.Y(
            'Nilai:Q',
            scale=alt.Scale(
                domain=[0, 100],
                nice=False,
                clamp=True
            ),
            axis=alt.Axis(
                title=ylabel,
                values=[0, 20, 40, 60, 80, 100],
                tickCount=6,
                grid=True,
                labelOverlap=False
            )
        ),
        color=alt.Color('Parameter:N', 
                        scale=alt.Scale(domain=cols_to_plot, range=warna_list),
                        legend=alt.Legend(orient='bottom', columns=min(4, len(cols_to_plot)), title=None)),
        tooltip=[
            alt.Tooltip(f'{x_col}:Q', title=x_col),
            alt.Tooltip('Parameter:N', title='Parameter'),
            alt.Tooltip('Nilai:Q', title='Nilai', format='.1f')
        ]
    ).properties(
        title=alt.TitleParams(
            text=judul,
            fontSize=14,
            fontWeight='bold',
            anchor='start',
            color='#0f172a'
        ),
        height=320,
        background='#ffffff'
    ).configure_view(
        stroke=None,
        fill='#ffffff'
    ).configure_axis(
        domainColor='#cbd5e1',
        tickColor='#cbd5e1',
        labelColor='#334155',
        titleColor='#0f172a',
        gridColor='#e2e8f0',
        gridDash=[4, 4]
    ).configure_legend(
        labelColor='#334155',
        titleColor='#0f172a',
        orient='bottom'
    ).configure_title(
        color='#0f172a'
    )
    
    st.altair_chart(chart, use_container_width=True)


def status_pencemaran_card(hasil):
    indeks_invertebrata = float(hasil["makroinvertebrata"])

    warna_limbah = (
        "#16a34a"
        if hasil["status_limbah"] == "Rendah"
        else "#f97316"
        if hasil["status_limbah"] == "Sedang"
        else "#dc2626"
    )

    warna_do = (
        "#16a34a"
        if hasil["status_do"] == "Normal"
        else "#f97316"
        if hasil["status_do"] == "Menurun"
        else "#dc2626"
    )

    warna_ikan = (
        "#16a34a"
        if hasil["status_populasi_ikan"] == "Stabil"
        else "#f97316"
        if hasil["status_populasi_ikan"] == "Menurun"
        else "#dc2626"
    )

    warna_invertebrata = (
        "#16a34a"
        if indeks_invertebrata >= 70
        else "#f97316"
        if indeks_invertebrata >= 40
        else "#dc2626"
    )

    status_html = (
        "<div style='background-color:white; padding:16px; border-radius:14px; "
        "box-shadow:0 3px 10px rgba(0,0,0,0.08); margin-bottom:20px;'>"
        "<div style='display:grid; grid-template-columns:repeat(2, minmax(180px, 1fr)); gap:16px;'>"

        "<div>"
        "<div style='font-size:16px; font-weight:700; color:#1f2937;'>Limbah Saat Ini:</div>"
        f"<div style='font-size:20px; font-weight:800; color:{warna_limbah}; margin-top:8px;'>"
        f"{hasil['status_limbah']}</div>"
        "</div>"

        "<div>"
        "<div style='font-size:16px; font-weight:700; color:#1f2937;'>Tingkat DO:</div>"
        f"<div style='font-size:20px; font-weight:800; color:{warna_do}; margin-top:8px;'>"
        f"{hasil['status_do']} ({hasil['nilai_do']} mg/L)</div>"
        "</div>"

        "<div>"
        "<div style='font-size:16px; font-weight:700; color:#1f2937;'>Populasi Ikan:</div>"
        f"<div style='font-size:20px; font-weight:800; color:{warna_ikan}; margin-top:8px;'>"
        f"{hasil['status_populasi_ikan']} ({hasil['populasi_ikan']}%)</div>"
        "</div>"

        "<div>"
        "<div style='font-size:16px; font-weight:700; color:#1f2937;'>Indeks Invertebrata:</div>"
        f"<div style='font-size:20px; font-weight:800; color:{warna_invertebrata}; margin-top:8px;'>"
        f"{indeks_invertebrata:.1f}</div>"
        "</div>"

        "</div>"
        "</div>"
    )

    st.markdown(status_html, unsafe_allow_html=True)


def status_rantai_makanan_card(hasil, energi_awal, penurunan_produsen, efisiensi_transfer):
    status_html = (
        "<div style='background-color:white; padding:16px; border-radius:14px; "
        "box-shadow:0 3px 10px rgba(0,0,0,0.08); margin-bottom:20px;'>"
        "<div style='display:grid; grid-template-columns:repeat(3, minmax(120px, 1fr)); gap:16px;'>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Energi Produsen (Setelah Kemarau):</div>"
        f"<div style='font-size:18px; font-weight:800; color:#16a34a; margin-top:8px;'>"
        f"{energi_awal:,.0f} kkal</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Rumput Berkurang:</div>"
        f"<div style='font-size:18px; font-weight:800; color:#dc2626; margin-top:8px;'>"
        f"{penurunan_produsen}%</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Efisiensi Transfer:</div>"
        f"<div style='font-size:18px; font-weight:800; color:#2563eb; margin-top:8px;'>"
        f"{efisiensi_transfer}%</div>"
        "</div>"
        
        "</div>"
        "</div>"
    )
    st.markdown(status_html, unsafe_allow_html=True)


def status_daur_air_card(hasil):
    status_html = (
        "<div style='background-color:white; padding:16px; border-radius:14px; "
        "box-shadow:0 3px 10px rgba(0,0,0,0.08); margin-bottom:20px;'>"
        "<div style='display:grid; grid-template-columns:repeat(2, minmax(180px, 1fr)); gap:16px;'>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Infiltrasi:</div>"
        f"<div style='font-size:18px; font-weight:800; color:#16a34a; margin-top:8px;'>"
        f"{hasil['infiltrasi']:.1f}%</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Limpasan Permukaan:</div>"
        f"<div style='font-size:18px; font-weight:800; color:#dc2626; margin-top:8px;'>"
        f"{hasil['limpasan_permukaan']:.1f}%</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>CO2 Diserap:</div>"
        f"<div style='font-size:18px; font-weight:800; color:#2563eb; margin-top:8px;'>"
        f"{hasil['penyerapan_karbon_dioksida']:.1f}%</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>O2 Dihasilkan:</div>"
        f"<div style='font-size:18px; font-weight:800; color:#059669; margin-top:8px;'>"
        f"{hasil['produksi_oksigen']:.1f}%</div>"
        "</div>"
        
        "</div>"
        "</div>"
    )
    st.markdown(status_html, unsafe_allow_html=True)


def status_eutrofikasi_card(hasil):
    warna_nutrien = (
        "#16a34a"
        if hasil["status_eutrofikasi"] == "Rendah"
        else "#f97316"
        if hasil["status_eutrofikasi"] == "Sedang"
        else "#dc2626"
    )
    warna_alga = (
        "#16a34a"
        if hasil["status_alga"] == "Normal"
        else "#f97316"
        if hasil["status_alga"] == "Meningkat"
        else "#dc2626"
    )
    warna_do = (
        "#16a34a"
        if hasil["status_do"] == "Normal"
        else "#f97316"
        if hasil["status_do"] == "Menurun"
        else "#dc2626"
    )
    warna_organisme = (
        "#16a34a"
        if hasil["kondisi_organisme"] >= 70
        else "#f97316"
        if hasil["kondisi_organisme"] >= 40
        else "#dc2626"
    )
    
    status_html = (
        "<div style='background-color:white; padding:16px; border-radius:14px; "
        "box-shadow:0 3px 10px rgba(0,0,0,0.08); margin-bottom:20px;'>"
        "<div style='display:grid; grid-template-columns:repeat(2, minmax(180px, 1fr)); gap:16px;'>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Zat Hara:</div>"
        f"<div style='font-size:18px; font-weight:800; color:{warna_nutrien}; margin-top:8px;'>"
        f"{hasil['indeks_nutrien']:.1f}% ({hasil['status_eutrofikasi']})</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Pertumbuhan Alga:</div>"
        f"<div style='font-size:18px; font-weight:800; color:{warna_alga}; margin-top:8px;'>"
        f"{hasil['pertumbuhan_alga']:.1f}%</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Oksigen Air (DO):</div>"
        f"<div style='font-size:18px; font-weight:800; color:{warna_do}; margin-top:8px;'>"
        f"{hasil['indeks_oksigen_air']:.1f}%</div>"
        "</div>"
        
        "<div>"
        "<div style='font-size:14px; font-weight:700; color:#4b5563;'>Kondisi Organisme:</div>"
        f"<div style='font-size:18px; font-weight:800; color:{warna_organisme}; margin-top:8px;'>"
        f"{hasil['kondisi_organisme']:.1f}%</div>"
        "</div>"
        
        "</div>"
        "</div>"
    )
    st.markdown(status_html, unsafe_allow_html=True)



# ============================================================
# TAB SIMULASI
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Pencemaran Sungai",
    "2. Rantai Makanan",
    "3. Daur Air dan Carbon",
    "4. Peningkatan Alga akibat Fosfor dan Nitrogen"
])


# ============================================================
# TAB 1: PENCEMARAN SUNGAI
# ============================================================

with tab1:
    jenis_simulasi = "Pencemaran Sungai Akibat Limbah Pabrik"

    section_title("Simulasi Pencemaran Sungai Akibat Limbah Pabrik")

    info_card(
        "Orientasi dan Penyajian Fenomena",
        """
        Limbah pabrik yang masuk ke sungai dapat mengubah kondisi air.
        Air menjadi tercemar, kadar oksigen terlarut menurun, dan organisme air dapat terganggu.
        Fenomena ini menunjukkan hubungan antara komponen abiotik seperti air, limbah, dan oksigen dengan komponen biotik seperti ikan dan hewan kecil di air.
        """,
        "blue-card"
    )

    info_card(
        "Tujuan Penyelidikan",
        """
        Gunakan simulasi ini untuk mengamati pengaruh tingkat limbah industri terhadap oksigen terlarut,
        populasi ikan, indeks invertebrata, dan kondisi ekosistem sungai.
        """,
        "green-card"
    )



    col_kiri, col_kanan = st.columns([1, 1.4])

    with col_kiri:
        image_path = os.path.join("assets", "images", "pencemaran_sungai.jpg")

        if os.path.exists(image_path):
            st.image(image_path, width="stretch")
        else:
            info_card(
                "Gambar Belum Tersedia",
                """
                Simpan gambar pencemaran sungai pada folder:
                assets/images/pencemaran_sungai.jpg
                """,
                "yellow-card"
            )

        st.markdown(
            """
            <p style='text-align:center; color:#6b7280; line-height:1.7; font-size:15px;'>
            Gambar ini menggambarkan kondisi sungai yang tercemar limbah.
            Siswa dapat mengamati hubungan antara peningkatan limbah,
            penurunan oksigen terlarut, dan gangguan organisme air.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Coba Ubah Variabel")

        tingkat_limbah = st.slider(
            "Tingkat Limbah Industri",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.01
        )

    with col_kanan:
        hasil = hitung_pencemaran_sungai(tingkat_limbah)
        data_tren = buat_tren_pencemaran_sungai(tingkat_limbah)
        df_tren = pd.DataFrame(data_tren)

        st.markdown("### Hasil Pengamatan")
        status_pencemaran_card(hasil)

        tampilkan_grafik_kurva(
            df=df_tren,
            x_col="Waktu (hari)",
            y_cols=[
                "Indeks Limbah",
                "Kualitas Air",
                "Indeks DO",
                "Populasi Ikan",
                "Indeks Invertebrata"
            ],
            warna_map={
                "Indeks Limbah": "#ef4444",
                "Kualitas Air": "#10b981",
                "Indeks DO": "#0284c7",
                "Populasi Ikan": "#8b5cf6",
                "Indeks Invertebrata": "#eab308"
            },
            judul="Tren Parameter Ekosistem Sungai dari Waktu ke Waktu",
            ylabel="Nilai Indeks"
        )

        st.dataframe(df_tren, width="stretch", hide_index=True)

        info_card(
            "Kondisi Ekosistem",
            hasil["kondisi"],
            "green-card"
            if hasil["tingkat_pencemaran"] <= 30
            else "yellow-card"
            if hasil["tingkat_pencemaran"] <= 70
            else "danger-card"
        )

    if st.button("Gunakan Simulasi Pencemaran Sungai"):
        simpan_hasil_simulasi(
            jenis_simulasi,
            {
                "tingkat_limbah_industri": tingkat_limbah,
                "indeks_limbah": hasil["indeks_limbah"],
                "tingkat_pencemaran": hasil["tingkat_pencemaran"]
            },
            hasil
        )

    if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
        st.success(f"{jenis_simulasi} berhasil dipilih. Silakan lanjut ke halaman Tanggapan Siswa.")
        if st.button("✍️ Lanjut ke Tanggapan Siswa", key="ke_tanggapan_1"):
            st.switch_page("pages/4_Tanggapan_Siswa.py")


# ============================================================
# TAB 2: RANTAI MAKANAN
# ============================================================

with tab2:
    jenis_simulasi = "Rantai Makanan Saat Kemarau"

    section_title("Simulasi Rantai Makanan Saat Kemarau")

    info_card(
        "Orientasi dan Penyajian Fenomena",
        """
        Saat kemarau panjang, rumput di padang rumput dapat berkurang karena kekurangan air.
        Rumput adalah produsen yang menjadi sumber energi bagi hewan pemakan tumbuhan.
        Ketika jumlah rumput berkurang, energi yang tersedia untuk konsumen I, konsumen II, dan konsumen III juga ikut menurun.
        """,
        "blue-card"
    )

    info_card(
        "Tujuan Penyelidikan",
        """
        Gunakan simulasi ini untuk melihat pengaruh berkurangnya produsen terhadap energi
        pada setiap tingkatan dalam rantai makanan.
        """,
        "green-card"
    )

    col_kiri, col_kanan = st.columns([1, 1.4])

    with col_kiri:
        image_path = os.path.join("assets", "images", "rantai_makanan_piramida_energi.png")

        if os.path.exists(image_path):
            st.image(image_path, width="stretch")
        else:
            info_card(
                "Gambar Belum Tersedia",
                """
                Simpan gambar rantai makanan pada folder:
                assets/images/rantai_makanan_piramida_energi.png
                """,
                "yellow-card"
            )

        st.markdown(
            """
            <p style='text-align:center; color:#6b7280; line-height:1.7; font-size:15px;'>
            Gambar ini menunjukkan piramida energi pada ekosistem rantai makanan padang rumput.
            Siswa dapat mengamati bagaimana energi berkurang secara drastis pada setiap tingkat trofik.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Coba Ubah Variabel")

        energi_produsen_normal = st.number_input(
            "Energi produsen sebelum kemarau (kkal)",
            min_value=100,
            max_value=100000,
            value=10000,
            step=100
        )

        penurunan_produsen = st.slider(
            "Rumput yang berkurang akibat kemarau (%)",
            min_value=0,
            max_value=90,
            value=30
        )

        efisiensi_transfer = st.slider(
            "Energi yang berpindah ke makhluk hidup berikutnya (%)",
            min_value=5,
            max_value=30,
            value=10
        )

    with col_kanan:
        energi_awal = energi_produsen_normal * (1 - penurunan_produsen / 100)
        hasil = hitung_aliran_energi(energi_awal, efisiensi_transfer)

        st.markdown("### Hasil Pengamatan")
        status_rantai_makanan_card(hasil, energi_awal, penurunan_produsen, efisiensi_transfer)

        data = pd.DataFrame({
            "Tingkatan Rantai Makanan": [
                "Produsen",
                "Konsumen I",
                "Konsumen II",
                "Konsumen III"
            ],
            "Energi": [
                hasil["produsen"],
                hasil["konsumen_1"],
                hasil["konsumen_2"],
                hasil["konsumen_3"]
            ]
        })

        st.dataframe(data, width="stretch", hide_index=True)

        info_card("Keterangan", hasil["keterangan"], "yellow-card")

    if st.button("Gunakan Simulasi Rantai Makanan"):
        simpan_hasil_simulasi(
            jenis_simulasi,
            {
                "energi_produsen_normal": energi_produsen_normal,
                "rumput_berkurang_akibat_kemarau": penurunan_produsen,
                "energi_produsen_setelah_kemarau": energi_awal,
                "perpindahan_energi": efisiensi_transfer
            },
            hasil
        )

    if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
        st.success(f"{jenis_simulasi} berhasil dipilih. Silakan lanjut ke halaman Tanggapan Siswa.")
        if st.button("✍️ Lanjut ke Tanggapan Siswa", key="ke_tanggapan_2"):
            st.switch_page("pages/4_Tanggapan_Siswa.py")


# ============================================================
# TAB 3: DAUR AIR, CO2, DAN O2
# ============================================================

with tab3:
    jenis_simulasi = "Daur Air, Karbon Dioksida, dan Oksigen Saat Pohon Berkurang"

    section_title("Simulasi Daur Air, CO2, dan O2 Saat Pohon Berkurang")

    info_card(
        "Orientasi dan Penyajian Fenomena",
        """
        Penebangan pohon dapat mengurangi tutupan vegetasi.
        Ketika pohon berkurang, air hujan lebih sedikit meresap ke tanah dan lebih banyak mengalir di permukaan.
        Tumbuhan juga berperan menyerap karbon dioksida dan menghasilkan oksigen.
        """,
        "blue-card"
    )

    info_card(
        "Tujuan Penyelidikan",
        """
        Gunakan simulasi ini untuk melihat pengaruh curah hujan dan tutupan vegetasi terhadap daur air,
        penyerapan CO2, dan produksi O2. Variabel panas matahari dibuat tetap agar penyelidikan lebih fokus.
        """,
        "green-card"
    )

    col_kiri, col_kanan = st.columns([1, 1.4])

    with col_kiri:
        image_path = os.path.join("assets", "images", "diagram_daur_air_co2_o2.png")

        if os.path.exists(image_path):
            st.image(image_path, width="stretch")
        else:
            info_card(
                "Gambar Belum Tersedia",
                """
                Simpan gambar diagram pada folder:
                assets/images/diagram_daur_air_co2_o2.png
                """,
                "yellow-card"
            )

        st.markdown(
            """
            <p style='text-align:center; color:#6b7280; line-height:1.7; font-size:15px;'>
            Diagram ini mengilustrasikan daur air, penyerapan karbon dioksida (CO2), dan pelepasan oksigen (O2) oleh vegetasi tumbuhan.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Coba Ubah Variabel")

        intensitas_panas = 60

        curah_hujan = st.slider(
            "Curah Hujan",
            min_value=0,
            max_value=100,
            value=70
        )

        tutupan_vegetasi = st.slider(
            "Tutupan Vegetasi Setelah Penebangan",
            min_value=0,
            max_value=100,
            value=50
        )

    with col_kanan:
        hasil = hitung_daur_air(
            curah_hujan=curah_hujan,
            tutupan_vegetasi=tutupan_vegetasi,
            intensitas_panas=intensitas_panas
        )

        st.markdown("### Hasil Pengamatan")
        status_daur_air_card(hasil)

        info_card(
            "Alur Sebab-Akibat",
            """
            Curah hujan dan tutupan vegetasi memengaruhi kondisi lingkungan.
            Jika vegetasi berkurang, akar tumbuhan yang membantu penyerapan air juga berkurang.
            Akibatnya, infiltrasi menurun dan limpasan permukaan meningkat.
            Pada saat yang sama, jumlah tumbuhan yang menyerap CO2 dan menghasilkan O2 juga menurun.
            """,
            "yellow-card"
        )

        info_card(
            "Status",
            hasil["status"],
            "green-card"
            if hasil["status"] == "Baik"
            else "yellow-card"
            if hasil["status"] == "Cukup"
            else "danger-card"
        )

        info_card(
            "Keterangan",
            hasil["keterangan"],
            "yellow-card"
        )

    data_tren_air = buat_tren_daur_air(
        curah_hujan=curah_hujan,
        tutupan_vegetasi_akhir=tutupan_vegetasi,
        intensitas_panas=intensitas_panas
    )

    df_tren_air = pd.DataFrame(data_tren_air)

    col_grafik1, col_grafik2 = st.columns(2)

    with col_grafik1:
        st.markdown("### Grafik 1. Daur Air")

        tampilkan_grafik_kurva(
            df=df_tren_air,
            x_col="Waktu (hari)",
            y_cols=[
                "Infiltrasi",
                "Limpasan Permukaan"
            ],
            warna_map={
                "Infiltrasi": "#10b981",
                "Limpasan Permukaan": "#ef4444"
            },
            judul="Vegetasi terhadap Air Hujan",
            ylabel="Nilai Indeks"
        )

        st.info(
            """
            Ketika tutupan vegetasi berkurang, infiltrasi menurun dan limpasan permukaan meningkat.
            """
        )

    with col_grafik2:
        st.markdown("### Grafik 2. CO2 dan O2")

        tampilkan_grafik_kurva(
            df=df_tren_air,
            x_col="Waktu (hari)",
            y_cols=[
                "CO2 Diserap",
                "O2 Dihasilkan"
            ],
            warna_map={
                "CO2 Diserap": "#64748b",
                "O2 Dihasilkan": "#22c55e"
            },
            judul="Vegetasi terhadap CO2 dan O2",
            ylabel="Nilai Indeks"
        )

        st.info(
            """
            Semakin sedikit tutupan vegetasi, semakin rendah CO2 yang diserap dan O2 yang dihasilkan.
            """
        )

    with st.expander("📊 Lihat Data Lengkap Simulasi"):
        st.dataframe(
            df_tren_air,
            width="stretch",
            hide_index=True
        )

    if st.button("Gunakan Simulasi Daur Air, CO2, dan O2"):
        simpan_hasil_simulasi(
            jenis_simulasi,
            {
                "curah_hujan": curah_hujan,
                "tutupan_vegetasi_setelah_penebangan": tutupan_vegetasi,
                "panas_matahari_tetap": intensitas_panas
            },
            hasil
        )

    if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
        st.success(f"{jenis_simulasi} berhasil dipilih. Silakan lanjut ke halaman Tanggapan Siswa.")
        if st.button("✍️ Lanjut ke Tanggapan Siswa", key="ke_tanggapan_3"):
            st.switch_page("pages/4_Tanggapan_Siswa.py")

# ============================================================
# TAB 4: PENINGKATAN ALGA
# ============================================================

with tab4:
    jenis_simulasi = "Peningkatan Alga Akibat Pupuk Berlebih"

    section_title("Simulasi Peningkatan Alga Akibat Pupuk Berlebih")

    info_card(
        "Orientasi dan Penyajian Fenomena",
        """
        Pupuk pertanian yang digunakan secara berlebihan dapat terbawa air hujan ke sungai atau danau.
        Pupuk mengandung zat hara seperti nitrogen dan fosfor.
        Jika zat hara masuk ke perairan dalam jumlah banyak, alga dapat tumbuh semakin banyak.
        Fenomena peningkatan alga ini dalam ilmu ekologi dikenal sebagai eutrofikasi.
        """,
        "blue-card"
    )

    info_card(
        "Tujuan Penyelidikan",
        """
        Gunakan simulasi ini untuk melihat pengaruh nitrogen dan fosfor terhadap pertumbuhan alga,
        oksigen air, dan kondisi organisme air.
        """,
        "green-card"
    )

    col_kiri, col_kanan = st.columns([1, 1.4])

    with col_kiri:
        image_path = os.path.join("assets", "images", "peningkatan_alga_akibat_pupuk_berlebih.png")

        if os.path.exists(image_path):
            st.image(image_path, width="stretch")
        else:
            info_card(
                "Gambar Belum Tersedia",
                """
                Simpan gambar simulasi 4 pada folder:
                assets/images/peningkatan_alga_akibat_pupuk_berlebih.png
                """,
                "yellow-card"
            )

        st.markdown(
            """
            <p style='text-align:center; color:#6b7280; line-height:1.7; font-size:15px;'>
            Gambar ini mengilustrasikan peristiwa eutrofikasi (ledakan pertumbuhan alga) di permukaan air yang dipicu oleh pemupukan berlebih.
            </p>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Coba Ubah Variabel")

        kadar_nitrogen = st.slider("Nitrogen dari Pupuk", min_value=0, max_value=100, value=50)
        kadar_fosfor = st.slider("Fosfor dari Pupuk", min_value=0, max_value=100, value=50)

    with col_kanan:
        hasil = hitung_eutrofikasi(kadar_nitrogen, kadar_fosfor)
        data_tren = buat_tren_eutrofikasi(kadar_nitrogen, kadar_fosfor)
        df_tren = pd.DataFrame(data_tren)

        st.markdown("### Hasil Pengamatan")
        status_eutrofikasi_card(hasil)

        tampilkan_grafik_kurva(
            df=df_tren,
            x_col="Waktu (hari)",
            y_cols=[
                "Zat Hara",
                "Pertumbuhan Alga",
                "Oksigen Air",
                "Organisme Air"
            ],
            warna_map={
                "Zat Hara": "#eab308",
                "Pertumbuhan Alga": "#10b981",
                "Oksigen Air": "#0284c7",
                "Organisme Air": "#ef4444"
            },
            judul="Tren Peningkatan Alga dari Waktu ke Waktu",
            ylabel="Nilai Parameter"
        )

        st.dataframe(df_tren, width="stretch", hide_index=True)

        info_card(
            "Status Peningkatan Alga",
            hasil["status_eutrofikasi"],
            "green-card"
            if hasil["indeks_nutrien"] <= 35
            else "yellow-card"
            if hasil["indeks_nutrien"] <= 70
            else "danger-card"
        )

        info_card(
            "Kondisi Ekosistem",
            hasil["kondisi"],
            "green-card"
            if hasil["indeks_nutrien"] <= 35
            else "yellow-card"
            if hasil["indeks_nutrien"] <= 70
            else "danger-card"
        )

    if st.button("Gunakan Simulasi Peningkatan Alga"):
        simpan_hasil_simulasi(
            jenis_simulasi,
            {
                "nitrogen_dari_pupuk": kadar_nitrogen,
                "fosfor_dari_pupuk": kadar_fosfor
            },
            hasil
        )

    if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
        st.success(f"{jenis_simulasi} berhasil dipilih. Silakan lanjut ke halaman Tanggapan Siswa.")
        if st.button("✍️ Lanjut ke Tanggapan Siswa", key="ke_tanggapan_4"):
            st.switch_page("pages/4_Tanggapan_Siswa.py")
