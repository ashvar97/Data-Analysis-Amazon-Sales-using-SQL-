-- Business analysis queries against the `sales` table (see schema.sql).
-- Every query here is executed and its real output shown in sql_analysis.ipynb.

-- 1. Total revenue and profit by region, ranked highest revenue first.
SELECT
    region,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(SUM(total_profit), 2)  AS total_profit,
    COUNT(*)                     AS num_orders
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 2. Top 5 item types by total revenue.
SELECT
    item_type,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    SUM(units_sold)              AS total_units_sold
FROM sales
GROUP BY item_type
ORDER BY total_revenue DESC
LIMIT 5;

-- 3. Profit margin (%) by item type -- which product lines are actually the most profitable
--    per dollar of revenue, not just the highest-revenue ones.
SELECT
    item_type,
    ROUND(SUM(total_profit), 2)                              AS total_profit,
    ROUND(100.0 * SUM(total_profit) / SUM(total_revenue), 2) AS profit_margin_pct
FROM sales
GROUP BY item_type
ORDER BY profit_margin_pct DESC;

-- 4. Online vs. offline: order count, average order value, and total profit per channel.
SELECT
    sales_channel,
    COUNT(*)                                    AS num_orders,
    ROUND(AVG(total_revenue), 2)                AS avg_order_value,
    ROUND(SUM(total_profit), 2)                 AS total_profit,
    ROUND(100.0 * SUM(total_profit) / SUM(total_revenue), 2) AS profit_margin_pct
FROM sales
GROUP BY sales_channel;

-- 5. Average order-to-ship processing time (days) by order priority -- does "High" priority
--    actually ship faster than "Low"?
SELECT
    order_priority,
    ROUND(AVG(JULIANDAY(ship_date) - JULIANDAY(order_date)), 2) AS avg_processing_days,
    COUNT(*) AS num_orders
FROM sales
GROUP BY order_priority
ORDER BY avg_processing_days;

-- 6. Top 10 countries by total profit.
SELECT
    country,
    ROUND(SUM(total_profit), 2) AS total_profit,
    COUNT(*)                    AS num_orders
FROM sales
GROUP BY country
ORDER BY total_profit DESC
LIMIT 10;

-- 7. Yearly revenue trend.
SELECT
    CAST(STRFTIME('%Y', order_date) AS INTEGER) AS order_year,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(SUM(total_profit), 2)  AS total_profit,
    COUNT(*)                     AS num_orders
FROM sales
GROUP BY order_year
ORDER BY order_year;

-- 8. The single highest-profit order.
SELECT *
FROM sales
ORDER BY total_profit DESC
LIMIT 1;

-- 9. Running (cumulative) total revenue over time, order by order -- a window function example.
SELECT
    order_date,
    order_id,
    total_revenue,
    SUM(total_revenue) OVER (ORDER BY order_date, order_id) AS running_total_revenue
FROM sales
ORDER BY order_date, order_id
LIMIT 20;

-- 10. Rank each region's item types by revenue within that region (window function: RANK).
SELECT *
FROM (
    SELECT
        region,
        item_type,
        SUM(total_revenue) AS item_revenue,
        RANK() OVER (PARTITION BY region ORDER BY SUM(total_revenue) DESC) AS revenue_rank
    FROM sales
    GROUP BY region, item_type
)
WHERE revenue_rank = 1
ORDER BY item_revenue DESC;
