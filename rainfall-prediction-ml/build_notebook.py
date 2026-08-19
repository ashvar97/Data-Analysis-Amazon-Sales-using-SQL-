"""One-off script that builds rainfall_prediction.ipynb. Not part of the deliverable itself --
kept so the notebook's construction is reproducible, but the notebook is what you'd actually open.
"""
import json

def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": src.splitlines(keepends=True)}

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

cells = []

cells.append(md("""# Rain in Australia -- Next-Day Rainfall Prediction

A binary classification model predicting `RainTomorrow` (will it rain tomorrow, yes/no) from
today's weather observations, using the real "Rain in Australia" dataset: 145,460 daily
observations from 49 Australian weather stations (2007-2017), originally from the Australian
Bureau of Meteorology (via the `rattle` R package's `weatherAUS` dataset).

Separate sub-project from `../amazon-sales-analysis/` -- this one is a genuine supervised ML
pipeline (data cleaning -> feature engineering -> train/test split -> model -> evaluation), not
EDA/BI dashboarding."""))

cells.append(code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report, RocCurveDisplay,
)

RANDOM_STATE = 42"""))

cells.append(md("## 1. Load and inspect"))

cells.append(code("""df = pd.read_csv("data/weatherAUS.csv")
print(f"{df.shape[0]:,} rows, {df.shape[1]} columns")
df.head()"""))

cells.append(code("""missing_pct = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
missing_pct[missing_pct > 0]"""))

cells.append(md("""## 2. Clean

- Drop rows with a missing target -- can't train or evaluate on those (2.2% of rows).
- Drop the four columns with >35% missing (`Sunshine`, `Evaporation`, `Cloud9am`, `Cloud3pm`):
  imputing that much of a column would mostly be inventing data, not filling gaps.
- Impute the remaining, much smaller gaps: median for numeric columns, mode for categorical."""))

cells.append(code("""df = df.dropna(subset=["RainTomorrow"])
print(f"{df.shape[0]:,} rows after dropping missing-target rows")

high_missing_cols = df.columns[df.isna().mean() > 0.35].tolist()
print("dropping (>35% missing):", high_missing_cols)
df = df.drop(columns=high_missing_cols)"""))

cells.append(md("## 3. Feature engineering"))

cells.append(code("""target = df["RainTomorrow"].map({"No": 0, "Yes": 1})
print("Class balance:")
print(target.value_counts(normalize=True).rename("fraction"))"""))

cells.append(code("""fig, ax = plt.subplots(figsize=(5, 4))
target.value_counts().rename({0: "No rain", 1: "Rain"}).plot(kind="bar", ax=ax, color=["#4C72B0", "#C44E52"])
ax.set_ylabel("count")
ax.set_title("RainTomorrow class balance")
plt.tight_layout()
plt.savefig("class_balance.png", dpi=120)
plt.show()"""))

cells.append(code("""df["RainToday"] = df["RainToday"].map({"No": 0, "Yes": 1})

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df = df.drop(columns=["Date", "RainTomorrow"])

cat_cols = df.select_dtypes(include=["object", "str"]).columns.tolist()
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print("categorical:", cat_cols)
print("numeric:", num_cols)

for c in num_cols:
    df[c] = df[c].fillna(df[c].median())
for c in cat_cols:
    df[c] = df[c].fillna(df[c].mode().iloc[0])

df_enc = pd.get_dummies(df, columns=cat_cols, drop_first=True)
print(f"encoded feature matrix: {df_enc.shape}")"""))

cells.append(md("""## 4. Correlation of numeric features with next-day rain

(computed before one-hot encoding, against the numeric weather features only, for readability)"""))

cells.append(code("""numeric_with_target = df[num_cols].copy()
numeric_with_target["RainTomorrow"] = target.values
corr = numeric_with_target.corr()["RainTomorrow"].drop("RainTomorrow").sort_values()

