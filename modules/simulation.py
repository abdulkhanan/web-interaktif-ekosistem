"""
Modul perhitungan simulasi ekosistem.

Catatan:
1. Semua simulasi memakai model indeks edukatif.
2. Nilai output utama berada pada skala 0 sampai 100.
3. Nilai DO pada simulasi pencemaran sungai tetap ditampilkan dalam mg/L.
4. Angka koefisien digunakan sebagai asumsi model pembelajaran, bukan hasil ukur laboratorium.
"""


def _batasi_indeks(nilai):
    """Membatasi nilai agar berada pada rentang 0 sampai 100."""
    return max(0, min(100, float(nilai)))


def _normalisasi_0_1(nilai):
    """
    Mengubah input menjadi skala 0 sampai 1.
    Jika nilai lebih dari 1, sistem menganggap input memakai skala 0 sampai 100.
    """
    nilai = float(nilai)

    if nilai > 1:
        nilai = nilai / 100

    return max(0, min(1, nilai))


# ============================================================
# 1. SIMULASI PENCEMARAN SUNGAI
# ============================================================

def hitung_pencemaran_sungai(tingkat_limbah):
    """
    Menghitung dampak limbah industri terhadap ekosistem sungai.

    L = tingkat limbah industri pada skala 0 sampai 1.
    DOmaks = 8,5 mg/L sebagai asumsi DO pada kondisi air baik.
    DOmin = 2,0 mg/L sebagai asumsi DO pada kondisi pencemaran tinggi.
    Angka 6,5 berasal dari 8,5 - 2,0.

    Rumus:
    Indeks Limbah = L x 100
    Kualitas Air = 100 x (1 - L)
    DO = 8,5 - ((8,5 - 2,0) x L)
    Indeks DO = (DO / 8,5) x 100
    Populasi Ikan = 100 - (90 x L)
    Indeks Invertebrata = 100 - (80 x L)
    """
    L = _normalisasi_0_1(tingkat_limbah)

    do_maks = 8.5
    do_min = 2.0
    koefisien_penurunan_do = do_maks - do_min

    indeks_limbah = L * 100
    kualitas_air = 100 * (1 - L)

    nilai_do = do_maks - (koefisien_penurunan_do * L)
    nilai_do = max(do_min, nilai_do)

    indeks_do = (nilai_do / do_maks) * 100

    populasi_ikan = 100 - (L * 90)
    makroinvertebrata = 100 - (L * 80)

    if indeks_limbah <= 30:
        status_limbah = "Rendah"
    elif indeks_limbah <= 70:
        status_limbah = "Sedang"
    else:
        status_limbah = "Tinggi"

    if nilai_do >= 6:
        status_do = "Normal"
    elif nilai_do >= 3:
        status_do = "Menurun"
    else:
        status_do = "Rendah"

    if populasi_ikan >= 70:
        status_ikan = "Stabil"
    elif populasi_ikan >= 40:
        status_ikan = "Menurun"
    else:
        status_ikan = "Kritis"

    if indeks_limbah <= 30:
        kondisi = "Ekosistem relatif stabil."
    elif indeks_limbah <= 70:
        kondisi = "Ekosistem mulai terganggu."
    else:
        kondisi = "Ekosistem mengalami gangguan berat."

    return {
        "tingkat_pencemaran": round(indeks_limbah, 2),
        "tingkat_limbah": round(L, 2),
        "status_limbah": status_limbah,
        "indeks_limbah": round(indeks_limbah, 2),

        # Nama lama dipertahankan agar kode lama tidak error.
        "konsentrasi_limbah_ppm": round(indeks_limbah, 2),

        "nilai_do": round(nilai_do, 2),
        "indeks_do": round(indeks_do, 2),
        "status_do": status_do,
        "kualitas_air": round(kualitas_air, 2),
        "makroinvertebrata": round(makroinvertebrata, 2),
        "populasi_ikan": round(populasi_ikan, 2),
        "status_populasi_ikan": status_ikan,
        "kondisi": kondisi,
    }


