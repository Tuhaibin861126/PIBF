from __future__ import annotations

import csv
from pathlib import Path

import pytest

from risk_model import (
    MODEL,
    CalculatorInput,
    predict,
    risk_category,
    transform_inputs,
    validate_raw_input,
)


ROOT = Path(__file__).resolve().parents[1]


def from_row(row: dict[str, str]) -> CalculatorInput:
    return CalculatorInput(
        serum_progesterone_ng_ml=float(row["serum_progesterone_ng_ml"]),
        beta_hcg_miu_ml=float(row["beta_hcg_miu_ml"]),
        pibf_ng_ml=float(row["pibf_ng_ml"]),
        fetal_heartbeat_visible=row["fetal_heartbeat_visible"].lower() == "true",
        crown_rump_length_mm=float(row["crown_rump_length_mm"]),
        bleeding_grade=int(row["bleeding_grade"]),
        previous_miscarriages=int(row["previous_miscarriages"]),
        subchorionic_hematoma=row["subchorionic_hematoma"].lower() == "true",
    )


def test_transforms_match_model_definition() -> None:
    raw = CalculatorInput(18.0, 25000.0, 130.0, True, 12.0, 1, 0, False)
    transformed = transform_inputs(raw)
    assert transformed["log10_beta_hcg"] == pytest.approx(4.3979400086720375)
    assert transformed["log_pibf"] == pytest.approx(4.867534450455582)
    assert transformed["fetal_heartbeat_visible"] == 1.0
    assert transformed["subchorionic_hematoma"] == 0.0


def test_reference_cases_reproduce_locked_formula() -> None:
    with (ROOT / "sample_cases.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        result = predict(from_row(row))
        assert result.probability == pytest.approx(
            float(row["expected_probability"]), abs=1e-10
        )
        assert result.risk_stratum == row["expected_stratum"]


def test_risk_stratum_boundaries() -> None:
    assert risk_category(0.099999) == "Low"
    assert risk_category(0.10) == "Intermediate"
    assert risk_category(0.499999) == "Intermediate"
    assert risk_category(0.50) == "High"


def test_bleeding_grade_zero_is_rejected() -> None:
    raw = CalculatorInput(18.0, 25000.0, 130.0, True, 12.0, 0, 0, False)
    assert "Bleeding grade must be 1, 2, or 3." in tuple(validate_raw_input(raw))


def test_current_locked_metadata() -> None:
    assert MODEL["development_youden_threshold"] == pytest.approx(0.31368175954835764)
    assert MODEL["validation_summary"]["development_auc"] == pytest.approx(0.955914391900551)
    assert MODEL["validation_summary"]["internal_validation_auc"] == pytest.approx(0.9321789321789322)
    assert MODEL["validation_summary"]["center_b_external_auc"] == pytest.approx(0.9480611045828437)
    assert MODEL["validation_summary"]["center_c_transport_auc"] == pytest.approx(0.9315111042087281)


def test_app_does_not_import_optional_chart_packages() -> None:
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "import altair" not in app_source
    assert "import pandas" not in app_source
    assert "st.altair_chart" not in app_source
