# Amazon Sales Analysis

The same small Amazon sales dataset (100 orders, 2010-2017, across 7 regions and 12 item types)
analyzed three ways: SQL, Python (pandas), and Power BI.

## Structure

```
.
├── data/amazon_sales_data.csv       # the raw dataset
├── notebooks/python_eda_analysis.ipynb   # pandas/matplotlib/seaborn EDA
├── sql/
│   ├── schema.sql                    # CREATE TABLE for the `sales` table
│   ├── queries.sql                   # 10 business queries, plain SQL
│   ├── sql_analysis.ipynb            # loads the CSV into real SQLite, runs queries.sql, shows output
│   └── build_sql_notebook.py         # (re)generates sql_analysis.ipynb -- not itself a deliverable
├── powerbi/amazon_sales_dashboard.pbix   # Power BI dashboard (open in Power BI Desktop)
└── reports/                          # PDF exports: final report, and each tool's own export
```

## SQL analysis (`sql/`)

`queries.sql` has 10 queries: revenue/profit by region, top item types, profit margin by item
type, online-vs-offline channel comparison, order-to-ship processing time by priority, top
countries by profit, yearly revenue trend, the single highest-profit order, and two window-
function examples (a running revenue total, and ranking each region's top item type by
`RANK() OVER (PARTITION BY ...)`).

`sql_analysis.ipynb` doesn't just print these queries -- it loads the CSV into a real in-memory
SQLite database (schema in `schema.sql`) and executes every query in `queries.sql` against it,
so the results shown are genuine SQL execution output, not a pandas re-implementation. Dates are
normalized before loading: 34 of the 100 rows use `M-D-YYYY` (hyphens) instead of the dominant
`M/D/YYYY` (slashes), a separator inconsistency rather than a day-first/month-first ambiguity
(every one of those 34 rows has a first component `<=12`).

A couple of the actual findings: high-priority orders ship *faster* on average than low-priority
ones (21.4 vs. 23.6 days) -- the priority label does correspond to real handling speed. Clothes
has the highest profit margin (67%) despite being one of the lower-revenue item types --
Cosmetics dominates on raw revenue but Clothes is the more profitable line per dollar sold.

To regenerate `sql_analysis.ipynb` after editing `queries.sql`:

```bash
cd sql
python3 build_sql_notebook.py
jupyter nbconvert --to notebook --execute --inplace sql_analysis.ipynb
```

## Python EDA (`notebooks/`)

`python_eda_analysis.ipynb` -- pandas-based exploration: summary stats, missing-value handling,
average price/cost by item type, processing time by sales channel, revenue trends, and several
matplotlib/seaborn visualizations. Runs in Jupyter or Google Colab (it's a standard `.ipynb`,
nothing environment-specific). Missing-value handling uses
`data.fillna(data.mean(numeric_only=True))` to fill only numeric columns.

## Power BI dashboard (`powerbi/`)

`amazon_sales_dashboard.pbix` -- open in [Power BI Desktop](https://powerbi.microsoft.com/desktop/)
(Windows only). `../reports/powerbi_dashboard_export.pdf` is a static PDF export if you just want
to see the dashboard without installing Power BI.

## Requirements

```bash
pip install -r ../requirements.txt
```

## License

[MIT](../LICENSE)
