"""Kontrol alur enam tahap guided inquiry.

Modul ini tidak merender UI. Tugasnya memastikan siswa mengikuti urutan tahap,
memenuhi syarat minimal setiap tahap, dan menyimpan progress melalui lapisan
query baru.
"""

from database.queries import (
    advance_mission_stage,
    get_experiment_runs_df,
    get_inquiry_response,
    get_mission_progress,
    initialize_mission_progress,
    start_mission,
)
from modules.missions import INQUIRY_STAGES, MISSIONS, get_stage_index


STAGE_LABELS = {
    "fenomena": "Orientasi Fenomena",
    "rumusan_masalah": "Merumuskan Masalah",
    "hipotesis": "Menyusun Hipotesis",
    "penyelidikan": "Melakukan Penyelidikan",
    "analisis": "Menganalisis Data dan Menguji Hipotesis",
    "kesimpulan": "Menarik Kesimpulan",
}


class InquiryValidationError(ValueError):
    """Kesalahan saat siswa belum memenuhi syarat untuk lanjut tahap."""


def get_stage_label(stage_code):
    return STAGE_LABELS.get(stage_code, stage_code)


def get_stage_number(stage_code):
    index = get_stage_index(stage_code)
    return index + 1 if index >= 0 else 0


def get_stage_progress_percent(stage_code, status="sedang_dikerjakan"):
    if status == "selesai":
        return 100
    index = get_stage_index(stage_code)
    if index < 0:
        return 0
    return int((index / len(INQUIRY_STAGES)) * 100)


def can_access_stage(progress, target_stage):
    """Siswa dapat membuka tahap aktif dan tahap yang sudah dilewati."""
    if not progress or target_stage not in INQUIRY_STAGES:
        return False
    if progress.get("status") == "selesai":
        return True

    current_stage = progress.get("current_stage", INQUIRY_STAGES[0])
    current_index = get_stage_index(current_stage)
    target_index = get_stage_index(target_stage)
    return 0 <= target_index <= current_index


def get_mission_state(id_user, mission_code):
    if mission_code not in MISSIONS:
        raise ValueError("Kode misi tidak valid.")

    initialize_mission_progress(id_user)
    progress = get_mission_progress(id_user, mission_code)
    if progress is None:
        progress = start_mission(id_user, mission_code)

    return {
        **progress,
        "mission": MISSIONS[mission_code],
        "stage_number": get_stage_number(progress.get("current_stage")),
        "stage_total": len(INQUIRY_STAGES),
        "progress_percent": get_stage_progress_percent(
            progress.get("current_stage"), progress.get("status")
        ),
    }


def _has_text(response, field_name):
    return bool((response or {}).get(field_name, "").strip())


def validate_stage_completion(id_user, mission_code, stage_code):
    """Memvalidasi isi minimal sebelum siswa boleh lanjut.

    Return True bila valid. Bila belum, melempar InquiryValidationError dengan
    pesan yang dapat langsung ditampilkan di UI.
    """
    if mission_code not in MISSIONS:
        raise InquiryValidationError("Misi tidak valid.")
    if stage_code not in INQUIRY_STAGES:
        raise InquiryValidationError("Tahap guided inquiry tidak valid.")

    response = get_inquiry_response(id_user, mission_code) or {}

    if stage_code == "fenomena":
        if not _has_text(response, "pengamatan"):
            raise InquiryValidationError(
                "Tuliskan hasil pengamatan terhadap fenomena sebelum melanjutkan."
            )

    elif stage_code == "rumusan_masalah":
        if not _has_text(response, "rumusan_masalah"):
            raise InquiryValidationError(
                "Tuliskan rumusan masalah yang dapat diselidiki melalui simulasi."
            )

    elif stage_code == "hipotesis":
        required = [
            "hipotesis",
            "alasan_hipotesis",
            "variabel_bebas",
            "variabel_terikat",
        ]
        missing = [field for field in required if not _has_text(response, field)]
        if missing:
            raise InquiryValidationError(
                "Lengkapi hipotesis, alasan, variabel yang diubah, dan variabel yang diamati."
            )

    elif stage_code == "penyelidikan":
        runs = get_experiment_runs_df(id_user, mission_code)
        minimum_trials = int(MISSIONS[mission_code]["minimum_trials"])
        if len(runs) < minimum_trials:
            raise InquiryValidationError(
                f"Simpan minimal {minimum_trials} percobaan sebelum menganalisis data."
            )

    elif stage_code == "analisis":
        required = [
            "analisis_pola",
            "bukti_data_1",
            "bukti_data_2",
            "hubungan_variabel",
            "status_hipotesis",
            "alasan_uji_hipotesis",
        ]
        missing = [field for field in required if not _has_text(response, field)]
        if missing:
            raise InquiryValidationError(
                "Lengkapi pola data, dua bukti, hubungan antarvariabel, dan hasil pengujian hipotesis."
            )

    elif stage_code == "kesimpulan":
        if not _has_text(response, "kesimpulan"):
            raise InquiryValidationError(
                "Tuliskan kesimpulan yang menjawab rumusan masalah berdasarkan data."
            )

    return True


def complete_stage(id_user, mission_code, stage_code):
    """Validasi tahap, lalu majukan progress tepat satu tahap."""
    progress = start_mission(id_user, mission_code)
    current_stage = progress.get("current_stage", INQUIRY_STAGES[0])

    # Tahap lama yang sudah selesai boleh dipanggil ulang tanpa menurunkan progress.
    if get_stage_index(stage_code) < get_stage_index(current_stage):
        return progress

    if stage_code != current_stage:
        raise InquiryValidationError(
            f"Selesaikan tahap {get_stage_label(current_stage)} terlebih dahulu."
        )

    validate_stage_completion(id_user, mission_code, stage_code)
    return advance_mission_stage(id_user, mission_code, stage_code)
