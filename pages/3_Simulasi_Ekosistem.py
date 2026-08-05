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
# ALUR INVESTIGASI GUIDED INQUIRY
# ============================================================

info_card(
    "Alur Penyelidikan",
    """
    Alurnya dibuat sederhana: tulis rumusan masalah dan hipotesis awal, jalankan simulasi,
    catat satu perubahan utama, lalu bandingkan jawabanmu dengan umpan balik ilmiah.
    Setelah itu, kamu dapat melanjutkan ke halaman uji hipotesis dan kesimpulan.
    """,
    "green-card"
)


def tampilkan_materi_pendukung(key_prefix):
    with st.expander("📘 Materi Pendukung untuk Penyelidikan"):
        st.write(
            "Gunakan materi sebagai bahan konsep saat menyusun hipotesis atau ketika menafsirkan data simulasi. "
            "Materi tidak memberikan jawaban langsung, tetapi membantu menjelaskan hubungan antar komponen ekosistem."
        )
        if st.button("Buka Halaman Materi Ekosistem", key=f"buka_materi_{key_prefix}"):
            st.switch_page("pages/2_Materi_Ekosistem.py")


def tampilkan_umpan_balik_setelah_simulasi(
    rumusan_masalah,
    hipotesis_awal,
    hasil_pengamatan,
    urgensi_fenomena,
    contoh_rumusan,
    contoh_hipotesis,
    arahan_rumusan,
    arahan_hipotesis
):
    """Menampilkan umpan balik hanya setelah siswa menjalankan dan menyimpan simulasi."""
    section_title("5. Umpan Balik Setelah Simulasi")

    st.success(
        "Kamu sudah menyusun jawaban awal, menjalankan simulasi, dan mencatat hasil pengamatan. "
        "Umpan balik berikut digunakan sebagai pembanding, bukan untuk menyatakan jawabanmu salah."
    )

    with st.container(border=True):
        st.markdown("#### 📝 Jawaban dan Hasil Pengamatanmu")
        col_rumusan, col_hipotesis = st.columns(2)

        with col_rumusan:
            st.markdown("**Rumusan masalah**")
            st.write(rumusan_masalah)

        with col_hipotesis:
            st.markdown("**Hipotesis awal**")
            st.write(hipotesis_awal)

        st.markdown("**Perubahan utama yang kamu amati**")
        st.write(hasil_pengamatan)

    info_card(
        "Kaitan Fenomena",
        urgensi_fenomena,
        "blue-card"
    )

    col_rumusan, col_hipotesis = st.columns(2)

    with col_rumusan:
        with st.container(border=True):
            st.markdown("#### 🔎 Umpan Balik Rumusan Masalah")
            st.write(arahan_rumusan)
            st.markdown("**Contoh jawaban ilmiah sebagai pembanding:**")
            st.info(contoh_rumusan)

    with col_hipotesis:
        with st.container(border=True):
            st.markdown("#### 💡 Umpan Balik Hipotesis")
            st.write(arahan_hipotesis)
            st.markdown("**Contoh jawaban ilmiah sebagai pembanding:**")
            st.info(contoh_hipotesis)

    st.caption(
        "Contoh tersebut tidak perlu disalin. Gunakan untuk membandingkan kelengkapan jawabanmu "
        "dengan data yang kamu peroleh dari simulasi."
    )


