"""Komponen visual khusus aktivitas guided inquiry siswa."""

from html import escape
import streamlit as st

from modules.missions import INQUIRY_STAGES
from modules.inquiry_flow import STAGE_LABELS


STAGE_SHORT_LABELS = {
    "fenomena": "Fenomena",
    "rumusan_masalah": "Masalah",
    "hipotesis": "Hipotesis",
    "penyelidikan": "Penyelidikan",
    "analisis": "Analisis",
    "kesimpulan": "Kesimpulan",
}


def inject_inquiry_css():
    st.markdown(
        """
        <style>
            .inq-shell {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                padding: 24px;
                margin: 0 0 20px 0;
                box-shadow: 0 12px 32px rgba(15, 23, 42, .05);
            }
            .inq-kicker {
                font-size: 12px;
                font-weight: 900;
                letter-spacing: 1.1px;
                color: #0284c7;
                text-transform: uppercase;
                margin-bottom: 7px;
            }
            .inq-title {
                font-family: 'Outfit', sans-serif;
                font-size: clamp(27px, 4vw, 38px);
                font-weight: 900;
                line-height: 1.12;
                color: #0f172a;
                margin-bottom: 8px;
            }
            .inq-subtitle {
                color: #64748b;
                font-size: 15px;
                line-height: 1.65;
            }
            .inq-stage-track {
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 8px;
                margin: 18px 0 4px 0;
            }
            .inq-stage {
                border-radius: 12px;
                padding: 10px 7px;
                border: 1px solid #e2e8f0;
                background: #f8fafc;
                color: #64748b;
                text-align: center;
                font-size: 11px;
                font-weight: 800;
                line-height: 1.3;
            }
            .inq-stage.done {
                background: #f0fdf4;
                border-color: #bbf7d0;
                color: #166534;
            }
            .inq-stage.active {
                background: #f0f9ff;
                border-color: #7dd3fc;
                color: #075985;
                box-shadow: inset 0 0 0 1px rgba(2,132,199,.10);
            }
            .inq-step-card {
                border-left: 5px solid #0ea5e9;
                background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
                border-radius: 18px;
                padding: 18px 20px;
                margin: 8px 0 18px 0;
            }
            .inq-step-number {
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
                color: #0284c7;
                font-weight: 900;
                margin-bottom: 5px;
            }
            .inq-step-name {
                font-family: 'Outfit', sans-serif;
                font-size: 25px;
                font-weight: 900;
                color: #0f172a;
            }
            .inq-step-desc {
                color: #64748b;
                line-height: 1.65;
                margin-top: 6px;
            }
            .inq-hint {
                border: 1px solid #bae6fd;
                background: #f0f9ff;
                color: #0c4a6e;
                border-radius: 14px;
                padding: 13px 15px;
                margin: 10px 0 14px 0;
                line-height: 1.55;
                font-size: 14px;
            }
            .inq-question {
                font-family: 'Outfit', sans-serif;
                font-size: 20px;
                font-weight: 850;
                color: #0f172a;
                margin: 8px 0 7px 0;
            }
            .inq-metric-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 12px;
                margin: 10px 0 16px 0;
            }
            .inq-metric {
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 15px;
                background: #ffffff;
            }
            .inq-metric-label {
                color: #64748b;
                font-size: 12px;
                font-weight: 750;
                margin-bottom: 5px;
            }
            .inq-metric-value {
                color: #0f172a;
                font-family: 'Outfit', sans-serif;
                font-size: 25px;
                font-weight: 900;
            }
            .inq-metric-status {
                color: #475569;
                font-size: 12px;
                margin-top: 4px;
            }
            .inq-evidence {
                border-left: 4px solid #10b981;
                background: #f0fdf4;
                border-radius: 12px;
                padding: 12px 14px;
                color: #14532d;
                margin: 7px 0;
                line-height: 1.55;
            }
            .inq-complete {
                border: 1px solid #bbf7d0;
                background: linear-gradient(135deg, #f0fdf4, #ffffff);
                border-radius: 22px;
                padding: 23px;
                margin-bottom: 20px;
            }
            @media (max-width: 780px) {
                .inq-shell { padding: 19px; border-radius: 20px; }
                .inq-stage-track { grid-template-columns: repeat(3, minmax(0, 1fr)); }
                .inq-metric-grid { grid-template-columns: 1fr; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_activity_header(mission_code, mission, status, current_stage):
    try:
        current_index = INQUIRY_STAGES.index(current_stage)
    except ValueError:
        current_index = 0

    stage_html = []
    for index, stage in enumerate(INQUIRY_STAGES):
        css_class = ""
        symbol = "○"
        if status == "selesai" or index < current_index:
            css_class = "done"
            symbol = "✓"
        elif index == current_index:
            css_class = "active"
            symbol = "●"
        stage_html.append(
            f'<div class="inq-stage {css_class}">{symbol}<br>{escape(STAGE_SHORT_LABELS[stage])}</div>'
        )

    mission_number = escape(mission_code.replace("misi_", "Misi "))
    st.markdown(
        f"""
        <div class="inq-shell">
            <div class="inq-kicker">{mission_number} · Guided Inquiry</div>
            <div class="inq-title">{escape(str(mission['title']))}</div>
            <div class="inq-subtitle">{escape(str(mission['focus']))}</div>
            <div class="inq-stage-track">{''.join(stage_html)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step_intro(stage_code, description):
    try:
        number = INQUIRY_STAGES.index(stage_code) + 1
    except ValueError:
        number = 0
    label = STAGE_LABELS.get(stage_code, stage_code)
    st.markdown(
        f"""
        <div class="inq-step-card">
            <div class="inq-step-number">Langkah {number} dari {len(INQUIRY_STAGES)}</div>
            <div class="inq-step-name">{escape(str(label))}</div>
            <div class="inq-step-desc">{escape(str(description))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hint(text):
    st.markdown(
        f'<div class="inq-hint"><strong>Petunjuk</strong><br>{escape(str(text))}</div>',
        unsafe_allow_html=True,
    )


def render_metric_cards(metrics):
    cards = []
    for label, value, status in metrics:
        cards.append(
            f"""
            <div class="inq-metric">
                <div class="inq-metric-label">{escape(str(label))}</div>
                <div class="inq-metric-value">{escape(str(value))}</div>
                <div class="inq-metric-status">{escape(str(status))}</div>
            </div>
            """
        )
    st.markdown(
        '<div class="inq-metric-grid">' + ''.join(cards) + '</div>',
        unsafe_allow_html=True,
    )


def render_saved_evidence(label, text):
    st.markdown(
        f'<div class="inq-evidence"><strong>{escape(str(label))}</strong><br>{escape(str(text))}</div>',
        unsafe_allow_html=True,
    )
