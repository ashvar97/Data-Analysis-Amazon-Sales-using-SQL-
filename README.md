# Amazon Sales Data Analysis using SQL, Python & Power BI

Two independent projects:

## [`amazon-sales-analysis/`](amazon-sales-analysis/)

The same small Amazon sales dataset analyzed three ways: **SQL** (real SQLite queries -- revenue/
profit by region, profit margin by item type, online-vs-offline comparison, window-function
examples, and more), **Python** (pandas/matplotlib/seaborn EDA), and **Power BI** (interactive
dashboard). This matches what the repo's name has always promised -- previously there was no
actual SQL work here at all; that's what `amazon-sales-analysis/sql/` now provides.

This folder used to also contain an unrelated "Danny's Diner" SQL case study (a well-known
generic practice exercise with nothing to do with Amazon or this dataset) -- removed, and
replaced with real SQL analysis of the actual Amazon Sales data instead.

See [`amazon-sales-analysis/README.md`](amazon-sales-analysis/README.md).

## [`rainfall-prediction-ml/`](rainfall-prediction-ml/)

A genuine machine learning project: a RandomForest classifier predicting next-day rain from the
real "Rain in Australia" weather dataset (145,460 observations, 49 stations, 2007-2017).
Accuracy 0.814, ROC-AUC 0.873 -- full pipeline (cleaning, feature engineering, train/test split,
evaluation with precision/recall/F1/ROC-AUC given real class imbalance, feature importance) in
one runnable notebook.

See [`rainfall-prediction-ml/README.md`](rainfall-prediction-ml/README.md).

## Requirements

```bash
pip install -r requirements.txt
```

## License

[MIT](LICENSE)
