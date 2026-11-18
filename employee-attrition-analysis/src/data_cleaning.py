"""
data_cleaning.py
Cleans the raw HR dataset and saves a processed copy.
"""
import pandas as pd
from data_loader import load_data, PROJECT_ROOT

PROCESSED_PATH=PROJECT_ROOT/"data"/"processed"/"cleaned_attrition.csv"

# column identifierss
ID_COLUMNS=["EmployeeNumber"]

def cleaned_data(df: pd.Dataframe)-> pd.DataFrame:
    
    df=df.copy()
    
    # text triming 
    text_cols=df.select_dtypes(exclude="number").columns

    for col in text_cols:
        df[col]=df[col].str.strip()
    
    befor= len(df)
    
    df=df.drop_duplicate()
    # printing kitte abhi the and ab hain  after dropping 
    print("droped columns:-->" + befor-len(df))
    
    # no column value
    
    constant_cols= [c for c in df.columns if df[c].nunique()==1]
    print(f"Constant columns dropped: {constant_cols}")
    
     # 4. Drop constant columns and ID columns
    cols_to_drop= constant_cols + [c for c in ID_COLUMNS if c in df.columns]
     
      # 5. Create numeric target: Yes -> 1 (left), No -> 0 (stayed)
    df["AttritionFlag"]=df["Attrition"].map({"Yes":1, "No":0})
    if df["AttritionFlag"].isnull().any():
        raise ValueError("error  foun in Atrrition col")
    
    # print current df 
    print(df)
    
    return df
    
      
    