def tampilkan_kasus_awal(
    key_prefix,
    judul_masalah,
    narasi_masalah,
    image_path,
    caption,
    fokus_penyelidikan,
    urgensi_fenomena,
    contoh_rumusan,
    contoh_hipotesis,
    arahan_rumusan,
    arahan_hipotesis,
    pertanyaan_pengamatan
):
    section_title("1. Fenomena Masalah")

    col_gambar, col_masalah = st.columns([1, 1.25])

    with col_gambar:
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            info_card(
                "Gambar Belum Tersedia",
                f"Simpan gambar pada folder: {image_path}",
                "yellow-card"
            )

        st.caption(caption)

    with col_masalah:
        info_card(judul_masalah, narasi_masalah, "blue-card")
        info_card("Fokus Penyelidikan", fokus_penyelidikan, "green-card")
        tampilkan_materi_pendukung(key_prefix)

    section_title("2. Rumusan Masalah dan Hipotesis Awal")

    st.write(
        "Tuliskan rumusan masalah dan hipotesis awal berdasarkan fenomena. "
        "Contoh jawaban belum ditampilkan agar kamu dapat berpikir mandiri terlebih dahulu."
    )

    flag_key = f"jawaban_awal_disimpan_{key_prefix}"
    data_key = f"data_jawaban_awal_{key_prefix}"

    if not st.session_state.get(flag_key, False):
        with st.form(key=f"form_jawaban_awal_{key_prefix}"):
            rumusan_masalah = st.text_area(
                "Rumusan masalah penyelidikan",
                key=f"rumusan_masalah_{key_prefix}",
                height=100,
                placeholder="Tuliskan pertanyaan penyelidikan berdasarkan fenomena yang kamu amati."
            )

            hipotesis_awal = st.text_area(
                "Hipotesis awal",
                key=f"hipotesis_awal_{key_prefix}",
                height=100,
                placeholder="Tuliskan dugaan sementara yang akan kamu uji melalui simulasi."
            )

            submit_awal = st.form_submit_button("Simpan Jawaban Awal dan Mulai Simulasi")

        if submit_awal:
            rumusan_bersih = rumusan_masalah.strip()
            hipotesis_bersih = hipotesis_awal.strip()

            if not rumusan_bersih or not hipotesis_bersih:
                st.error("Rumusan masalah dan hipotesis awal harus diisi.")
            else:
                st.session_state[data_key] = {
                    "rumusan_masalah": rumusan_bersih,
                    "hipotesis_awal": hipotesis_bersih
                }
                st.session_state[flag_key] = True
                st.rerun()

        info_card(
            "Langkah Berikutnya",
            "Setelah kedua jawaban disimpan, simulasi akan terbuka. Umpan balik dan contoh jawaban baru muncul setelah kamu mengamati serta menyimpan hasil simulasi.",
            "yellow-card"
        )

        return {
            "rumusan_masalah": "",
            "hipotesis_awal": ""
        }, False, {
            "urgensi_fenomena": urgensi_fenomena,
            "contoh_rumusan": contoh_rumusan,
            "contoh_hipotesis": contoh_hipotesis,
            "arahan_rumusan": arahan_rumusan,
            "arahan_hipotesis": arahan_hipotesis,
            "pertanyaan_pengamatan": pertanyaan_pengamatan
        }

    investigasi = st.session_state.get(data_key, {})

    st.success(
        "Jawaban awalmu sudah tersimpan. Sekarang jalankan simulasi untuk mencari data yang dapat menguji dugaanmu."
    )

    with st.expander("Lihat Jawaban Awal", expanded=False):
        st.markdown("**Rumusan masalah**")
        st.write(investigasi.get("rumusan_masalah", ""))
        st.markdown("**Hipotesis awal**")
        st.write(investigasi.get("hipotesis_awal", ""))

    if st.button("Ubah Jawaban Awal", key=f"ubah_jawaban_awal_{key_prefix}"):
        st.session_state.pop(flag_key, None)
        st.session_state.pop(data_key, None)
        st.session_state.pop("hasil_simulasi", None)
        st.session_state.pop("simulasi_tersimpan", None)
        st.rerun()

    return investigasi, True, {
        "urgensi_fenomena": urgensi_fenomena,
        "contoh_rumusan": contoh_rumusan,
        "contoh_hipotesis": contoh_hipotesis,
        "arahan_rumusan": arahan_rumusan,
        "arahan_hipotesis": arahan_hipotesis,
        "pertanyaan_pengamatan": pertanyaan_pengamatan
    }


def tampilkan_hasil_pengamatan_singkat(key_prefix, pertanyaan):
    section_title("4. Hasil Pengamatan Singkat")
    st.write(
        "Setelah mencoba beberapa kondisi, tuliskan satu perubahan utama yang kamu lihat pada data atau grafik."
    )
    return st.text_area(
        pertanyaan,
        key=f"hasil_pengamatan_{key_prefix}",
        height=100,
        placeholder="Tuliskan perubahan utama berdasarkan data simulasi, bukan berdasarkan perkiraan."
    )

