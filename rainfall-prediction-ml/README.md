# Rainfall Prediction (Machine Learning)

A binary classification model predicting `RainTomorrow` from the real
["Rain in Australia"](https://rdrr.io/cran/rattle.data/man/weatherAUS.html) dataset: 145,460
daily weather observations from 49 Australian weather stations (2007-2017), originally from the
Australian Bureau of Meteorology.

Separate from `../amazon-sales-analysis/` -- this is a genuine supervised ML pipeline (cleaning
-> feature engineering -> train/test split -> model -> evaluation), not EDA or BI dashboarding.

## Pipeline

1. **Clean**: drop rows with a missing target (2.2%); drop `Sunshine`, `Evaporation`, `Cloud9am`,
   `Cloud3pm` (35-48% missing each -- imputing that much would be mostly inventing data, not
   filling gaps); impute the remaining, much smaller gaps (median for numeric, mode for
   categorical).
2. **Feature engineering**: encode `RainToday`/`RainTomorrow` as 0/1, extract month from date,
   one-hot encode the categorical weather-station/wind-direction columns (107 features after
   encoding).
3. **Split**: 80/20, stratified on the target so both splits keep the same ~22%/78% rain/no-rain
   ratio.
4. **Model**: `RandomForestClassifier` (150 trees, max depth 15, `class_weight="balanced"` --
   see [Notes](#results--notes) below on why).
5. **Evaluate**: accuracy, precision, recall, F1, ROC-AUC, confusion matrix, ROC curve, feature
   importances.

## Results

| Metric | Value |
|---|---|
| Accuracy | 0.814 |
| Precision (Rain) | 0.565 |
| Recall (Rain) | 0.741 |
| F1 (Rain) | 0.641 |
| ROC-AUC | 0.873 |

Top predictive features: `Humidity3pm` by a wide margin, then `Rainfall`, `Humidity9am`,
`Pressure9am`/`Pressure3pm`, and `RainToday` -- afternoon humidity dominating is a well-documented
finding for this dataset, which is a good sanity check that this pipeline is doing something
real rather than just running without error.

## Notes / limitations

- **Class imbalance** (~22% rain days): `class_weight="balanced"` trades some precision for
  recall on the minority class deliberately -- missing an actual rainy day is usually worse than
  an unnecessary umbrella, so accuracy alone would be a misleading headline metric here.
- **Random (not time-based) train/test split**: matches how this dataset is conventionally split
  in most public benchmarks, but can inflate reported performance slightly versus a strict
  forecast-into-the-future evaluation (e.g. train on 2007-2015, test on 2016-2017) — worth
  knowing if comparing this number against a time-blocked evaluation elsewhere.

## Usage

```bash
pip install -r ../requirements.txt
jupyter notebook rainfall_prediction.ipynb
```

Or open `rainfall_prediction.ipynb` directly in Google Colab -- it's a standard `.ipynb`, no
environment-specific code.

To regenerate the notebook after editing `build_notebook.py`:

```bash
python3 build_notebook.py
jupyter nbconvert --to notebook --execute --inplace rainfall_prediction.ipynb
```

## Requirements

```bash
pip install -r ../requirements.txt
```

## License

[MIT](../LICENSE)
