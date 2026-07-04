"""Konten pembelajaran untuk aktivitas guided inquiry.

Tahap 3 mengaktifkan Misi 1 secara penuh. Konten dipisahkan dari halaman
Streamlit agar mudah divalidasi oleh ahli materi dan diperluas ke misi lain.
"""

MISSION_CONTENT = {
    "misi_1": {
        "phenomenon_title": "Misteri Sungai yang Mulai Rusak",
        "phenomenon_image": "assets/images/pencemaran_sungai.jpg",
        "phenomenon_story": (
            "Sebuah sungai yang sebelumnya jernih dan banyak dihuni organisme air mulai "
            "mengalami perubahan setelah aktivitas industri di sekitarnya meningkat. Air tampak "
            "lebih keruh. Beberapa ikan ditemukan mati, sedangkan jumlah organisme kecil di dasar "
            "sungai berkurang. Tim pengamat kemudian membandingkan kondisi sungai pada dua waktu berbeda."
        ),
        "initial_observations": [
            {
                "Kondisi": "Pengamatan awal",
                "DO (mg/L)": 8.2,
                "Populasi ikan (indeks)": 93,
                "Makroinvertebrata (indeks)": 90,
            },
            {
                "Kondisi": "Setelah perubahan",
                "DO (mg/L)": 5.1,
                "Populasi ikan (indeks)": 61,
                "Makroinvertebrata (indeks)": 56,
            },
        ],
        "observation_prompt": (
            "Tuliskan minimal dua hal yang kamu amati dari gambar, cerita, dan data awal. "
            "Fokus pada perubahan yang benar-benar terlihat."
        ),
        "problem_prompt": (
            "Berdasarkan fenomena tersebut, tuliskan satu pertanyaan yang dapat kamu selidiki "
            "menggunakan simulasi."
        ),
        "problem_hint": "Gunakan pola: Bagaimana pengaruh ... terhadap ...?",
        "hypothesis_prompt": (
            "Buat dugaan awal sebelum menjalankan simulasi. Gunakan pola jika ..., maka ..., "
            "lalu jelaskan alasan ilmiah dari dugaanmu."
        ),
        "independent_variable_options": [
            "Tingkat limbah industri",
            "Kualitas air",
            "Populasi ikan",
        ],
        "dependent_variable_options": [
            "Oksigen terlarut dan populasi ikan",
            "Kualitas air dan makroinvertebrata",
            "Populasi ikan dan makroinvertebrata",
        ],
        "control_variable_options": [
            "Lama pengamatan dan model ekosistem",
            "Tingkat limbah industri",
            "Populasi ikan",
        ],
        "reinforcement_title": "Menghubungkan Data dengan Konsep Ekosistem",
        "reinforcement_text": (
            "Ekosistem tersusun atas komponen abiotik dan biotik yang saling berhubungan. "
            "Air dan oksigen terlarut termasuk komponen abiotik. Ikan dan makroinvertebrata "
            "termasuk komponen biotik. Ketika tingkat limbah meningkat, kualitas lingkungan air "
            "dapat berubah. Perubahan kondisi abiotik kemudian dapat memengaruhi organisme yang "
            "bergantung pada kondisi tersebut. Data percobaanmu menunjukkan pola hubungan itu "
            "dalam sebuah model edukatif."
        ),
        "model_note": (
            "Simulasi menggunakan model indeks edukatif untuk memperlihatkan pola hubungan "
            "antarvariabel. Hasil simulasi tidak digunakan untuk memprediksi kondisi sungai nyata."
        ),
    }
}


def get_mission_content(mission_code):
    """Mengembalikan konten misi atau None bila belum tersedia."""
    return MISSION_CONTENT.get((mission_code or "").strip())