def tampilkan_arahan_pengumpulan_data():
    info_card(
        "3. Simulasi dan Pengumpulan Data",
        """
        Ubah variabel simulasi beberapa kali untuk melihat pola perubahan data. Bandingkan kondisi rendah,
        sedang, dan tinggi jika memungkinkan. Setelah menemukan data yang paling relevan dengan hipotesismu,
        simpan hasil simulasi untuk digunakan pada tahap uji hipotesis.
        """,
        "green-card"
    )


def tampilkan_arahan_analisis():
    info_card(
        "Baca Pola Data",
        """
        Perhatikan parameter yang naik, parameter yang turun, serta hubungan antara variabel yang kamu ubah
        dengan kondisi ekosistem. Gunakan data ini sebagai bukti saat menguji hipotesis pada halaman tanggapan.
        """,
        "yellow-card"
    )


def tampilkan_grafik_batang(df, x_col, y_col, judul, ylabel="Nilai"):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{x_col}:N", axis=alt.Axis(title=x_col, labelAngle=0)),
        y=alt.Y(f"{y_col}:Q", axis=alt.Axis(title=ylabel)),
        tooltip=[
            alt.Tooltip(f"{x_col}:N", title=x_col),
            alt.Tooltip(f"{y_col}:Q", title=ylabel, format=",.2f")
        ]
    ).properties(
        title=alt.TitleParams(text=judul, fontSize=14, fontWeight="bold", anchor="start"),
        height=320,
        background="#ffffff"
    ).configure_view(stroke=None)

    st.altair_chart(chart, use_container_width=True)


def payload_investigasi(investigasi, data_variabel, hasil_pengamatan):
    payload = {
        "rumusan_masalah": investigasi.get("rumusan_masalah", ""),
        "hipotesis_awal": investigasi.get("hipotesis_awal", ""),
        "hasil_pengamatan_siswa": hasil_pengamatan.strip()
    }
    payload.update(data_variabel)
    return payload


# ============================================================
# TAB SIMULASI
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Pencemaran Sungai",
    "2. Rantai Makanan",
    "3. Daur Air, CO2, dan O2",
    "4. Peningkatan Alga"
])


# ============================================================
# TAB 1: PENCEMARAN SUNGAI
# ============================================================