def buat_tren_pencemaran_sungai(tingkat_limbah):
    """
    Membuat tren pencemaran sungai dari hari ke-0 sampai hari ke-30.
    Jika limbah akhir 0, semua indikator yang terdampak limbah tetap dimulai dari kondisi baik.
    """
    L_akhir = _normalisasi_0_1(tingkat_limbah)
    waktu = [0, 5, 10, 15, 20, 25, 30]
    data = []

    for hari in waktu:
        faktor_waktu = hari / 30
        L_saat_ini = L_akhir * faktor_waktu
        hasil = hitung_pencemaran_sungai(L_saat_ini)

        data.append({
            "Waktu (hari)": hari,
            "Indeks Limbah": hasil["indeks_limbah"],
            "Kualitas Air": hasil["kualitas_air"],
            "Indeks DO": hasil["indeks_do"],
            "DO (mg/L)": hasil["nilai_do"],
            "Populasi Ikan": hasil["populasi_ikan"],
            "Indeks Invertebrata": hasil["makroinvertebrata"],

            # Nama lama dipertahankan agar kode lama tidak error.
            "Konsentrasi Limbah (ppm)": hasil["indeks_limbah"],
            "Oksigen Terlarut (DO)": hasil["indeks_do"]
        })

    return data


# ============================================================
# 2. SIMULASI RANTAI MAKANAN
# ============================================================

def hitung_aliran_energi(energi_awal, efisiensi_transfer):
    """
    Menghitung aliran energi pada rantai makanan.

    Rumus:
    r = efisiensi_transfer / 100
    Konsumen I = Produsen x r
    Konsumen II = Konsumen I x r
    Konsumen III = Konsumen II x r
    """
    produsen = max(0, float(energi_awal))
    r = max(0, min(1, float(efisiensi_transfer) / 100))

    konsumen_1 = produsen * r
    konsumen_2 = konsumen_1 * r
    konsumen_3 = konsumen_2 * r

    return {
        "produsen": round(produsen, 2),
        "konsumen_1": round(konsumen_1, 2),
        "konsumen_2": round(konsumen_2, 2),
        "konsumen_3": round(konsumen_3, 2),
        "efisiensi_transfer_desimal": round(r, 4),
        "keterangan": (
            "Energi berkurang pada setiap tingkat trofik karena hanya sebagian energi "
            "yang berpindah ke tingkat berikutnya. Sebagian energi digunakan untuk aktivitas hidup "
            "dan sebagian hilang sebagai panas."
        ),
    }


# ============================================================
# 3. SIMULASI DAUR AIR, CO2, DAN O2
# ============================================================

