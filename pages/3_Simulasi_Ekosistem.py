import json
from pathlib import Path

import pandas as pd
import streamlit as st

from components.inquiry_ui import (
    inject_inquiry_css,
    render_activity_header,
    render_hint,
    render_metric_cards,
    render_step_intro,
)
from components.mission_ui import inject_mission_css
from components.ui import load_css, role_navigation
from database.init_db import init_db
from database.queries import (
    clear_experiment_runs,
    get_experiment_runs_df,
    get_inquiry_response,
    get_mission_progress,
    save_experiment_run,
    save_inquiry_response,
    start_mission,
)
from modules.auth import require_role
from modules.inquiry_flow import InquiryValidationError, complete_stage
from modules.mission_content import get_mission_content
from modules.missions import MISSIONS
from modules.simulation import hitung_pencemaran_sungai


st.set_page_config(
    page_title="Aktivitas Misi",
    page_icon="🔬",
    layout="wide",
)


@st.cache_resource
def cached_init_db():
    init_db()


cached_init_db()
load_css()
require_role(["siswa"])
role_navigation()
inject_mission_css()
inject_inquiry_css()


id_user = st.session_state.get("id_user")
mission_code = st.session_state.get("selected_mission_code")

if not id_user:
    st.error("Identitas akun siswa tidak ditemukan. Silakan keluar lalu login kembali.")
    st.stop()

if mission_code not in MISSIONS:
    st.warning("Pilih misi terlebih dahulu dari halaman Misi Penyelidikan.")
    if st.button("Buka Misi Penyelidikan", type="primary"):
        st.switch_page("pages/2_Misi_Penyelidikan.py")
    st.stop()

# Tahap 3 mengaktifkan Misi 1 secara penuh. Tiga misi lain akan memakai pola
# halaman yang sama pada tahap pengembangan berikutnya.
if mission_code != "misi_1":
    mission = MISSIONS[mission_code]
    st.info(
        f"{mission['icon']} **{mission['title']}** sudah terdaftar dalam sistem, "
        "tetapi aktivitas lengkapnya belum diaktifkan pada Tahap 3."
    )
    if st.button("← Kembali ke Pilihan Misi", use_container_width=True):
        st.switch_page("pages/2_Misi_Penyelidikan.py")
    st.stop()

mission = MISSIONS[mission_code]
content = get_mission_content(mission_code)

if not content:
    st.error("Konten misi belum tersedia.")
    st.stop()

try:
    progress = start_mission(id_user, mission_code)
    response = get_inquiry_response(id_user, mission_code) or {}
    runs_df = get_experiment_runs_df(id_user, mission_code)
except Exception as exc:
    st.error("Aktivitas misi belum dapat membaca data dari database.")
    st.code(str(exc))
    st.stop()

status = progress.get("status", "sedang_dikerjakan")
current_stage = progress.get("current_stage", "fenomena")

render_activity_header(mission_code, mission, status, current_stage)

nav_left, nav_right = st.columns([1, 4])
with nav_left:
    if st.button("← Kembali ke Misi", use_container_width=True):
        st.switch_page("pages/2_Misi_Penyelidikan.py")
with nav_right:
    st.caption("Jawaban dan data percobaan tersimpan pada akunmu.")


def _as_dict(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}
    return {}


def _saved_index(options, value):
    try:
        return options.index(value)
    except ValueError:
        return 0


def _runs_table(dataframe):
    rows = []
    if dataframe is None or dataframe.empty:
        return pd.DataFrame(
            columns=[
                "Percobaan",
                "Tingkat Limbah (%)",
                "DO (mg/L)",
                "Populasi Ikan",
                "Makroinvertebrata",
            ]
        )

    for _, row in dataframe.sort_values("run_number").iterrows():
        input_data = _as_dict(row.get("input_data"))
        output_data = _as_dict(row.get("output_data"))
        rows.append(
            {
                "Percobaan": int(row.get("run_number", len(rows) + 1)),
                "Tingkat Limbah (%)": float(input_data.get("tingkat_limbah", 0)),
                "DO (mg/L)": float(output_data.get("nilai_do", 0)),
                "Populasi Ikan": float(output_data.get("populasi_ikan", 0)),
                "Makroinvertebrata": float(output_data.get("makroinvertebrata", 0)),
            }
        )
    return pd.DataFrame(rows)


