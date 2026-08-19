-- Schema for the Amazon Sales dataset, loaded into a single `sales` table.
-- Dates are stored as TEXT in ISO-8601 (YYYY-MM-DD) so SQLite's date functions work directly.

CREATE TABLE IF NOT EXISTS sales (
    region          TEXT NOT NULL,
    country         TEXT NOT NULL,
    item_type       TEXT NOT NULL,
    sales_channel   TEXT NOT NULL CHECK (sales_channel IN ('Online', 'Offline')),
    order_priority  TEXT NOT NULL,
    order_date      TEXT NOT NULL,
    order_id        INTEGER PRIMARY KEY,
    ship_date       TEXT NOT NULL,
    units_sold      INTEGER NOT NULL,
    unit_price      REAL NOT NULL,
    unit_cost       REAL NOT NULL,
    total_revenue   REAL NOT NULL,
    total_cost      REAL NOT NULL,
    total_profit    REAL NOT NULL
);
