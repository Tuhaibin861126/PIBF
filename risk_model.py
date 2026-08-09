from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Mapping


MODEL_PATH = Path(__file__).with_name("model_coefficients.json")


def read_model(path: Path = MODEL_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


MODEL = read_model()


@dataclass(frozen=True)
class CalculatorInput:
    serum_progesterone_ng_ml: float
    beta_hcg_miu_ml: float
    pibf_ng_ml: float
    fetal_heartbeat_visible: bool
    crown_rump_length_mm: float
    bleeding_grade: int
    previous_miscarriages: int
    subchorionic_hematoma: bool


@dataclass(frozen=True)
class PredictionResult:
    probability: float
    risk_stratum: str
    threshold_comparison: str
    linear_predictor: float
    transformed_inputs: dict[str, float]
    standardized_inputs: dict[str, float]
    feature_contributions: dict[str, float]
    range_warnings: tuple[str, ...]


def sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


def transform_inputs(raw: CalculatorInput) -> dict[str, float]:
    return {
        "serum_progesterone_ng_ml": float(raw.serum_progesterone_ng_ml),
        "log10_beta_hcg": math.log10(float(raw.beta_hcg_miu_ml)),
        "fetal_heartbeat_visible": 1.0 if raw.fetal_heartbeat_visible else 0.0,
        "crown_rump_length_mm": float(raw.crown_rump_length_mm),
        "bleeding_grade": float(raw.bleeding_grade),
        "previous_miscarriages": float(raw.previous_miscarriages),
        "subchorionic_hematoma": 1.0 if raw.subchorionic_hematoma else 0.0,
        "log_pibf": math.log(float(raw.pibf_ng_ml)),
    }


def standardized_values(
    transformed: Mapping[str, float], model: Mapping = MODEL
) -> dict[str, float]:
    return {
        feature: (
            float(transformed[feature]) - float(model["scaler_mean"][feature])
        )
        / float(model["scaler_scale"][feature])
        for feature in model["features"]
    }


def feature_contributions(
    standardized: Mapping[str, float], model: Mapping = MODEL
) -> dict[str, float]:
    return {
        feature: float(model["coefficients_standardized"][feature])
        * float(standardized[feature])
        for feature in model["features"]
    }


def risk_category(probability: float, model: Mapping = MODEL) -> str:
    strata = model["risk_strata"]
    if probability < float(strata["low"]["upper_exclusive"]):
        return str(strata["low"]["label"])
    if probability < float(strata["intermediate"]["upper_exclusive"]):
        return str(strata["intermediate"]["label"])
    return str(strata["high"]["label"])


def threshold_flag(probability: float, model: Mapping = MODEL) -> str:
    threshold = float(model["development_youden_threshold"])
    if probability >= threshold:
        return "At or above threshold"
    return "Below threshold"


def validate_raw_input(raw: CalculatorInput) -> Iterable[str]:
    if raw.serum_progesterone_ng_ml < 0:
        yield "Serum progesterone cannot be negative."
    if raw.beta_hcg_miu_ml <= 0:
        yield "Beta-hCG must be greater than zero for log10 transformation."
    if raw.pibf_ng_ml <= 0:
        yield "PIBF must be greater than zero for natural-log transformation."
    if raw.crown_rump_length_mm < 0:
        yield "Crown-rump length cannot be negative."
    if int(raw.bleeding_grade) not in {1, 2, 3}:
        yield "Bleeding grade must be 1, 2, or 3."
    if raw.previous_miscarriages < 0:
        yield "Previous miscarriages cannot be negative."
    if int(raw.previous_miscarriages) != raw.previous_miscarriages:
        yield "Previous miscarriages must be a whole number."


def development_range_warnings(
    raw: CalculatorInput, model: Mapping = MODEL
) -> tuple[str, ...]:
    ranges = model["development_reference_ranges"]
    raw_values = {
        "serum_progesterone_ng_ml": raw.serum_progesterone_ng_ml,
        "beta_hcg_miu_ml": raw.beta_hcg_miu_ml,
        "crown_rump_length_mm": raw.crown_rump_length_mm,
        "bleeding_grade": raw.bleeding_grade,
        "previous_miscarriages": raw.previous_miscarriages,
        "pibf_ng_ml": raw.pibf_ng_ml,
    }
    labels = {
        "serum_progesterone_ng_ml": "Serum progesterone",
        "beta_hcg_miu_ml": "Beta-hCG",
        "crown_rump_length_mm": "Crown-rump length",
        "bleeding_grade": "Bleeding grade",
        "previous_miscarriages": "Previous miscarriages",
        "pibf_ng_ml": "PIBF",
    }
    warnings: list[str] = []
    for feature, value in raw_values.items():
        lower, upper = map(float, ranges[feature])
        if float(value) < lower or float(value) > upper:
            warnings.append(
                f"{labels[feature]} is outside the development range "
                f"({lower:g} to {upper:g})."
            )
    return tuple(warnings)


def predict(raw: CalculatorInput, model: Mapping = MODEL) -> PredictionResult:
    errors = tuple(validate_raw_input(raw))
    if errors:
        raise ValueError(" ".join(errors))

    transformed = transform_inputs(raw)
    standardized = standardized_values(transformed, model)
    contributions = feature_contributions(standardized, model)
    linear_predictor = float(model["intercept"]) + sum(contributions.values())
    probability = sigmoid(linear_predictor)

    return PredictionResult(
        probability=probability,
        risk_stratum=risk_category(probability, model),
        threshold_comparison=threshold_flag(probability, model),
        linear_predictor=linear_predictor,
        transformed_inputs=transformed,
        standardized_inputs=standardized,
        feature_contributions=contributions,
        range_warnings=development_range_warnings(raw, model),
    )


def result_payload(
    raw: CalculatorInput, result: PredictionResult, model: Mapping = MODEL
) -> dict:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_name": model["model_name"],
        "model_version": model["model_version"],
        "outcome": model["outcome"],
        "predicted_probability": result.probability,
        "risk_stratum": result.risk_stratum,
        "development_threshold": model["development_youden_threshold"],
        "threshold_comparison": result.threshold_comparison,
        "linear_predictor": result.linear_predictor,
        "inputs": asdict(raw),
        "transformed_inputs": result.transformed_inputs,
        "standardized_inputs": result.standardized_inputs,
        "feature_contributions_log_odds": result.feature_contributions,
        "range_warnings": list(result.range_warnings),
        "data_status": model["data_status"],
        "intended_use": model["intended_use"],
        "prohibited_use": model["prohibited_use"],
    }
