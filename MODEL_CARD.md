# Model Card

## Model

PIBF-enhanced logistic model for early pregnancy loss before 16 gestational weeks in threatened miscarriage.

## Intended population

Patients presenting with vaginal bleeding, with or without abdominal pain, who satisfy the study eligibility criteria and have the required blood biomarkers and ultrasound predictors from the same clinical episode.

## Inputs and timing

The model accepts eight locked predictors. In the study framework, serum biomarkers and ultrasound predictors belonged to the same clinical episode and were obtained within 24 hours. The calculator cannot verify timing, assay platform, data completeness, or eligibility.

## Output

- Predicted probability from 0 to 1.
- Low (<0.10), intermediate (0.10 to <0.50), or high (>=0.50) predicted-risk stratum.
- Comparison with the fixed development-derived threshold of 0.313682.
- Additive contributions on the model linear-predictor scale.

The fixed threshold is an analysis threshold and is not a treatment cutoff.

## Validation summary

The current locked planning analysis produced AUCs of 0.956 in development, 0.932 in internal validation, 0.948 in Center B external validation, and 0.932 in Center C transport validation. Center C showed overprediction in the high-risk stratum.

## Limitations

- Current coefficients must be replaced or confirmed using the author-verified real dataset.
- Development events were modest relative to the eight predictor parameters.
- Calibration may vary by center, baseline risk, assay, and clinical workflow.
- PIBF lacks universally accepted clinical reference intervals and cross-platform harmonization.
- The model does not estimate treatment effects.
- Feature contributions explain fitted model behavior and are not causal effects.
- Inputs outside the development range are extrapolations.

## Clinical implementation requirements

Prospective validation, local recalibration, assay harmonization, impact evaluation, institutional approval, security review, monitoring, and clear clinical governance are required before clinical implementation.

## Data governance

This repository contains no patient-level data. The calculation is coefficient based and does not write submitted values to a database.
