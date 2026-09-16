"""
EXTRACT stage
-------------
Reads raw data from the source (a CSV file here, but in a real pipeline
this could just as easily be a REST API, an S3 bucket, or a database
table). Kept deliberately dumb: extract should not clean or transform
anything, only pull the data in.
"""

import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw_sales.csv"


def extract(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Read the raw sales CSV into a DataFrame."""
    df = pd.read_csv(path)
    print(f"[EXTRACT] Read {len(df)} rows from {path.name}")
    return df


if __name__ == "__main__":
    df = extract()
    print(df.head())
