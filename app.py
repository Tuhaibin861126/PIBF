from __future__ import annotations

import json

import altair as alt
import pandas as pd
import streamlit as st

from risk_model import MODEL, CalculatorInput, predict, result_payload


st.set_page_config(
    page_title="PIBF-Enhanced Risk Calculator",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, p, label, button { letter-spacing: 0 !important; }
    h1 { font-size: 2rem !important; line-height: 1.18 !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.05rem !important; }
    .model-kicker {
        color: #52615f;
        font-size: 0.86rem;
        font-weight: 650;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
    }
    .research-notice {
        border-left: 4px solid #b46a16;
        background: #fff8ec;
        color: #463316;
        padding: 0.78rem 1rem;
        margin: 0.9rem 0 1.35rem 0;
    }
    .result-empty {
        border: 1px solid #d7dedc;
        background: #f7f9f8;
        color: #52615f;
        min-height: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2rem;
    }
    div[data-testid="stMetric"] {
        border-top: 2px solid #d7dedc;
        padding-top: 0.7rem;
    }
    div[data-testid="stMetricValue"] { font-size: 1.65rem; }
    div[data-testid="stForm"] { border-radius: 6px; }
    div[data-testid="stAlert"] { border-radius: 6px; }
    .footer-note {
        color: #5f6d6b;
        font-size: 0.82rem;
        margin-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def contribution_frame(values: dict[str, float]) -> pd.DataFrame:
    labels = MODEL["display_labels"]
    rows = [
        {
            "Predictor": labels.get(feature, feature),
            "Contribution": value,
            "Direction": "Higher predicted risk" if value >= 0 else "Lower predicted risk",
        }
        for feature, value in values.items()
    ]
    return pd.DataFrame(rows).sort_values("Contribution")


def contribution_chart(frame: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(frame)
        .mark_bar(cornerRadiusEnd=2)
        .encode(
            x=alt.X(
                "Contribution:Q",
                title="Contribution (log-odds)",
                axis=alt.Axis(grid=True, gridColor="#e7ecea"),
            ),
            y=alt.Y(
                "Predictor:N",
                title=None,
                sort=None,
                axis=alt.Axis(labelLimit=175, labelOverlap=False),
            ),
            color=alt.Color(
                "Direction:N",
                scale=alt.Scale(
                    domain=["Higher predicted risk", "Lower predicted risk"],
                    range=["#b33d35", "#14745a"],
                ),
                legend=alt.Legend(
                    title=None,
                    orient="bottom",
                    direction="vertical",
                    columns=1,
                ),
            ),
            tooltip=[
                alt.Tooltip("Predictor:N"),
                alt.Tooltip("Contribution:Q", format=".3f"),
                alt.Tooltip("Direction:N"),
            ],
        )
        .properties(height=300)
    )


st.markdown('<div class="model-kicker">Research prediction tool</div>', unsafe_allow_html=True)
st.title("PIBF-Enhanced Early Pregnancy Loss Risk Calculator")
st.caption("Outcome: early pregnancy loss before 16 gestational weeks")
st.markdown(
    '<div class="research-notice"><strong>Research use only.</strong> '
    "This prototype is not approved for diagnosis, treatment selection, triage, or patient counseling. "
    "Prospective validation, local recalibration, assay harmonization, and institutional approval are required before clinical implementation.</div>",
    unsafe_allow_html=True,
)

input_column, result_column = st.columns([0.92, 1.08], gap="large")

with input_column:
    st.subheader("Index assessment")
    with st.form("risk_calculator"):
        biomarker_left, biomarker_right = st.columns(2)
        with biomarker_left:
            progesterone = st.number_input(
                "Serum progesterone (ng/mL)",
                min_value=0.0,
                max_value=200.0,
                value=20.0,
                step=0.1,
            )
            beta_hcg = st.number_input(
                "Beta-hCG (mIU/mL)",
                min_value=0.01,
                max_value=2000000.0,
                value=45000.0,
                step=100.0,
                format="%.2f",
            )
            pibf = st.number_input(
                "PIBF (ng/mL)",
                min_value=0.01,
                max_value=2000.0,
                value=165.0,
                step=1.0,
                format="%.2f",
            )
            previous_miscarriages = st.number_input(
                "Previous miscarriages",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
            )

        with biomarker_right:
            fetal_heartbeat = st.selectbox(
                "Fetal heartbeat",
                options=["Not visible", "Visible"],
            )
            crown_rump_length = st.number_input(
                "Crown-rump length (mm)",
                min_value=0.0,
                max_value=100.0,
                value=11.0,
                step=0.1,
            )
            bleeding_grade_label = st.selectbox(
                "Bleeding grade",
                options=[
                    "1 - Spotting/light",
                    "2 - Menses-like",
                    "3 - Heavy/clots",
                ],
                help=(
                    "Grade 1: spotting or light bleeding; grade 2: menses-like bleeding; "
                    "grade 3: heavier-than-menses bleeding or bleeding with clots."
                ),
            )
            hematoma = st.selectbox(
                "Subchorionic hematoma",
                options=["Absent", "Present"],
            )

        submitted = st.form_submit_button(
            "Calculate risk",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        raw_input = CalculatorInput(
            serum_progesterone_ng_ml=float(progesterone),
            beta_hcg_miu_ml=float(beta_hcg),
            pibf_ng_ml=float(pibf),
            fetal_heartbeat_visible=fetal_heartbeat == "Visible",
            crown_rump_length_mm=float(crown_rump_length),
            bleeding_grade=int(bleeding_grade_label[0]),
            previous_miscarriages=int(previous_miscarriages),
            subchorionic_hematoma=hematoma == "Present",
        )
        try:
            prediction = predict(raw_input)
            st.session_state["calculator_raw_input"] = raw_input
            st.session_state["calculator_prediction"] = prediction
        except ValueError as error:
            st.error(str(error))

with result_column:
    st.subheader("Estimated risk")
    prediction = st.session_state.get("calculator_prediction")
    raw_input = st.session_state.get("calculator_raw_input")

    if prediction is None or raw_input is None:
        st.markdown(
            '<div class="result-empty">No calculation has been generated.</div>',
            unsafe_allow_html=True,
        )
    else:
        probability_column, stratum_column, threshold_column = st.columns(3)
        probability_column.metric("Predicted probability", f"{prediction.probability:.1%}")
        stratum_column.metric("Risk stratum", prediction.risk_stratum)
        threshold_value = float(MODEL["development_youden_threshold"])
        threshold_display = (
            f">= {threshold_value:.3f}"
            if prediction.probability >= threshold_value
            else f"< {threshold_value:.3f}"
        )
        threshold_column.metric("Threshold status", threshold_display)

        if prediction.risk_stratum == "Low":
            st.success("Low predicted-risk stratum (<10%).")
        elif prediction.risk_stratum == "Intermediate":
            st.warning("Intermediate predicted-risk stratum (10% to <50%).")
        else:
            st.error("High predicted-risk stratum (>=50%).")

        st.caption(
            f"Fixed development-derived Youden threshold: "
            f"{MODEL['development_youden_threshold']:.3f}. This is a model-evaluation threshold, not a treatment cutoff."
        )

        for warning in prediction.range_warnings:
            st.warning(warning)

        st.markdown("#### Model contributions")
        frame = contribution_frame(prediction.feature_contributions)
        st.altair_chart(contribution_chart(frame), use_container_width=True)
        st.caption(
            "Contributions explain the fitted prediction function. They do not represent biological causality or the effect of changing a predictor."
        )

        payload = result_payload(raw_input, prediction)
        st.download_button(
            "Download result JSON",
            data=json.dumps(payload, indent=2),
            file_name="pibf_risk_result.json",
            mime="application/json",
            use_container_width=True,
        )

st.divider()

details_left, details_right = st.columns(2, gap="large")
with details_left:
    with st.expander("Model specification"):
        st.write(
            "The locked model uses serum progesterone, log10 beta-hCG, fetal heartbeat visibility, "
            "crown-rump length, bleeding grade, previous miscarriages, subchorionic hematoma, and natural-log PIBF."
        )
        st.write(
            "Inputs are standardized using development-cohort means and scales stored in the coefficient file. "
            "No patient-level data are required by the application."
        )

with details_right:
    with st.expander("Validation and implementation boundary"):
        validation = MODEL["validation_summary"]
        st.write(
            f"Reported AUCs were {validation['development_auc']:.3f} in development, "
            f"{validation['internal_validation_auc']:.3f} in internal validation, "
            f"{validation['center_b_external_auc']:.3f} in Center B, and "
            f"{validation['center_c_transport_auc']:.3f} in Center C."
        )
        st.write(validation["implementation_note"])

st.markdown(
    f'<div class="footer-note">Model version: {MODEL["model_version"]}. '
    "Confirm the coefficient file against the author-verified final analysis before publication.</div>",
    unsafe_allow_html=True,
)
