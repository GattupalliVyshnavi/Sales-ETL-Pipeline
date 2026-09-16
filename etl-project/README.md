# Sales ETL Pipeline

A small end-to-end ETL (Extract, Transform, Load) pipeline built with
Python and SQL, designed to demonstrate core data-engineering
fundamentals: data extraction, cleaning/validation, relational loading,
and SQL-based reporting.

## What it does

1. **Extract** (`etl/extract.py`) — reads raw sales records from a CSV
   source file.
2. **Transform** (`etl/transform.py`) — cleans and validates the data
   using Pandas:
   - trims/standardizes text fields
   - parses dates
   - rejects rows with missing customer names, invalid quantities, or
     bad dates (instead of silently dropping them, they are kept in a
     separate `rejected_sales` table for auditing)
   - derives a `total_amount` column
3. **Load** (`etl/load.py`) — loads the clean data into a SQLite
   database as a `fact_sales` table, and builds an aggregate
   `agg_sales_by_region_product` table using a SQL `GROUP BY` query.
4. **Orchestration** (`etl/pipeline.py`) — runs all three stages in
   sequence with logging and a run summary, the same role a scheduler
   like Airflow would play in production.
5. **Reporting** (`sql/reporting_queries.sql`) — SQL queries against
   the warehouse: revenue by region, top-selling product, orders above
   average value, and a data-quality check on rejected rows.

## Why it's structured this way

This mirrors a simplified version of a real ETL pipeline: separate,
single-responsibility stages (extract / transform / load) that can be
tested and run independently, a clear data-quality gate instead of
silently dropping bad records, and a warehouse layer that supports
downstream SQL reporting.

## How to run it

```bash
pip install -r requirements.txt
cd etl
python pipeline.py
```

This produces `data/warehouse.db` (SQLite) with three tables:
`fact_sales`, `rejected_sales`, and `agg_sales_by_region_product`.

Then run the reporting queries:

```bash
sqlite3 data/warehouse.db < sql/reporting_queries.sql
```

## Tech used

Python, Pandas, SQL (SQLite), basic data-quality validation, ETL
pipeline design.

## Possible extensions

- Swap SQLite for MySQL/Postgres/Snowflake by changing the connection
  in `load.py`
- Schedule with Apache Airflow (each stage maps cleanly to a DAG task)
- Add dbt models on top of `fact_sales` for the aggregate layer
- Add PySpark version of `transform.py` for larger datasets
