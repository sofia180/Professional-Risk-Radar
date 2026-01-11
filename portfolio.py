import pandas as pd
import numpy as np

def portfolio_risk(df):
    return {
        "Portfolio Mean": df.mean().mean(),
        "Portfolio Std": df.std().mean(),
        "Portfolio VaR 95%": np.percentile(df.values.flatten(), 5)
    }

def correlation_matrix(df):
    return df.corr()

def stress_test(df, shock=0.1):
    # Простая стресс-модель: -shock% на все позиции
    stressed = df * (1 - shock)
    return stressed.describe()