with tab1:
    jenis_simulasi = "Pencemaran Sungai Akibat Limbah Pabrik"
    section_title("Investigasi Pencemaran Sungai Akibat Limbah Pabrik")

    investigasi, siap, umpan_balik = tampilkan_kasus_awal(
        key_prefix="pencemaran",
        judul_masalah="Masalah Ekosistem Sungai",
        narasi_masalah="""
        Sebuah sungai menerima limbah dari aktivitas industri. Setelah beberapa waktu, air tampak berubah,
        organisme kecil berkurang, dan jumlah ikan mulai menurun. Kondisi ini menunjukkan adanya perubahan
        pada komponen abiotik dan biotik di ekosistem perairan.
        """,
        image_path=os.path.join("assets", "images", "pencemaran_sungai.jpg"),
        caption="Fenomena pencemaran sungai digunakan sebagai konteks awal penyelidikan.",
        fokus_penyelidikan="Selidiki hubungan antara tingkat limbah industri, kualitas air, oksigen terlarut, dan kondisi organisme air.",
        urgensi_fenomena="Limbah industri dapat mengubah kualitas air dan kadar oksigen terlarut. Perubahan pada komponen abiotik tersebut berpotensi memengaruhi organisme kecil dan ikan. Oleh karena itu, hubungan antara tingkat limbah dan kondisi ekosistem sungai perlu diselidiki melalui data simulasi.",
        contoh_rumusan="Bagaimana peningkatan tingkat limbah industri memengaruhi kualitas air, oksigen terlarut, dan kondisi organisme di ekosistem sungai?",
        contoh_hipotesis="Jika tingkat limbah industri meningkat, maka kualitas air dan oksigen terlarut diperkirakan menurun sehingga kondisi organisme air dapat terganggu.",
        arahan_rumusan="Jawabanmu sudah menjadi bagian dari proses penyelidikan. Agar lebih terarah, rumusan masalah dapat menghubungkan tingkat limbah sebagai faktor penyebab dengan perubahan kualitas air, oksigen terlarut, dan organisme air.",
        arahan_hipotesis="Hipotesismu dapat dikembangkan dengan menunjukkan dugaan hubungan sebab-akibat. Gunakan kata seperti ‘jika’, ‘maka’, atau ‘diperkirakan’ karena dugaan tersebut masih perlu dibuktikan melalui data.",
        pertanyaan_pengamatan="Apa perubahan utama pada kualitas air, oksigen terlarut, atau organisme ketika tingkat limbah diubah?"
    )

    if siap:
        tampilkan_arahan_pengumpulan_data()

        col_kiri, col_kanan = st.columns([1, 1.35])

        with col_kiri:
            st.subheader("Ubah Variabel")
            tingkat_limbah = st.slider(
                "Tingkat Limbah Industri",
                min_value=0.0,
                max_value=1.0,
                value=0.50,
                step=0.01,
                key="slider_limbah_final"
            )
            st.caption("Coba beberapa kondisi sebelum menyimpan hasil: rendah, sedang, dan tinggi.")

        with col_kanan:
            hasil = hitung_pencemaran_sungai(tingkat_limbah)
            df_tren = pd.DataFrame(buat_tren_pencemaran_sungai(tingkat_limbah))

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

        hasil_pengamatan = tampilkan_hasil_pengamatan_singkat(
            "pencemaran",
            umpan_balik["pertanyaan_pengamatan"]
        )
        hasil_pengamatan_bersih = hasil_pengamatan.strip()

        if st.button("Simpan Hasil Pengamatan", key="simpan_pencemaran_final"):
            if not hasil_pengamatan_bersih:
                st.warning("Tuliskan satu perubahan utama yang kamu amati sebelum menyimpan hasil.")
            else:
                simpan_hasil_simulasi(
                    jenis_simulasi,
                    payload_investigasi(
                        investigasi,
                        {
                            "tingkat_limbah_industri": tingkat_limbah,
                            "indeks_limbah": hasil["indeks_limbah"],
                            "tingkat_pencemaran": hasil["tingkat_pencemaran"]
                        },
                        hasil_pengamatan_bersih
                    ),
                    hasil
                )

        if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
            st.success(f"{jenis_simulasi} berhasil disimpan.")
            tampilkan_umpan_balik_setelah_simulasi(
                rumusan_masalah=investigasi["rumusan_masalah"],
                hipotesis_awal=investigasi["hipotesis_awal"],
                hasil_pengamatan=hasil_pengamatan_bersih,
                urgensi_fenomena=umpan_balik["urgensi_fenomena"],
                contoh_rumusan=umpan_balik["contoh_rumusan"],
                contoh_hipotesis=umpan_balik["contoh_hipotesis"],
                arahan_rumusan=umpan_balik["arahan_rumusan"],
                arahan_hipotesis=umpan_balik["arahan_hipotesis"]
            )
            if st.button("✍️ Lanjut ke Uji Hipotesis", key="ke_tanggapan_1_final"):
                st.switch_page("pages/4_Tanggapan_Siswa.py")


# ============================================================
# TAB 2: RANTAI MAKANAN
# ============================================================

