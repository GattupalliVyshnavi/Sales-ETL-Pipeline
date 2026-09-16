"""
LOAD stage
----------
Loads the cleaned data into a relational database (SQLite here -- the
same logic applies to MySQL/Postgres/Snowflake, just swap the
connection). Also builds a simple aggregate table using pure SQL, to
mirror the kind of reporting query a data warehouse would serve.
"""

import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "warehouse.db"


def load(clean_df: pd.DataFrame, rejected_df: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    try:
        # Fact table: one row per clean order line
        clean_df.to_sql("fact_sales", conn, if_exists="replace", index=False)

        # Rejected rows are kept too, for data-quality auditing
        rejected_df.to_sql("rejected_sales", conn, if_exists="replace", index=False)

        # Build a reporting aggregate purely with SQL (JOIN/GROUP BY-style logic)
        conn.execute("DROP TABLE IF EXISTS agg_sales_by_region_product;")
        conn.execute(
            """
            CREATE TABLE agg_sales_by_region_product AS
            SELECT
                region,
                product,
                COUNT(*)            AS num_orders,
                SUM(quantity)       AS total_units,
                SUM(total_amount)   AS total_revenue
            FROM fact_sales
            GROUP BY region, product
            ORDER BY total_revenue DESC;
            """
        )
        conn.commit()
        print(f"[LOAD] Loaded {len(clean_df)} rows into fact_sales at {db_path.name}")
        print("[LOAD] Built agg_sales_by_region_product via SQL GROUP BY")
    finally:
        conn.close()


if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw = extract()
    clean, rejected = transform(raw)
    load(clean, rejected)
