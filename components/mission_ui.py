"""Komponen visual untuk dashboard dan hub empat misi guided inquiry."""

from html import escape

import streamlit as st

from modules.missions import INQUIRY_STAGES


MISSION_THEME = {
    "blue": {
        "accent": "#0284c7",
        "soft": "#e0f2fe",
        "border": "#bae6fd",
        "gradient": "linear-gradient(135deg, #eff6ff 0%, #ecfeff 100%)",
    },
    "orange": {
        "accent": "#ea580c",
        "soft": "#ffedd5",
        "border": "#fed7aa",
        "gradient": "linear-gradient(135deg, #fff7ed 0%, #fffbeb 100%)",
    },
    "green": {
        "accent": "#16a34a",
        "soft": "#dcfce7",
        "border": "#bbf7d0",
        "gradient": "linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%)",
    },
    "teal": {
        "accent": "#0f766e",
        "soft": "#ccfbf1",
        "border": "#99f6e4",
        "gradient": "linear-gradient(135deg, #f0fdfa 0%, #ecfeff 100%)",
    },
}

STATUS_META = {
    "belum_dimulai": {
        "label": "Belum dimulai",
        "icon": "○",
        "bg": "#f1f5f9",
        "text": "#475569",
    },
    "sedang_dikerjakan": {
        "label": "Sedang dikerjakan",
        "icon": "●",
        "bg": "#fef3c7",
        "text": "#b45309",
    },
    "selesai": {
        "label": "Selesai",
        "icon": "✓",
        "bg": "#dcfce7",
        "text": "#15803d",
    },
}

STAGE_LABELS = {
    "fenomena": "Fenomena",
    "rumusan_masalah": "Masalah",
    "hipotesis": "Hipotesis",
    "penyelidikan": "Penyelidikan",
    "analisis": "Analisis",
    "kesimpulan": "Kesimpulan",
}