with tab2:
    jenis_simulasi = "Rantai Makanan Saat Kemarau"
    section_title("Investigasi Rantai Makanan Saat Kemarau")

    investigasi, siap, umpan_balik = tampilkan_kasus_awal(
        key_prefix="rantai",
        judul_masalah="Masalah Ketersediaan Produsen Saat Kemarau",
        narasi_masalah="""
        Pada musim kemarau panjang, pertumbuhan rumput di suatu ekosistem padang rumput menurun.
        Rumput berperan sebagai produsen yang menjadi sumber energi bagi konsumen. Perubahan pada produsen
        dapat memengaruhi aliran energi pada tingkat trofik berikutnya.
        """,
        image_path=os.path.join("assets", "images", "rantai_makanan_piramida_energi.png"),
        caption="Piramida energi digunakan untuk membantu membaca aliran energi antar tingkat trofik.",
        fokus_penyelidikan="Selidiki pengaruh berkurangnya produsen dan efisiensi transfer energi terhadap energi pada tiap tingkat trofik.",
        urgensi_fenomena="Rumput merupakan produsen dan sumber awal energi dalam rantai makanan. Ketika musim kemarau menyebabkan jumlah rumput berkurang, energi yang tersedia bagi konsumen tingkat I, II, dan III juga dapat berubah. Hubungan antara ketersediaan produsen dan aliran energi perlu diselidiki melalui data simulasi.",
        contoh_rumusan="Bagaimana berkurangnya rumput akibat musim kemarau dan efisiensi transfer energi memengaruhi jumlah energi pada setiap tingkat trofik?",
        contoh_hipotesis="Jika jumlah rumput berkurang akibat musim kemarau, maka energi yang tersedia bagi konsumen diperkirakan ikut menurun. Semakin tinggi tingkat trofik, energi yang diterima diperkirakan semakin sedikit.",
        arahan_rumusan="Jawabanmu sudah mengarah pada fenomena rantai makanan. Agar lebih terukur, rumusan masalah dapat menyebutkan perubahan jumlah rumput, efisiensi transfer, dan energi pada setiap tingkat trofik.",
        arahan_hipotesis="Hipotesismu dapat dikembangkan dengan menjelaskan akibat berkurangnya sumber energi pada produsen terhadap konsumen, termasuk pola energi yang semakin sedikit pada tingkat trofik yang lebih tinggi.",
        pertanyaan_pengamatan="Apa perubahan utama pada energi produsen dan konsumen ketika jumlah rumput atau efisiensi transfer diubah?"
    )

    if siap:
        tampilkan_arahan_pengumpulan_data()

        col_kiri, col_kanan = st.columns([1, 1.35])

        with col_kiri:
            st.subheader("Ubah Variabel")
            energi_produsen_normal = st.number_input(
                "Energi produsen sebelum kemarau (kkal)",
                min_value=100,
                max_value=100000,
                value=10000,
                step=100,
                key="energi_produsen_final"
            )
            penurunan_produsen = st.slider(
                "Rumput yang berkurang akibat kemarau (%)",
                min_value=0,
                max_value=90,
                value=30,
                key="penurunan_produsen_final"
            )
            efisiensi_transfer = st.slider(
                "Energi yang berpindah ke makhluk hidup berikutnya (%)",
                min_value=5,
                max_value=30,
                value=10,
                key="efisiensi_transfer_final"
            )
            st.caption("Coba ubah penurunan produsen dan efisiensi transfer untuk melihat perubahan energi.")

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

        hasil_pengamatan = tampilkan_hasil_pengamatan_singkat(
            "rantai",
            umpan_balik["pertanyaan_pengamatan"]
        )
        hasil_pengamatan_bersih = hasil_pengamatan.strip()

        if st.button("Simpan Hasil Pengamatan", key="simpan_rantai_final"):
            if not hasil_pengamatan_bersih:
                st.warning("Tuliskan satu perubahan utama yang kamu amati sebelum menyimpan hasil.")
            else:
                simpan_hasil_simulasi(
                    jenis_simulasi,
                    payload_investigasi(
                        investigasi,
                        {
                            "energi_produsen_normal": energi_produsen_normal,
                            "rumput_berkurang_akibat_kemarau": penurunan_produsen,
                            "energi_produsen_setelah_kemarau": energi_awal,
                            "efisiensi_transfer_energi": efisiensi_transfer
                        },
                        hasil_pengamatan_bersih
                    ),
                    hasil
                )

        if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
            st.success(f"{jenis_simulasi} berhasil disimpan.")
            tampilkan_umpan_balik_setelah_simulasi(
                rumusan_masalah=investigasi["rumusan_masalah"],
                hipotesis_awal=investigasi["hipotesis_awal"],
                hasil_pengamatan=hasil_pengamatan_bersih,
                urgensi_fenomena=umpan_balik["urgensi_fenomena"],
                contoh_rumusan=umpan_balik["contoh_rumusan"],
                contoh_hipotesis=umpan_balik["contoh_hipotesis"],
                arahan_rumusan=umpan_balik["arahan_rumusan"],
                arahan_hipotesis=umpan_balik["arahan_hipotesis"]
            )
            if st.button("✍️ Lanjut ke Uji Hipotesis", key="ke_tanggapan_2_final"):
                st.switch_page("pages/4_Tanggapan_Siswa.py")


