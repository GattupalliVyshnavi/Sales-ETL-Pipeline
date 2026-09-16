"""
PIPELINE orchestrator
----------------------
Runs Extract -> Transform -> Load in sequence, with basic logging and a
final summary. This plays the same role a tool like Airflow or a dbt
run would play in production: coordinating the stages and reporting
whether each one succeeded.
"""

import time
from extract import extract
from transform import transform
from load import load, DB_PATH


def run_pipeline() -> None:
    start = time.time()
    print("=" * 50)
    print("SALES ETL PIPELINE - START")
    print("=" * 50)

    raw_df = extract()
    clean_df, rejected_df = transform(raw_df)
    load(clean_df, rejected_df)

    elapsed = round(time.time() - start, 3)
    print("=" * 50)
    print(f"PIPELINE COMPLETE in {elapsed}s -> {DB_PATH}")
    print(f"  Rows loaded : {len(clean_df)}")
    print(f"  Rows rejected: {len(rejected_df)}")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
