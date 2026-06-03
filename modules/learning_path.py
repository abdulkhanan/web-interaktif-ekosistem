SIMULASI_PRASYARAT = {
    "Pencemaran Sungai": [
        "pengertian_ekosistem",
        "satuan_makhluk_hidup",
        "komponen_biotik_abiotik",
        "interaksi_antar_komponen",
        "pencemaran_sungai"
    ],
    "Aliran Energi dan Piramida Ekologi": [
        "pengertian_ekosistem",
        "satuan_makhluk_hidup",
        "komponen_biotik_abiotik",
        "aliran_energi",
        "piramida_ekologi"
    ],
    "Daur Biogeokimia: Daur Air": [
        "pengertian_ekosistem",
        "komponen_biotik_abiotik",
        "daur_biogeokimia"
    ]
}


NAMA_MATERI = {
    "pengertian_ekosistem": "Pengertian Ekosistem",
    "satuan_makhluk_hidup": "Satuan Makhluk Hidup Penyusun Ekosistem",
    "komponen_biotik_abiotik": "Komponen Biotik dan Abiotik",
    "interaksi_antar_komponen": "Interaksi Antar Komponen Ekosistem",
    "pencemaran_sungai": "Pencemaran Sungai dan Gangguan Ekosistem",
    "aliran_energi": "Aliran Energi dalam Ekosistem",
    "piramida_ekologi": "Piramida Ekologi",
    "tipe_ekosistem": "Tipe Ekosistem",
    "produktivitas": "Produktivitas",
    "daur_biogeokimia": "Daur Biogeokimia"
}


def cek_prasyarat_simulasi(jenis_simulasi, materi_selesai):
    prasyarat = SIMULASI_PRASYARAT.get(jenis_simulasi, [])
    materi_selesai_set = set(materi_selesai)

    belum_selesai = [
        kode for kode in prasyarat
        if kode not in materi_selesai_set
    ]

    return {
        "boleh_akses": len(belum_selesai) == 0,
        "prasyarat": prasyarat,
        "belum_selesai": belum_selesai
    }


def format_nama_materi(kode_materi):
    return NAMA_MATERI.get(kode_materi, kode_materi)