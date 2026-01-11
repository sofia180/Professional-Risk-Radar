import pandas as pd

def clean_data(df):
    # Простая очистка: убрать дубликаты и NaN
    df = df.drop_duplicates()
    df = df.fillna(0)
    return df

def validate_data(df):
    if df.empty:
        raise ValueError("Dataframe is empty after cleaning")
    if df.shape[1] < 1:
        raise ValueError("Dataframe has no columns")
