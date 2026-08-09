# GitHub Upload Manifest

## Runtime files

- `.streamlit/config.toml`
- `app.py`
- `risk_model.py`
- `model_coefficients.json`
- `requirements.txt`

Runtime dependency policy: `requirements.txt` directly declares Streamlit only; the application does not directly import Altair or Pandas.

## Verification files

- `sample_cases.csv`
- `requirements-dev.txt`
- `tests/test_risk_model.py`
- `QA_REPORT.md`

## Documentation

- `README.md`
- `DEPLOYMENT.md`
- `DEPLOYMENT_CN.md`
- `MODEL_CARD.md`
- `LICENSE.md`
- `MANIFEST.md`

## Excluded from the public package

- Patient-level data
- Manuscript and response-letter files
- Reviewer comments
- Internal simulation and analysis scripts
- Render caches and Python bytecode

## Locked planning values

- Development AUC: 0.956
- Internal-validation AUC: 0.932
- Center B AUC: 0.948
- Center C AUC: 0.932
- Development-derived threshold: 0.313682
- Risk strata: low <0.10; intermediate 0.10 to <0.50; high >=0.50
