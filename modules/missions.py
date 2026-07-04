"""Konfigurasi pusat untuk empat misi guided inquiry.

File ini sengaja tidak bergantung pada Streamlit agar dapat dipakai oleh
lapisan database, halaman siswa, dan dashboard guru tanpa side effect.
"""

INQUIRY_STAGES = [
    "fenomena",
    "rumusan_masalah",
    "hipotesis",
    "penyelidikan",
    "analisis",
    "kesimpulan",
]

MISSION_STATUS = [
    "belum_dimulai",
    "sedang_dikerjakan",
    "selesai",
]

HYPOTHESIS_STATUS = [
    "didukung",
    "didukung_sebagian",
    "tidak_didukung",
]

MISSIONS = {
    "misi_1": {
        "title": "Misteri Sungai yang Mulai Rusak",
        "short_title": "Misteri Sungai",
        "icon": "🌊",
        "focus": "Komponen biotik, abiotik, dan keseimbangan ekosistem",
        "simulation_code": "pencemaran_sungai",
        "material_code": "materi_1_komponen_ekosistem",
        "minimum_trials": 3,
        "theme": "blue",
    },
    "misi_2": {
        "title": "Energi di Tengah Kemarau",
        "short_title": "Energi Saat Kemarau",
        "icon": "☀️",
        "focus": "Aliran energi, rantai makanan, dan tingkat trofik",
        "simulation_code": "aliran_energi",
        "material_code": "materi_2_aliran_energi",
        "minimum_trials": 3,
        "theme": "orange",
    },
    "misi_3": {
        "title": "Ketika Pohon Terus Berkurang",
        "short_title": "Pohon Berkurang",
        "icon": "🌳",
        "focus": "Daur air, karbon dioksida, dan oksigen",
        "simulation_code": "daur_air_karbon_oksigen",
        "material_code": "materi_3_daur_air_karbon_oksigen",
        "minimum_trials": 3,
        "theme": "green",
    },
    "misi_4": {
        "title": "Ketika Perairan Dipenuhi Alga",
        "short_title": "Perairan dan Alga",
        "icon": "🌿",
        "focus": "Nitrogen, fosfor, dan eutrofikasi",
        "simulation_code": "eutrofikasi",
        "material_code": "materi_4_daur_nitrogen_fosfor",
        "minimum_trials": 4,
        "theme": "teal",
    },
}

MISSION_CODES = tuple(MISSIONS.keys())


def get_mission(mission_code):
    """Mengembalikan konfigurasi misi atau None bila kode tidak valid."""
    return MISSIONS.get((mission_code or "").strip())


def get_stage_index(stage_code):
    """Mengembalikan indeks tahap inquiry, atau -1 bila tidak valid."""
    try:
        return INQUIRY_STAGES.index((stage_code or "").strip())
    except ValueError:
        return -1


def get_next_stage(stage_code):
    """Mengembalikan tahap berikutnya. None bila tahap terakhir/tidak valid."""
    index = get_stage_index(stage_code)
    if index < 0 or index >= len(INQUIRY_STAGES) - 1:
        return None
    return INQUIRY_STAGES[index + 1]
