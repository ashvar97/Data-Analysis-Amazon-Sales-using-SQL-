"""One-off script that builds sql_analysis.ipynb. Not part of the deliverable itself --
kept so the notebook's construction is reproducible, but the notebook is what you'd actually open.
"""
import json

def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": src.splitlines(keepends=True)}

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

cells = []

cells.append(md("""# Amazon Sales -- SQL Analysis

Loads `../data/amazon_sales_data.csv` into a real SQLite database (schema in `schema.sql`) and
runs the business queries in `queries.sql` against it, so this is genuine SQL execution -- not a
Python re-implementation of what SQL would do. Complements `../notebooks/python_eda_analysis.ipynb`
(pandas-based EDA) and the Power BI dashboard: same dataset, three different tools, matching what
this repo's name promises."""))

cells.append(code("""import sqlite3
import re
import pandas as pd

DB_PATH = ":memory:"
conn = sqlite3.connect(DB_PATH)"""))

cells.append(md("## 1. Load the CSV, reshape dates to ISO-8601, load into SQLite per `schema.sql`"))

cells.append(code("""df = pd.read_csv("../data/amazon_sales_data.csv")

# The source CSV stores dates as M/D/YYYY, but 34 rows use "M-D-YYYY" (hyphens instead of
# slashes) -- a real inconsistency in the raw data, not a day-first/month-first ambiguity: every
# one of those 34 rows has a first component <=12, so they're the same M-D-YYYY format, just a
# different separator, not genuinely day-first dates. Normalize the separator, then parse
# uniformly. SQLite's date functions (JULIANDAY, STRFTIME) expect ISO-8601 (YYYY-MM-DD), so
# convert on the way in rather than inside SQL.
def parse_mixed_date(series):
    normalized = series.str.replace("-", "/", regex=False)
    return pd.to_datetime(normalized, format="%m/%d/%Y").dt.strftime("%Y-%m-%d")

df["Order Date"] = parse_mixed_date(df["Order Date"])
df["Ship Date"] = parse_mixed_date(df["Ship Date"])

df = df.rename(columns={
    "Region": "region", "Country": "country", "Item Type": "item_type",
    "Sales Channel": "sales_channel", "Order Priority": "order_priority",
    "Order Date": "order_date", "Order ID": "order_id", "Ship Date": "ship_date",
    "Units Sold": "units_sold", "Unit Price": "unit_price", "Unit Cost": "unit_cost",
    "Total Revenue": "total_revenue", "Total Cost": "total_cost", "Total Profit": "total_profit",
})

with open("schema.sql") as f:
    conn.executescript(f.read())

df.to_sql("sales", conn, if_exists="append", index=False)

pd.read_sql("SELECT COUNT(*) AS row_count FROM sales", conn)"""))

cells.append(md("## 2. Run each query from `queries.sql` against the real database"))

cells.append(code("""def load_queries(path):
    with open(path) as f:
        text = f.read()
    # split into blocks starting at each "-- N. <title>" comment
    blocks = re.split(r"\\n(?=-- \\d+\\.\\s)", text)
    queries = []
    for block in blocks:
        block = block.strip()
        if not re.match(r"-- \\d+\\.\\s", block):
            continue  # the file's header comment before query 1, not a real query
        title_line = block.splitlines()[0]
        title = title_line.lstrip("- ").strip()
        sql = "\\n".join(l for l in block.splitlines() if not l.strip().startswith("--")).strip()
        assert sql, f"query {title!r} parsed to empty SQL -- parser bug"
        queries.append((title, sql))
    return queries

queries = load_queries("queries.sql")
print(f"{len(queries)} queries loaded")
assert len(queries) == 10, f"expected 10 queries, got {len(queries)}\""""))

cells.append(code("""for title, sql in queries:
    print("=" * 80)
    print(title)
    print("=" * 80)
    result = pd.read_sql(sql, conn)
    display(result)
    print()"""))

cells.append(md("""## Notes

- Query 5 (processing time by priority) and query 9/10 (window functions) are the ones that
  most clearly need real SQL rather than a `pandas.groupby` -- `JULIANDAY` for date arithmetic,
  and `RANK() OVER (PARTITION BY ...)` for the per-region top item type.
- All ten queries above were executed against the actual SQLite database built from the CSV in
  this run, not hand-computed -- re-running this notebook top to bottom reproduces every number
  shown."""))

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

with open("sql_analysis.ipynb", "w") as f:
    json.dump(nb, f, indent=1)
print("wrote sql_analysis.ipynb")