def _render_saved_experiments(dataframe):
    table = _runs_table(dataframe)
    if table.empty:
        st.caption("Belum ada percobaan yang disimpan.")
        return table

    st.markdown("### Data hasil penyelidikanmu")
    st.dataframe(table, hide_index=True, use_container_width=True)

    sorted_table = table.sort_values("Tingkat Limbah (%)")
    chart_left, chart_right = st.columns(2, gap="large")
    with chart_left:
        st.markdown("**Perubahan oksigen terlarut**")
        st.line_chart(
            sorted_table.set_index("Tingkat Limbah (%)")[["DO (mg/L)"]],
            use_container_width=True,
        )
    with chart_right:
        st.markdown("**Perubahan organisme air**")
        st.line_chart(
            sorted_table.set_index("Tingkat Limbah (%)")[[
                "Populasi Ikan",
                "Makroinvertebrata",
            ]],
            use_container_width=True,
        )
    return table


def _safe_save_and_advance(stage_code, **fields):
    try:
        save_inquiry_response(id_user, mission_code, **fields)
        complete_stage(id_user, mission_code, stage_code)
        st.rerun()
    except InquiryValidationError as exc:
        st.warning(str(exc))
    except Exception as exc:
        st.error("Jawaban belum dapat disimpan.")
        st.code(str(exc))


