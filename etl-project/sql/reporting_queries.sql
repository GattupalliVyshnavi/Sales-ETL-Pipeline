-- Reporting queries against the warehouse.db built by the pipeline
-- Run with: sqlite3 data/warehouse.db < sql/reporting_queries.sql

-- 1. Total revenue and orders by region
SELECT
    region,
    COUNT(*)          AS num_orders,
    SUM(quantity)      AS total_units,
    SUM(total_amount)  AS total_revenue
FROM fact_sales
GROUP BY region
ORDER BY total_revenue DESC;

-- 2. Top-selling product overall (JOIN-style logic against the aggregate table)
SELECT
    product,
    SUM(total_units)   AS total_units_sold,
    SUM(total_revenue) AS total_revenue
FROM agg_sales_by_region_product
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 1;

-- 3. Orders above the average order value (subquery)
SELECT order_id, customer_name, product, total_amount
FROM fact_sales
WHERE total_amount > (SELECT AVG(total_amount) FROM fact_sales)
ORDER BY total_amount DESC;

-- 4. Data-quality check: see everything the pipeline rejected, and why
SELECT * FROM rejected_sales;
