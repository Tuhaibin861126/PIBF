# Deployment Checklist

## Before uploading

- Confirm `model_coefficients.json` against the author-verified locked model.
- Confirm beta-hCG uses log10 and PIBF uses the natural logarithm.
- Confirm progesterone and PIBF are entered in ng/mL and beta-hCG in mIU/mL.
- Confirm bleeding grade uses only grades 1, 2, and 3.
- Confirm the research-use notice remains visible on first page load.
- Confirm no patient-level data, manuscript files, reviewer files, or internal analysis scripts are included.
- Obtain agreement from all authors and the institution before selecting an open-source license.

## GitHub

Upload every file and folder in this directory to the repository root. The repository root should contain `app.py`, `risk_model.py`, `model_coefficients.json`, `requirements.txt`, and the `.streamlit` folder.

Suggested commands:

```bash
git init
git add .
git commit -m "Add PIBF research risk calculator"
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git push -u origin main
```

## Streamlit Community Cloud

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`
- Python version: 3.12 recommended
- Secrets: none required

## Post-deployment checks

1. Confirm the page loads without an exception.
2. Enter every row in `sample_cases.csv` and compare the displayed probability and stratum.
3. Check the page on desktop and mobile widths.
4. Confirm the JSON download works.
5. Confirm out-of-development-range values produce a visible warning.
6. Confirm the public repository does not contain patient-level data.

## Manuscript update

After deployment, replace the red manuscript placeholder with the public URL and update the response letter to the same URL.
