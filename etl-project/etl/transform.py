"""
TRANSFORM stage
----------------
Cleans and validates the raw data, then derives the fields the business
actually needs. This is where most real-world data-engineering work
happens: fixing inconsistent text, handling missing values, rejecting
bad rows, and calculating derived metrics.
"""

import pandas as pd


def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns a tuple of (clean_df, rejected_df) so bad records are never
    silently dropped -- they are logged for review instead.
    """
    df = df.copy()

    # 1. Trim whitespace and standardize casing on text columns
    df["customer_name"] = df["customer_name"].str.strip()
    df["product"] = df["product"].str.strip()
    df["region"] = df["region"].str.strip().str.title()

    # 2. Parse date column properly
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # 3. Flag invalid rows instead of guessing values for them:
    #    - missing customer name
    #    - non-positive quantity (data entry error, e.g. -2)
    #    - unparseable date
    is_valid = (
        df["customer_name"].notna()
        & (df["customer_name"] != "")
        & (df["quantity"] > 0)
        & df["order_date"].notna()
    )

    clean_df = df[is_valid].copy()
    rejected_df = df[~is_valid].copy()

    # 4. Derived column: total sale value per line item
    clean_df["total_amount"] = clean_df["quantity"] * clean_df["unit_price"]

    # 5. Column order/rename to match the target schema
    clean_df = clean_df[
        [
            "order_id",
            "customer_name",
            "region",
            "product",
            "quantity",
            "unit_price",
            "total_amount",
            "order_date",
        ]
    ]

    print(f"[TRANSFORM] {len(clean_df)} valid rows, {len(rejected_df)} rejected rows")
    return clean_df, rejected_df


if __name__ == "__main__":
    from extract import extract

    raw = extract()
    clean, rejected = transform(raw)
    print("\nClean sample:\n", clean.head())
    print("\nRejected rows:\n", rejected)