fig, ax = plt.subplots(figsize=(6, 5))
corr.plot(kind="barh", ax=ax, color=["#C44E52" if v > 0 else "#4C72B0" for v in corr])
ax.set_xlabel("correlation with RainTomorrow")
ax.set_title("Which of today's numeric features correlate with tomorrow's rain?")
plt.tight_layout()
plt.savefig("feature_correlation.png", dpi=120)
plt.show()"""))

cells.append(md("""## 5. Train/test split and model

80/20 split, stratified on the target so both splits keep the same ~22%/78% rain/no-rain ratio.
`class_weight="balanced"` on the RandomForest, since a model optimizing plain accuracy on this
imbalanced a target tends to just predict "No" most of the time and still look accurate."""))

cells.append(code("""X_train, X_test, y_train, y_test = train_test_split(
    df_enc, target, test_size=0.2, random_state=RANDOM_STATE, stratify=target
)
print(f"train: {X_train.shape}, test: {X_test.shape}")

clf = RandomForestClassifier(
    n_estimators=150, max_depth=15, random_state=RANDOM_STATE, n_jobs=-1, class_weight="balanced"
)
clf.fit(X_train, y_train)"""))

cells.append(md("## 6. Evaluate"))

cells.append(code("""pred = clf.predict(X_test)
proba = clf.predict_proba(X_test)[:, 1]

print(f"accuracy:  {accuracy_score(y_test, pred):.3f}")
print(f"precision: {precision_score(y_test, pred):.3f}")
print(f"recall:    {recall_score(y_test, pred):.3f}")
print(f"f1:        {f1_score(y_test, pred):.3f}")
print(f"ROC-AUC:   {roc_auc_score(y_test, proba):.3f}")
print()
print(classification_report(y_test, pred, target_names=["No rain", "Rain"]))"""))

cells.append(code("""cm = confusion_matrix(y_test, pred)
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["No rain", "Rain"], yticklabels=["No rain", "Rain"], ax=ax)
ax.set_xlabel("predicted")
ax.set_ylabel("actual")
ax.set_title("Confusion matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=120)
plt.show()"""))

cells.append(code("""fig, ax = plt.subplots(figsize=(5, 5))
RocCurveDisplay.from_predictions(y_test, proba, ax=ax, name="RandomForest")
ax.plot([0, 1], [0, 1], "k--", alpha=0.4, label="chance")
ax.set_title("ROC curve")
ax.legend()
plt.tight_layout()
plt.savefig("roc_curve.png", dpi=120)
plt.show()"""))

cells.append(md("## 7. Feature importance"))

cells.append(code("""importances = pd.Series(clf.feature_importances_, index=X_train.columns).sort_values(ascending=False).head(15)

fig, ax = plt.subplots(figsize=(6, 6))
importances.sort_values().plot(kind="barh", ax=ax, color="#4C72B0")
ax.set_xlabel("importance")
ax.set_title("Top 15 feature importances")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=120)
plt.show()"""))

cells.append(md("""## Notes / limitations

- **Class imbalance**: only ~22% of days are followed by rain. `class_weight="balanced"` trades
  some precision for recall on the minority ("Rain") class -- for a rain forecast, missing an
  actual rainy day (false negative) is usually worse than an unnecessary umbrella (false
  positive), so this is a deliberate choice, not an oversight. Plain accuracy alone would be
  misleading here; that's why precision/recall/F1/ROC-AUC are all reported above, not just accuracy.
- **Random (not time-based) train/test split**: rows from the same station on nearby dates can
  end up on both sides of the split, which can inflate reported performance slightly versus a
  strict forecast-into-the-future evaluation (e.g. train on 2007-2015, test on 2016-2017). This
  matches how this dataset is conventionally split in most public benchmarks/tutorials, but is
  worth knowing if you're comparing this number to a genuinely time-blocked evaluation.
- **Missing-data columns dropped, not imputed**: `Sunshine`, `Evaporation`, `Cloud9am`,
  `Cloud3pm` were dropped rather than imputed because 35-48% of their values are missing --
  imputing that much would mean mostly inventing data rather than filling small gaps."""))

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("rainfall_prediction.ipynb", "w") as f:
    json.dump(nb, f, indent=1)
print("wrote rainfall_prediction.ipynb")
