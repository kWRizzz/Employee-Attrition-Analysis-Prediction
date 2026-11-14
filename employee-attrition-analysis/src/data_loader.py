"""
data_loader.py
Loads the IBM HR Attrition dataset and prints a structured inspection report.
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read the CSV into a DataFrame. Fail with a clear message if missing."""
    if not Path(path).exists():
        raise FileNotFoundError(f"DataSet not found at :{path}")
    return pd.read_csv(path)


def inspect_data(df: pd.DataFrame) -> None:
    """Print everything we need to understand the dataset."""
    # Show all columns/wide tables instead of truncating with "..."
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print("=" * 70)
    print("1. SHAPE (rows, columns)")
    print(df.shape)

    print("\n" + "=" * 70)
    print("2. FIRST 5 ROWS")
    print(df.head())

    print("\n" + "=" * 70)
    print("3. COLUMN NAMES, DATA TYPES, NON-NULL COUNTS")
    df.info()

    print("\n" + "=" * 70)
    print("4. MISSING VALUES PER COLUMN")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print(f"Total missing values: {df.isnull().sum().sum()}")

    print("\n" + "=" * 70)
    print("5. DUPLICATE ROWS")
    print(df.duplicated().sum())

    print("\n" + "=" * 70)
    print("6. NUMBER OF UNIQUE VALUES PER COLUMN (sorted)")
    print(df.nunique().sort_values())

    print("\n" + "=" * 70)
    print("7. NUMERIC SUMMARY STATISTICS")
    print(df.describe().T)


    print("\n" + "=" * 70)
    
    print("8. TARGET VARIABLE: Attrition")
    if "Attrition" in df.columns:
        print(df["Attrition"].value_counts())
        print("\nPercentage:")
        print((df["Attrition"].value_counts(normalize=True) * 100).round(2))
    else:
        print("Column 'Attrition' not found!")


if __name__=="__main__":
    data=load_data()
    inspect_data(data)