# Calculator QA Report

Date: 2026-08-09

## Formula checks

- Model JSON parsed successfully.
- Python files compiled successfully.
- Five automated tests passed.
- Three synthetic reference cases reproduced their locked probabilities within an absolute tolerance of 1e-10.
- Risk-stratum boundaries were verified at 0.10 and 0.50.
- Bleeding grade 0 was verified as invalid.

## Locked-value checks

- Development-derived threshold: 0.31368175954835764.
- Development AUC: 0.955914391900551.
- Internal-validation AUC: 0.9321789321789322.
- Center B external-validation AUC: 0.9480611045828437.
- Center C transport-validation AUC: 0.9315111042087281.

## Interface checks

- Local Streamlit server returned a healthy response.
- Desktop layout checked at 1440 x 1000 pixels.
- Mobile layout checked at 390 x 844 pixels.
- No horizontal page overflow was detected at mobile width.
- Input form, calculation button, risk metrics, warning panel, contribution chart, and JSON download control rendered.
- All eight contribution labels remained visible on mobile.
- No browser console errors were detected.

## Public-package checks

- No patient-level dataset is included.
- No manuscript, reviewer comment, or response-letter file is included.
- Python bytecode and cache directories are excluded by `.gitignore` and must be removed before zipping.