def _render_completion_screen():
    latest_response = get_inquiry_response(id_user, mission_code) or {}
    latest_runs = get_experiment_runs_df(id_user, mission_code)

    st.markdown(
        """
        <div class="inq-complete">
            <div class="inq-kicker">Misi 1 selesai</div>
            <div class="inq-title" style="font-size:30px;">Kamu telah menyelesaikan enam tahap penyelidikan</div>
            <div class="inq-subtitle">Sekarang hubungkan temuanmu dengan konsep ekosistem, lalu tuliskan refleksi singkat.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Penguatan Konsep")
    col_image, col_text = st.columns([1.05, 1.4], gap="large")
    with col_image:
        concept_image = Path("assets/images/komponen_ekosistem.png")
        if concept_image.exists():
            st.image(str(concept_image), use_container_width=True)
    with col_text:
        st.markdown(f"### {content['reinforcement_title']}")
        st.write(content["reinforcement_text"])
        st.info(content["model_note"])

    st.divider()
    st.markdown("## Ringkasan Penyelidikanmu")
    if latest_response.get("rumusan_masalah"):
        st.markdown(f"**Rumusan masalah:** {latest_response['rumusan_masalah']}")
    if latest_response.get("hipotesis"):
        st.markdown(f"**Hipotesis awal:** {latest_response['hipotesis']}")
    if latest_response.get("kesimpulan"):
        st.markdown(f"**Kesimpulan:** {latest_response['kesimpulan']}")
    _render_saved_experiments(latest_runs)

    st.divider()
    st.markdown("## Refleksi dan Aksi")
    with st.form("reflection_form"):
        reflection = st.text_area(
            "Apa hal terpenting yang kamu pelajari dari misi ini?",
            value=latest_response.get("refleksi") or "",
            height=120,
        )
        action = st.text_area(
            "Tindakan apa yang dapat dilakukan untuk membantu menjaga ekosistem sungai?",
            value=latest_response.get("aksi_lingkungan") or "",
            height=120,
        )
        save_reflection = st.form_submit_button(
            "Simpan Refleksi",
            type="primary",
            use_container_width=True,
        )
    if save_reflection:
        if not reflection.strip() or not action.strip():
            st.warning("Lengkapi refleksi dan tindakan lingkungan sebelum menyimpan.")
        else:
            try:
                save_inquiry_response(
                    id_user,
                    mission_code,
                    refleksi=reflection,
                    aksi_lingkungan=action,
                )
                st.success("Refleksi berhasil disimpan.")
            except Exception as exc:
                st.error("Refleksi belum dapat disimpan.")
                st.code(str(exc))

    action_left, action_right = st.columns(2)
    with action_left:
        if st.button("📊 Lihat Hasil Saya", type="primary", use_container_width=True):
            st.switch_page("pages/3_Hasil_Saya.py")
    with action_right:
        if st.button("🏠 Kembali ke Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard_Siswa.py")


if status == "selesai":
    _render_completion_screen()
    st.stop()


if current_stage == "fenomena":
    render_step_intro(
        "fenomena",
        "Amati fenomena dan data awal. Catat fakta yang terlihat tanpa langsung menentukan penyebabnya.",
    )

    col_image, col_story = st.columns([1.05, 1.25], gap="large")
    with col_image:
        image_path = Path(content["phenomenon_image"])
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.info("Gambar fenomena belum ditemukan.")
    with col_story:
        st.markdown(f"### {content['phenomenon_title']}")
        st.write(content["phenomenon_story"])
        st.markdown("**Data pengamatan awal**")
        st.dataframe(
            pd.DataFrame(content["initial_observations"]),
            hide_index=True,
            use_container_width=True,
        )

    st.markdown('<div class="inq-question">Apa yang kamu amati?</div>', unsafe_allow_html=True)
    render_hint(content["observation_prompt"])

    with st.form("fenomena_form"):
        observation = st.text_area(
            "Hasil pengamatan saya",
            value=response.get("pengamatan") or "",
            placeholder="Contoh struktur jawaban: Pada data awal ..., sedangkan setelah perubahan ...",
            height=150,
        )
        submitted = st.form_submit_button(
            "Simpan dan Lanjutkan ke Rumusan Masalah →",
            type="primary",
            use_container_width=True,
        )
    if submitted:
        if not observation.strip():
            st.warning("Tuliskan hasil pengamatan terlebih dahulu.")
        else:
            _safe_save_and_advance("fenomena", pengamatan=observation)


elif current_stage == "rumusan_masalah":
    render_step_intro(
        "rumusan_masalah",
        "Ubah hasil pengamatan menjadi satu pertanyaan yang dapat diuji melalui simulasi.",
    )
    st.markdown(f"**Hasil pengamatanmu:** {response.get('pengamatan', '')}")
    st.markdown('<div class="inq-question">Apa yang ingin kamu selidiki?</div>', unsafe_allow_html=True)
    render_hint(content["problem_hint"])

    with st.form("problem_form"):
        problem = st.text_area(
            "Rumusan masalah saya",
            value=response.get("rumusan_masalah") or "",
            placeholder="Bagaimana pengaruh ... terhadap ...?",
            height=130,
        )
        submitted = st.form_submit_button(
            "Simpan dan Lanjutkan ke Hipotesis →",
            type="primary",
            use_container_width=True,
        )
    if submitted:
        if not problem.strip():
            st.warning("Tuliskan rumusan masalah terlebih dahulu.")
        else:
            _safe_save_and_advance("rumusan_masalah", rumusan_masalah=problem)


elif current_stage == "hipotesis":
    render_step_intro(
        "hipotesis",
        "Buat dugaan awal dan tentukan variabel sebelum melihat hasil simulasi.",
    )
    st.markdown(f"**Rumusan masalahmu:** {response.get('rumusan_masalah', '')}")
    render_hint(content["hypothesis_prompt"])

    independent_options = content["independent_variable_options"]
    dependent_options = content["dependent_variable_options"]
    control_options = content["control_variable_options"]

    with st.form("hypothesis_form"):
        hypothesis = st.text_area(
            "Hipotesis saya",
            value=response.get("hipotesis") or "",
            placeholder="Jika ..., maka ...",
            height=110,
        )
        reason = st.text_area(
            "Alasan saya",
            value=response.get("alasan_hipotesis") or "",
            placeholder="Jelaskan alasan ilmiah dari dugaanmu.",
            height=110,
        )

        var_col1, var_col2, var_col3 = st.columns(3)
        with var_col1:
            independent = st.selectbox(
                "Variabel yang diubah",
                independent_options,
                index=_saved_index(independent_options, response.get("variabel_bebas")),
            )
        with var_col2:
            dependent = st.selectbox(
                "Variabel yang diamati",
                dependent_options,
                index=_saved_index(dependent_options, response.get("variabel_terikat")),
            )
        with var_col3:
            control = st.selectbox(
                "Variabel yang dibuat tetap",
                control_options,
                index=_saved_index(control_options, response.get("variabel_kontrol")),
            )

        submitted = st.form_submit_button(
            "Simpan Hipotesis dan Mulai Penyelidikan →",
            type="primary",
            use_container_width=True,
        )
    if submitted:
        if not hypothesis.strip() or not reason.strip():
            st.warning("Lengkapi hipotesis dan alasan sebelum melanjutkan.")
        else:
            _safe_save_and_advance(
                "hipotesis",
                hipotesis=hypothesis,
                alasan_hipotesis=reason,
                variabel_bebas=independent,
                variabel_terikat=dependent,
                variabel_kontrol=control,
            )


elif current_stage == "penyelidikan":
    render_step_intro(
        "penyelidikan",
        "Ubah tingkat limbah, jalankan simulasi, lalu simpan sedikitnya tiga kondisi yang berbeda.",
    )

    runs_df = get_experiment_runs_df(id_user, mission_code)
    run_table = _runs_table(runs_df)
    saved_levels = set(run_table["Tingkat Limbah (%)"].tolist()) if not run_table.empty else set()
    minimum_trials = int(mission["minimum_trials"])

    st.markdown(
        f"**Percobaan tersimpan: {len(run_table)} dari minimal {minimum_trials}.** "
        "Gunakan nilai tingkat limbah yang berbeda agar pola dapat dibandingkan."
    )

    suggested_levels = [20, 50, 80]
    default_level = next((value for value in suggested_levels if value not in saved_levels), 35)

    control_col, result_col = st.columns([0.85, 1.35], gap="large")
    with control_col:
        with st.container(border=True):
            st.markdown("### Panel Percobaan")
            pollution_level = st.slider(
                "Tingkat limbah industri (%)",
                min_value=0,
                max_value=100,
                value=int(default_level),
                step=5,
            )
            st.caption("Ubah satu nilai, jalankan simulasi, lalu simpan hasilnya.")
            if st.button("Jalankan Simulasi", type="primary", use_container_width=True):
                preview = hitung_pencemaran_sungai(pollution_level)
                st.session_state[f"preview_{id_user}_{mission_code}"] = {
                    "tingkat_limbah": pollution_level,
                    "hasil": preview,
                }
                st.rerun()

    preview_key = f"preview_{id_user}_{mission_code}"
    preview_data = st.session_state.get(preview_key)

    with result_col:
        with st.container(border=True):
            st.markdown("### Hasil Kondisi yang Diuji")
            if preview_data:
                preview_level = int(preview_data.get("tingkat_limbah", 0))
                preview_result = preview_data.get("hasil", {})
                render_metric_cards(
                    [
                        ("Oksigen terlarut", f"{preview_result.get('nilai_do', 0):.2f} mg/L", preview_result.get("status_do", "")),
                        ("Populasi ikan", f"{preview_result.get('populasi_ikan', 0):.0f}", preview_result.get("status_populasi_ikan", "")),
                        ("Makroinvertebrata", f"{preview_result.get('makroinvertebrata', 0):.0f}", "Indeks 0–100"),
                    ]
                )
                st.caption(f"Hasil ini berasal dari tingkat limbah {preview_level}%.")

                duplicate = float(preview_level) in saved_levels
                value_changed = preview_level != pollution_level
                if duplicate:
                    st.warning("Kondisi ini sudah tersimpan. Gunakan tingkat limbah yang berbeda.")
                elif value_changed:
                    st.info("Nilai slider berubah. Jalankan simulasi lagi sebelum menyimpan.")

                if st.button(
                    "Simpan sebagai Percobaan",
                    use_container_width=True,
                    disabled=duplicate or value_changed,
                ):
                    try:
                        save_experiment_run(
                            id_user=id_user,
                            mission_code=mission_code,
                            simulation_code=mission["simulation_code"],
                            input_data={"tingkat_limbah": preview_level},
                            output_data=preview_result,
                        )
                        st.session_state.pop(preview_key, None)
                        st.rerun()
                    except Exception as exc:
                        st.error("Percobaan belum dapat disimpan.")
                        st.code(str(exc))
            else:
                st.info("Atur tingkat limbah lalu klik Jalankan Simulasi.")

    st.divider()
    run_table = _render_saved_experiments(get_experiment_runs_df(id_user, mission_code))

    with st.expander("Ulangi penyelidikan dari awal"):
        st.caption("Gunakan fitur ini hanya jika kamu ingin menghapus seluruh data percobaan pada Misi 1.")
        confirm_reset = st.checkbox("Saya memahami bahwa seluruh percobaan Misi 1 akan dihapus.")
        if st.button("Hapus Semua Percobaan", disabled=not confirm_reset):
            try:
                clear_experiment_runs(id_user, mission_code)
                st.session_state.pop(preview_key, None)
                st.rerun()
            except Exception as exc:
                st.error("Data percobaan belum dapat dihapus.")
                st.code(str(exc))

    enough_runs = len(run_table) >= minimum_trials
    if st.button(
        "Lanjutkan ke Analisis Data →",
        type="primary",
        use_container_width=True,
        disabled=not enough_runs,
    ):
        try:
            complete_stage(id_user, mission_code, "penyelidikan")
            st.rerun()
        except InquiryValidationError as exc:
            st.warning(str(exc))
        except Exception as exc:
            st.error("Tahap penyelidikan belum dapat diselesaikan.")
            st.code(str(exc))

    if not enough_runs:
        st.caption(f"Simpan minimal {minimum_trials} kondisi berbeda untuk membuka tahap analisis.")


elif current_stage == "analisis":
    render_step_intro(
        "analisis",
        "Bandingkan seluruh percobaan, temukan pola, gunakan bukti angka, lalu uji hipotesismu.",
    )

    runs_df = get_experiment_runs_df(id_user, mission_code)
    _render_saved_experiments(runs_df)

    st.markdown("### Hipotesis awalmu")
    st.info(response.get("hipotesis") or "Hipotesis belum tersimpan.")
    render_hint(
        "Gunakan angka dari tabel atau grafik. Hindari jawaban umum seperti 'naik' atau 'turun' tanpa menyebut data."
    )

    status_labels = {
        "Didukung": "didukung",
        "Didukung sebagian": "didukung_sebagian",
        "Tidak didukung": "tidak_didukung",
    }
    saved_status = response.get("status_hipotesis")
    saved_label = next((label for label, code in status_labels.items() if code == saved_status), "Didukung")

    with st.form("analysis_form"):
        pattern = st.text_area(
            "1. Pola apa yang kamu temukan dari semua percobaan?",
            value=response.get("analisis_pola") or "",
            height=120,
        )
        evidence1 = st.text_area(
            "2. Bukti data pertama",
            value=response.get("bukti_data_1") or "",
            placeholder="Sebutkan kondisi percobaan dan angka yang relevan.",
            height=100,
        )
        evidence2 = st.text_area(
            "3. Bukti data kedua",
            value=response.get("bukti_data_2") or "",
            placeholder="Gunakan data berbeda untuk memperkuat analisis.",
            height=100,
        )
        relationship = st.text_area(
            "4. Bagaimana hubungan tingkat limbah, oksigen terlarut, dan organisme air?",
            value=response.get("hubungan_variabel") or "",
            height=120,
        )
        hypothesis_label = st.radio(
            "5. Bagaimana hasil pengujian hipotesismu?",
            list(status_labels.keys()),
            index=list(status_labels.keys()).index(saved_label),
            horizontal=True,
        )
        test_reason = st.text_area(
            "6. Jelaskan keputusanmu menggunakan bukti data.",
            value=response.get("alasan_uji_hipotesis") or "",
            height=120,
        )

        submitted = st.form_submit_button(
            "Simpan Analisis dan Lanjutkan ke Kesimpulan →",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        required_texts = [pattern, evidence1, evidence2, relationship, test_reason]
        if any(not item.strip() for item in required_texts):
            st.warning("Lengkapi seluruh bagian analisis sebelum melanjutkan.")
        else:
            _safe_save_and_advance(
                "analisis",
                analisis_pola=pattern,
                bukti_data_1=evidence1,
                bukti_data_2=evidence2,
                hubungan_variabel=relationship,
                status_hipotesis=status_labels[hypothesis_label],
                alasan_uji_hipotesis=test_reason,
            )


elif current_stage == "kesimpulan":
    render_step_intro(
        "kesimpulan",
        "Jawab rumusan masalah secara langsung menggunakan hasil penyelidikan dan analisis datamu.",
    )

    st.markdown("### Rumusan masalah")
    st.info(response.get("rumusan_masalah") or "Rumusan masalah belum tersimpan.")

    st.markdown("### Hasil pengujian hipotesis")
    status_text = {
        "didukung": "Hipotesis didukung",
        "didukung_sebagian": "Hipotesis didukung sebagian",
        "tidak_didukung": "Hipotesis tidak didukung",
    }.get(response.get("status_hipotesis"), "Belum ditentukan")
    st.write(status_text)

    render_hint(
        "Kesimpulan yang baik menjawab rumusan masalah, menyebut arah hubungan antarvariabel, dan sesuai dengan data."
    )

    with st.form("conclusion_form"):
        conclusion = st.text_area(
            "Kesimpulan saya",
            value=response.get("kesimpulan") or "",
            placeholder="Berdasarkan hasil penyelidikan, saya menyimpulkan bahwa ...",
            height=170,
        )
        submitted = st.form_submit_button(
            "Simpan Kesimpulan dan Selesaikan Misi",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not conclusion.strip():
            st.warning("Tuliskan kesimpulan sebelum menyelesaikan misi.")
        else:
            _safe_save_and_advance("kesimpulan", kesimpulan=conclusion)


else:
    st.error("Tahap aktivitas tidak dikenali.")