def inject_mission_css():
    st.markdown(
        """
        <style>
            .mission-hero {
                background:
                    radial-gradient(circle at top right, rgba(14,165,233,.15), transparent 34%),
                    radial-gradient(circle at bottom left, rgba(16,185,129,.13), transparent 34%),
                    #ffffff;
                border: 1px solid rgba(203, 213, 225, .8);
                border-radius: 26px;
                padding: 28px 30px;
                margin: 4px 0 24px 0;
                box-shadow: 0 16px 42px rgba(15, 23, 42, .06);
            }
            .mission-kicker {
                font-size: 12px;
                font-weight: 900;
                letter-spacing: 1.2px;
                color: #059669;
                text-transform: uppercase;
                margin-bottom: 7px;
            }
            .mission-hero h1 {
                font-family: 'Outfit', sans-serif;
                font-size: clamp(28px, 4vw, 42px);
                line-height: 1.08;
                letter-spacing: -1px;
                color: #0f172a;
                margin: 0 0 10px 0;
            }
            .mission-hero p {
                color: #64748b;
                font-size: 16px;
                line-height: 1.7;
                margin: 0;
                max-width: 820px;
            }
            .overall-progress-shell {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 18px 20px;
                margin: 0 0 24px 0;
            }
            .overall-progress-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                margin-bottom: 10px;
            }
            .overall-progress-title {
                font-weight: 800;
                color: #0f172a;
                font-size: 15px;
            }
            .overall-progress-value {
                font-weight: 900;
                color: #047857;
                font-size: 14px;
            }
            .progress-track {
                height: 10px;
                width: 100%;
                background: #e2e8f0;
                border-radius: 999px;
                overflow: hidden;
            }
            .progress-fill {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, #10b981 0%, #0ea5e9 100%);
            }
            .next-mission-banner {
                border-radius: 18px;
                padding: 17px 20px;
                margin-bottom: 24px;
                background: linear-gradient(135deg, rgba(5,150,105,.08), rgba(2,132,199,.08));
                border: 1px solid rgba(5,150,105,.22);
                color: #14532d;
                line-height: 1.6;
            }
            .mission-card-head {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 15px;
            }
            .mission-icon {
                width: 52px;
                height: 52px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                flex: 0 0 auto;
            }
            .mission-status {
                border-radius: 999px;
                padding: 6px 10px;
                font-size: 11px;
                font-weight: 850;
                white-space: nowrap;
            }
            .mission-number {
                font-size: 11px;
                font-weight: 900;
                letter-spacing: 1px;
                text-transform: uppercase;
                margin-bottom: 7px;
            }
            .mission-title {
                font-family: 'Outfit', sans-serif;
                font-size: 22px;
                line-height: 1.2;
                font-weight: 900;
                color: #0f172a;
                min-height: 54px;
                margin-bottom: 8px;
            }
            .mission-focus {
                color: #64748b;
                font-size: 14px;
                line-height: 1.55;
                min-height: 66px;
                margin-bottom: 14px;
            }
            .mission-stage-line {
                font-size: 12px;
                color: #475569;
                font-weight: 700;
                margin-top: 9px;
            }
            .mission-card-spacer {
                height: 2px;
            }
            .mission-detail {
                border-radius: 24px;
                padding: 25px;
                margin-bottom: 20px;
                border: 1px solid #e2e8f0;
                background: #ffffff;
                box-shadow: 0 12px 32px rgba(15,23,42,.05);
            }
            .stage-track {
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 8px;
                margin: 18px 0 8px 0;
            }
            .stage-chip {
                border-radius: 12px;
                padding: 10px 6px;
                text-align: center;
                font-size: 11px;
                font-weight: 800;
                border: 1px solid #e2e8f0;
                color: #64748b;
                background: #f8fafc;
            }
            .stage-chip.done {
                color: #166534;
                border-color: #bbf7d0;
                background: #f0fdf4;
            }
            .stage-chip.active {
                color: #075985;
                border-color: #bae6fd;
                background: #f0f9ff;
                box-shadow: inset 0 0 0 1px rgba(2,132,199,.12);
            }
            .result-row {
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:12px;
                padding:13px 0;
                border-bottom:1px solid #f1f5f9;
            }
            .result-row:last-child { border-bottom: 0; }
            .result-title { font-weight:800; color:#0f172a; }
            .result-meta { font-size:12px; color:#64748b; margin-top:3px; }
            @media (max-width: 760px) {
                .mission-hero { padding: 22px 20px; border-radius: 20px; }
                .mission-title, .mission-focus { min-height: auto; }
                .stage-track { grid-template-columns: repeat(3, minmax(0, 1fr)); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_theme(theme_name):
    return MISSION_THEME.get(theme_name, MISSION_THEME["green"])


def get_status_meta(status):
    return STATUS_META.get(status, STATUS_META["belum_dimulai"])


def get_stage_label(stage_code):
    return STAGE_LABELS.get(stage_code, stage_code or "Fenomena")


def get_stage_progress(status, current_stage):
    if status == "selesai":
        return 100
    if status == "belum_dimulai":
        return 0
    try:
        index = INQUIRY_STAGES.index(current_stage)
    except ValueError:
        return 0
    return max(8, round((index / len(INQUIRY_STAGES)) * 100))


def mission_card_html(mission_code, mission, progress):
    status = (progress or {}).get("status", "belum_dimulai")
    current_stage = (progress or {}).get("current_stage", "fenomena")
    theme = get_theme(mission.get("theme"))
    status_meta = get_status_meta(status)
    progress_percent = get_stage_progress(status, current_stage)
    number = escape(mission_code.replace("misi_", "Misi "))

    return f"""
        <div class="mission-card-head">
            <div class="mission-icon" style="background:{theme['soft']}; color:{theme['accent']};">
                {escape(str(mission['icon']))}
            </div>
            <div class="mission-status" style="background:{status_meta['bg']}; color:{status_meta['text']};">
                {status_meta['icon']} {status_meta['label']}
            </div>
        </div>
        <div class="mission-number" style="color:{theme['accent']};">{number}</div>
        <div class="mission-title">{escape(str(mission['title']))}</div>
        <div class="mission-focus">{escape(str(mission['focus']))}</div>
        <div class="progress-track"><div class="progress-fill" style="width:{progress_percent}%;"></div></div>
        <div class="mission-stage-line">
            {"Selesai 6 dari 6 tahap" if status == "selesai" else ("Belum ada tahap yang dimulai" if status == "belum_dimulai" else f"Tahap aktif: {escape(get_stage_label(current_stage))}")}
        </div>
    """


def render_overall_progress(completed_count, total=4):
    percent = round((completed_count / total) * 100) if total else 0
    st.markdown(
        f"""
        <div class="overall-progress-shell">
            <div class="overall-progress-row">
                <div class="overall-progress-title">Progres keseluruhan</div>
                <div class="overall-progress-value">{completed_count} dari {total} misi selesai</div>
            </div>
            <div class="progress-track"><div class="progress-fill" style="width:{percent}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stage_tracker_html(status, current_stage):
    try:
        current_index = INQUIRY_STAGES.index(current_stage)
    except ValueError:
        current_index = 0

    chips = []
    for index, stage in enumerate(INQUIRY_STAGES):
        css_class = ""
        prefix = "○"
        if status == "selesai" or index < current_index:
            css_class = "done"
            prefix = "✓"
        elif status == "sedang_dikerjakan" and index == current_index:
            css_class = "active"
            prefix = "●"
        chips.append(
            f'<div class="stage-chip {css_class}">{prefix}<br>{escape(get_stage_label(stage))}</div>'
        )
    return '<div class="stage-track">' + "".join(chips) + "</div>"
