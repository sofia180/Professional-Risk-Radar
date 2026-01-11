import pandas as pd

def clean_data(df):
    df = df.dropna()
    return df

def validate_data(df):
    if df.empty:
        raise ValueError("Dataframe is empty after cleaning")
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found")