# ============================================================
# TAB 3: DAUR AIR, CO2, DAN O2
# ============================================================

with tab3:
    jenis_simulasi = "Daur Air, Karbon Dioksida, dan Oksigen Saat Pohon Berkurang"
    section_title("Investigasi Daur Air, CO2, dan O2 Saat Pohon Berkurang")

    investigasi, siap, umpan_balik = tampilkan_kasus_awal(
        key_prefix="daur_air",
        judul_masalah="Masalah Berkurangnya Tutupan Vegetasi",
        narasi_masalah="""
        Penebangan pohon mengurangi tutupan vegetasi di suatu wilayah. Kondisi ini dapat memengaruhi
        penyerapan air hujan ke dalam tanah, limpasan permukaan, penyerapan karbon dioksida, dan produksi oksigen.
        Perubahan tersebut menunjukkan keterkaitan antara tumbuhan, air, dan gas di atmosfer.
        """,
        image_path=os.path.join("assets", "images", "diagram_daur_air_co2_o2.png"),
        caption="Diagram daur air, CO2, dan O2 digunakan sebagai konteks awal penyelidikan.",
        fokus_penyelidikan="Selidiki pengaruh tutupan vegetasi terhadap infiltrasi, limpasan permukaan, penyerapan CO2, dan produksi O2.",
        urgensi_fenomena="Tumbuhan membantu air hujan meresap ke tanah melalui akar, menyerap karbon dioksida, dan menghasilkan oksigen. Ketika tutupan vegetasi berkurang, keseimbangan air dan gas di lingkungan dapat berubah. Dampak tersebut perlu diselidiki melalui beberapa kondisi simulasi.",
        contoh_rumusan="Bagaimana berkurangnya tutupan vegetasi setelah penebangan memengaruhi infiltrasi air, limpasan permukaan, penyerapan CO2, dan produksi O2?",
        contoh_hipotesis="Jika tutupan vegetasi berkurang, maka infiltrasi air, penyerapan CO2, dan produksi O2 diperkirakan menurun, sedangkan limpasan permukaan diperkirakan meningkat.",
        arahan_rumusan="Jawabanmu sudah menjadi awal penyelidikan. Agar sesuai dengan variabel simulasi, rumusan masalah dapat menghubungkan tutupan vegetasi dan curah hujan dengan infiltrasi, limpasan, penyerapan CO2, serta produksi O2.",
        arahan_hipotesis="Hipotesismu dapat dikembangkan dengan menjelaskan arah perubahan setiap parameter saat vegetasi berkurang, tanpa menganggap hasilnya sudah pasti sebelum simulasi dilakukan.",
        pertanyaan_pengamatan="Apa perubahan utama pada infiltrasi, limpasan, CO2, atau O2 ketika tutupan vegetasi diubah?"
    )

    if siap:
        tampilkan_arahan_pengumpulan_data()

        col_kiri, col_kanan = st.columns([1, 1.35])

        with col_kiri:
            st.subheader("Ubah Variabel")
            intensitas_panas = 60
            curah_hujan = st.slider(
                "Curah Hujan",
                min_value=0,
                max_value=100,
                value=70,
                key="curah_hujan_final"
            )
            tutupan_vegetasi = st.slider(
                "Tutupan Vegetasi Setelah Penebangan",
                min_value=0,
                max_value=100,
                value=50,
                key="tutupan_vegetasi_final"
            )
            st.caption("Intensitas panas matahari dibuat tetap agar penyelidikan lebih fokus.")

        with col_kanan:
            hasil = hitung_daur_air(
                curah_hujan=curah_hujan,
                tutupan_vegetasi=tutupan_vegetasi,
                intensitas_panas=intensitas_panas
            )
            df_tren_air = pd.DataFrame(buat_tren_daur_air(
                curah_hujan=curah_hujan,
                tutupan_vegetasi_akhir=tutupan_vegetasi,
                intensitas_panas=intensitas_panas
            ))

            st.markdown("### Hasil Pengamatan")
            status_daur_air_card(hasil)

            info_card(
                "Petunjuk Pengamatan",
                """
                Bandingkan nilai infiltrasi dan limpasan permukaan pada beberapa tingkat tutupan vegetasi.
                Amati juga perubahan penyerapan CO2 dan produksi O2 sebelum menuliskan hasil pengamatanmu.
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
                "Bandingkan arah perubahan infiltrasi dan limpasan permukaan saat tutupan vegetasi diubah."
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
                "Amati arah perubahan CO2 yang diserap dan O2 yang dihasilkan saat tutupan vegetasi diubah."
            )

        with st.expander("📊 Lihat Data Lengkap Simulasi"):
            st.dataframe(
                df_tren_air,
                width="stretch",
                hide_index=True
            )

        hasil_pengamatan = tampilkan_hasil_pengamatan_singkat(
            "daur_air",
            umpan_balik["pertanyaan_pengamatan"]
        )
        hasil_pengamatan_bersih = hasil_pengamatan.strip()

        if st.button("Simpan Hasil Pengamatan", key="simpan_daur_air_final"):
            if not hasil_pengamatan_bersih:
                st.warning("Tuliskan satu perubahan utama yang kamu amati sebelum menyimpan hasil.")
            else:
                simpan_hasil_simulasi(
                    jenis_simulasi,
                    payload_investigasi(
                        investigasi,
                        {
                            "curah_hujan": curah_hujan,
                            "tutupan_vegetasi_setelah_penebangan": tutupan_vegetasi,
                            "panas_matahari_tetap": intensitas_panas
                        },
                        hasil_pengamatan_bersih
                    ),
                    hasil
                )

        if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
            st.success(f"{jenis_simulasi} berhasil disimpan.")
            tampilkan_umpan_balik_setelah_simulasi(
                rumusan_masalah=investigasi["rumusan_masalah"],
                hipotesis_awal=investigasi["hipotesis_awal"],
                hasil_pengamatan=hasil_pengamatan_bersih,
                urgensi_fenomena=umpan_balik["urgensi_fenomena"],
                contoh_rumusan=umpan_balik["contoh_rumusan"],
                contoh_hipotesis=umpan_balik["contoh_hipotesis"],
                arahan_rumusan=umpan_balik["arahan_rumusan"],
                arahan_hipotesis=umpan_balik["arahan_hipotesis"]
            )
            if st.button("✍️ Lanjut ke Uji Hipotesis", key="ke_tanggapan_3_final"):
                st.switch_page("pages/4_Tanggapan_Siswa.py")


# ============================================================
# TAB 4: PENINGKATAN ALGA
# ============================================================

with tab4:
    jenis_simulasi = "Peningkatan Alga Akibat Pupuk Berlebih"
    section_title("Investigasi Peningkatan Alga Akibat Pupuk Berlebih")

    investigasi, siap, umpan_balik = tampilkan_kasus_awal(
        key_prefix="alga",
        judul_masalah="Masalah Pupuk Berlebih di Perairan",
        narasi_masalah="""
        Pupuk pertanian yang digunakan berlebihan dapat terbawa air hujan menuju sungai atau danau.
        Pupuk mengandung nitrogen dan fosfor. Jika zat hara masuk ke perairan dalam jumlah tinggi,
        pertumbuhan alga dapat meningkat dan mengubah kondisi organisme air.
        """,
        image_path=os.path.join("assets", "images", "peningkatan_alga_akibat_pupuk_berlebih.png"),
        caption="Fenomena peningkatan alga digunakan sebagai konteks awal penyelidikan eutrofikasi.",
        fokus_penyelidikan="Selidiki pengaruh nitrogen dan fosfor terhadap pertumbuhan alga, oksigen air, dan kondisi organisme air.",
        urgensi_fenomena="Pupuk yang terbawa air hujan dapat membawa nitrogen dan fosfor ke perairan. Jika zat hara terlalu tinggi, pertumbuhan alga dapat meningkat dan mengubah ketersediaan oksigen serta kondisi organisme air. Hubungan antartahap tersebut perlu diselidiki melalui data simulasi.",
        contoh_rumusan="Bagaimana peningkatan kadar nitrogen dan fosfor dari pupuk memengaruhi pertumbuhan alga, oksigen dalam air, dan kondisi organisme perairan?",
        contoh_hipotesis="Jika kadar nitrogen dan fosfor dalam perairan meningkat, maka pertumbuhan alga diperkirakan meningkat. Kondisi tersebut dapat menurunkan oksigen dalam air dan mengganggu organisme perairan.",
        arahan_rumusan="Jawabanmu sudah berhubungan dengan fenomena peningkatan alga. Agar lebih terarah, rumusan masalah dapat menyebutkan nitrogen dan fosfor sebagai faktor yang diuji serta alga, oksigen, dan organisme sebagai parameter yang diamati.",
        arahan_hipotesis="Hipotesismu dapat dikembangkan dengan menjelaskan urutan sebab-akibat dari zat hara menuju pertumbuhan alga, perubahan oksigen, lalu kondisi organisme air.",
        pertanyaan_pengamatan="Apa perubahan utama pada alga, oksigen air, atau organisme ketika kadar nitrogen dan fosfor diubah?"
    )

    if siap:
        tampilkan_arahan_pengumpulan_data()

        col_kiri, col_kanan = st.columns([1, 1.35])

        with col_kiri:
            st.subheader("Ubah Variabel")
            kadar_nitrogen = st.slider(
                "Nitrogen dari Pupuk",
                min_value=0,
                max_value=100,
                value=50,
                key="nitrogen_final"
            )
            kadar_fosfor = st.slider(
                "Fosfor dari Pupuk",
                min_value=0,
                max_value=100,
                value=50,
                key="fosfor_final"
            )
            st.caption("Coba ubah nitrogen dan fosfor untuk melihat respons alga dan organisme air.")

        with col_kanan:
            hasil = hitung_eutrofikasi(kadar_nitrogen, kadar_fosfor)
            df_tren = pd.DataFrame(buat_tren_eutrofikasi(kadar_nitrogen, kadar_fosfor))

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

        hasil_pengamatan = tampilkan_hasil_pengamatan_singkat(
            "alga",
            umpan_balik["pertanyaan_pengamatan"]
        )
        hasil_pengamatan_bersih = hasil_pengamatan.strip()

        if st.button("Simpan Hasil Pengamatan", key="simpan_alga_final"):
            if not hasil_pengamatan_bersih:
                st.warning("Tuliskan satu perubahan utama yang kamu amati sebelum menyimpan hasil.")
            else:
                simpan_hasil_simulasi(
                    jenis_simulasi,
                    payload_investigasi(
                        investigasi,
                        {
                            "nitrogen_dari_pupuk": kadar_nitrogen,
                            "fosfor_dari_pupuk": kadar_fosfor,
                            "indeks_nutrien": hasil["indeks_nutrien"]
                        },
                        hasil_pengamatan_bersih
                    ),
                    hasil
                )

        if st.session_state.get("simulasi_tersimpan") == jenis_simulasi:
            st.success(f"{jenis_simulasi} berhasil disimpan.")
            tampilkan_umpan_balik_setelah_simulasi(
                rumusan_masalah=investigasi["rumusan_masalah"],
                hipotesis_awal=investigasi["hipotesis_awal"],
                hasil_pengamatan=hasil_pengamatan_bersih,
                urgensi_fenomena=umpan_balik["urgensi_fenomena"],
                contoh_rumusan=umpan_balik["contoh_rumusan"],
                contoh_hipotesis=umpan_balik["contoh_hipotesis"],
                arahan_rumusan=umpan_balik["arahan_rumusan"],
                arahan_hipotesis=umpan_balik["arahan_hipotesis"]
            )
            if st.button("✍️ Lanjut ke Uji Hipotesis", key="ke_tanggapan_4_final"):
                st.switch_page("pages/4_Tanggapan_Siswa.py")
