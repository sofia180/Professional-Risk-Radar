import pandas as pd

def generate_report(df, column):
    filename = f"report_{column}.csv"
    df.to_csv(filename, index=False)
    return filename