def hitung_daur_air(curah_hujan, tutupan_vegetasi, intensitas_panas=60):
    """
    Menghitung dampak curah hujan dan tutupan vegetasi terhadap:
    1. daur air,
    2. penyerapan karbon dioksida,
    3. produksi oksigen.

    Variabel yang diubah siswa:
    P = curah hujan, skala 0 sampai 100
    V = tutupan vegetasi setelah penebangan, skala 0 sampai 1

    Variabel tetap:
    H = intensitas panas matahari, dibuat tetap 60

    Rumus:
    Evaporasi = min(100, (H x 0,70) + (P x 0,30))
    Presipitasi = P
    Infiltrasi = P x (0,30 + 0,70V)
    Limpasan Permukaan = P - Infiltrasi
    CO2 Diserap = V x 100
    O2 Dihasilkan = V x 90
    """

    H = _batasi_indeks(intensitas_panas)
    P = _batasi_indeks(curah_hujan)

    vegetasi_indeks = _batasi_indeks(tutupan_vegetasi)
    V = vegetasi_indeks / 100

    evaporasi = _batasi_indeks((H * 0.70) + (P * 0.30))
    presipitasi = P

    infiltrasi = _batasi_indeks(P * (0.30 + (0.70 * V)))
    limpasan_permukaan = _batasi_indeks(P - infiltrasi)

    penyerapan_karbon_dioksida = _batasi_indeks(V * 100)
    produksi_oksigen = _batasi_indeks(V * 90)

    co2_tidak_terserap = _batasi_indeks(100 - penyerapan_karbon_dioksida)

    if vegetasi_indeks >= 70:
        status = "Baik"
        keterangan = (
            "Tutupan vegetasi masih tinggi. Air hujan lebih banyak meresap ke tanah, "
            "limpasan permukaan rendah, tumbuhan menyerap CO2 lebih banyak, "
            "dan produksi O2 juga tinggi."
        )
    elif vegetasi_indeks >= 40:
        status = "Cukup"
        keterangan = (
            "Tutupan vegetasi berada pada tingkat sedang. Sebagian air masih meresap ke tanah, "
            "tetapi limpasan permukaan mulai meningkat. Penyerapan CO2 dan produksi O2 mulai menurun."
        )
    else:
        status = "Terganggu"
        keterangan = (
            "Tutupan vegetasi rendah. Air hujan lebih banyak mengalir di permukaan, "
            "infiltrasi menurun, limpasan meningkat, penyerapan CO2 rendah, "
            "dan produksi O2 juga berkurang."
        )

    return {
        "intensitas_panas": round(H, 2),
        "curah_hujan": round(P, 2),
        "tutupan_vegetasi": round(vegetasi_indeks, 2),

        "evaporasi": round(evaporasi, 2),
        "presipitasi": round(presipitasi, 2),
        "infiltrasi": round(infiltrasi, 2),
        "limpasan_permukaan": round(limpasan_permukaan, 2),

        "penyerapan_karbon_dioksida": round(penyerapan_karbon_dioksida, 2),
        "co2_tidak_terserap": round(co2_tidak_terserap, 2),
        "produksi_oksigen": round(produksi_oksigen, 2),

        "status": status,
        "keterangan": keterangan,

    }


def buat_tren_daur_air(curah_hujan, tutupan_vegetasi_akhir, intensitas_panas=60):
    """
    Membuat tren daur air, CO2, dan O2 dari hari ke-0 sampai hari ke-30.

    Tutupan vegetasi diasumsikan turun bertahap dari 100 menuju nilai akhir
    yang dipilih siswa pada slider.
    """

    waktu = [0, 5, 10, 15, 20, 25, 30]
    vegetasi_awal = 100
    vegetasi_akhir = _batasi_indeks(tutupan_vegetasi_akhir)

    data = []

    for hari in waktu:
        faktor_waktu = hari / 30

        vegetasi_saat_ini = vegetasi_awal - (
            (vegetasi_awal - vegetasi_akhir) * faktor_waktu
        )

        hasil = hitung_daur_air(
            curah_hujan=curah_hujan,
            tutupan_vegetasi=vegetasi_saat_ini,
            intensitas_panas=intensitas_panas
        )

        data.append({
            "Waktu (hari)": hari,
            "Tutupan Vegetasi": round(vegetasi_saat_ini, 2),
            "Infiltrasi": hasil["infiltrasi"],
            "Limpasan Permukaan": hasil["limpasan_permukaan"],
            "CO2 Diserap": hasil["penyerapan_karbon_dioksida"],
            "CO2 Tidak Terserap": hasil["co2_tidak_terserap"],
            "O2 Dihasilkan": hasil["produksi_oksigen"],
            "Evaporasi": hasil["evaporasi"],
            "Presipitasi": hasil["presipitasi"]
        })

    return data

# Fungsi lama dipertahankan agar kode lain yang memanggil hitung_simulasi tetap berjalan.
def hitung_simulasi(tingkat_pencemaran):
    return hitung_pencemaran_sungai(tingkat_pencemaran)


# ============================================================
# 4. SIMULASI PENINGKATAN ALGA
# ============================================================

