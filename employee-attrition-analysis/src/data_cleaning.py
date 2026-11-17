"""
data_cleaning.py
Cleans the raw HR dataset and saves a processed copy.
"""

import pandas as pd
from data_loader import load_data, PROJECT_ROOT

PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_attrition.csv"

# Columns that are identifiers (no predictive meaning)
ID_COLUMNS = ["EmployeeNumber"]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the dataset. The original is not modified."""
    df = df.copy()

    # 1. Remove stray spaces from text columns (e.g. "Yes " vs "Yes")
    text_cols = df.select_dtypes(exclude="number").columns
    for col in text_cols:
        df[col] = df[col].str.strip()

    # 2. Remove exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    print(f"Duplicates removed: {before - len(df)}")

    # 3. Find columns with only one unique value (carry no information)
    constant_cols = [c for c in df.columns if df[c].nunique() == 1]
    print(f"Constant columns dropped: {constant_cols}")

    # 4. Drop constant columns and ID columns
    cols_to_drop = constant_cols + [c for c in ID_COLUMNS if c in df.columns]
    df = df.drop(columns=cols_to_drop)
    print(f"ID columns dropped: {ID_COLUMNS}")

    # 5. Create numeric target: Yes -> 1 (left), No -> 0 (stayed)
    df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})
    if df["AttritionFlag"].isnull().any():
        raise ValueError("Unexpected values found in Attrition column")

    return df


def save_clean_data(df: pd.DataFrame) -> None:
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Cleaned data saved to: {PROCESSED_PATH}")


if __name__ == "__main__":
    raw = load_data()
    print(f"Raw shape: {raw.shape}\n")

    cleaned = clean_data(raw)

    print(f"\nCleaned shape: {cleaned.shape}")
    print(f"Remaining missing values: {cleaned.isnull().sum().sum()}")
    print("\nAttritionFlag counts:")
    print(cleaned["AttritionFlag"].value_counts())
    print("\nRemaining columns:")
    print(list(cleaned.columns))

    save_clean_data(cleaned)
    
    
    