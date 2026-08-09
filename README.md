# PIBF-Enhanced Early Pregnancy Loss Risk Calculator

This repository contains a Streamlit implementation of a locked eight-predictor logistic model for estimating early pregnancy loss before 16 gestational weeks among patients presenting with threatened miscarriage.

## Research-use boundary

This application is a research prototype. It is not approved for diagnosis, triage, treatment selection, patient counseling, or autonomous clinical decision-making. Prospective validation, local recalibration, assay harmonization, institutional approval, and deployment governance are required before clinical implementation.

The included coefficient file currently represents the internal planning analysis. Replace and revalidate it against the author-verified real-data model before publication or public clinical evaluation.

## Model inputs

| Input | Format |
|---|---|
| Serum progesterone | ng/mL, continuous |
| Beta-hCG | mIU/mL, transformed using log10 |
| Fetal heartbeat | visible or not visible |
| Crown-rump length | mm, continuous |
| Bleeding grade | 1 spotting/light; 2 menses-like; 3 heavier bleeding/clots |
| Previous miscarriages | non-negative count |
| Subchorionic hematoma | present or absent |
| PIBF | ng/mL, transformed using the natural logarithm |

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Run tests

```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

## Deploy on Streamlit Community Cloud

1. Upload the contents of this folder to the root of a GitHub repository.
2. Create a new app in Streamlit Community Cloud.
3. Select the repository and branch.
4. Set the main file path to `app.py`.
5. Deploy and verify all three rows in `sample_cases.csv`.

No secrets, database, or patient-level file is required.

## Repository contents

- `app.py`: Streamlit interface.
- `risk_model.py`: deterministic model calculation and validation.
- `model_coefficients.json`: coefficients, transformations, standardization parameters, risk strata, and validation summary.
- `sample_cases.csv`: synthetic formula-check cases with expected probabilities.
- `tests/test_risk_model.py`: unit and regression tests.
- `QA_REPORT.md`: formula, locked-value, and responsive-interface checks.
- `.streamlit/config.toml`: application theme and server configuration.
- `MODEL_CARD.md`: intended use, validation, limitations, and update requirements.
- `DEPLOYMENT.md`: English deployment checklist.
- `DEPLOYMENT_CN.md`: Chinese deployment instructions.

## Citation

Add the final article citation and DOI after acceptance.