def hitung_eutrofikasi(kadar_nitrogen, kadar_fosfor):
    """
    Menghitung dampak nitrogen dan fosfor terhadap pertumbuhan alga.

    Rumus:
    Indeks Nutrien = (N + P) / 2
    Pertumbuhan Alga = Indeks Nutrien
    Oksigen Air = 100 - (Pertumbuhan Alga x 0,75)
    Organisme Air = 100 - (Pertumbuhan Alga x 0,90)
    """
    N = _batasi_indeks(kadar_nitrogen)
    P = _batasi_indeks(kadar_fosfor)

    indeks_nutrien = (N + P) / 2
    pertumbuhan_alga = indeks_nutrien

    indeks_oksigen_air = _batasi_indeks(100 - (pertumbuhan_alga * 0.75))

    # Dibuat berbeda dari oksigen air agar kurva organisme tidak tertutup kurva oksigen.
    kondisi_organisme = _batasi_indeks(100 - (pertumbuhan_alga * 0.90))

    if indeks_nutrien <= 35:
        status_eutrofikasi = "Rendah"
        status_alga = "Normal"
        status_do = "Normal"
        kondisi = (
            "Kondisi perairan relatif stabil. Zat hara dari pupuk masih rendah, "
            "pertumbuhan alga terkendali, dan oksigen air masih cukup untuk organisme air."
        )
    elif indeks_nutrien <= 70:
        status_eutrofikasi = "Sedang"
        status_alga = "Meningkat"
        status_do = "Menurun"
        kondisi = (
            "Ekosistem perairan mulai terganggu. Zat hara dari pupuk meningkat, "
            "pertumbuhan alga bertambah, dan oksigen air mulai menurun."
        )
    else:
        status_eutrofikasi = "Tinggi"
        status_alga = "Ledakan Alga"
        status_do = "Kritis"
        kondisi = (
            "Ekosistem perairan mengalami gangguan berat. Zat hara yang tinggi memicu ledakan alga, "
            "menurunkan oksigen air, dan mengganggu organisme air."
        )

    return {
        "kadar_nitrogen": round(N, 2),
        "kadar_fosfor": round(P, 2),
        "indeks_nutrien": round(indeks_nutrien, 2),
        "pertumbuhan_alga": round(pertumbuhan_alga, 2),
        "indeks_oksigen_air": round(indeks_oksigen_air, 2),

        "nilai_do": round(indeks_oksigen_air, 2),
        "kondisi_organisme": round(kondisi_organisme, 2),
        "status_eutrofikasi": status_eutrofikasi,
        "status_alga": status_alga,
        "status_do": status_do,
        "kondisi": kondisi,
    }


def buat_tren_eutrofikasi(kadar_nitrogen, kadar_fosfor):
    """
    Membuat tren eutrofikasi dari hari ke-0 sampai hari ke-30.
    Zat hara meningkat bertahap sampai nilai akhir berdasarkan input nitrogen dan fosfor.
    """
    N = _batasi_indeks(kadar_nitrogen)
    P = _batasi_indeks(kadar_fosfor)
    indeks_nutrien_akhir = (N + P) / 2

    waktu = [0, 5, 10, 15, 20, 25, 30]
    data = []

    for hari in waktu:
        faktor_waktu = hari / 30
        zat_hara = indeks_nutrien_akhir * faktor_waktu
        pertumbuhan_alga = zat_hara
        oksigen_air = _batasi_indeks(100 - (pertumbuhan_alga * 0.75))
        organisme_air = _batasi_indeks(100 - (pertumbuhan_alga * 0.90))

        data.append({
            "Waktu (hari)": hari,
            "Zat Hara": round(zat_hara, 2),
            "Pertumbuhan Alga": round(pertumbuhan_alga, 2),
            "Oksigen Air": round(oksigen_air, 2),
            "Organisme Air": round(organisme_air, 2)
        })

    return data