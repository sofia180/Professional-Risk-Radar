import pandas as pd
import numpy as np

def portfolio_risk(df):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return {"Portfolio Mean": np.nan, "Portfolio Std": np.nan, "Portfolio VaR 95%": np.nan}
    portfolio_mean = numeric_df.mean().mean()
    portfolio_std = numeric_df.std().mean()
    values = numeric_df.values.flatten()
    values = values[values != 0]
    portfolio_var_95 = np.percentile(values,5) if len(values)>0 else np.nan
    return {"Portfolio Mean":portfolio_mean,"Portfolio Std":portfolio_std,"Portfolio VaR 95%":portfolio_var_95}

def correlation_matrix(df):
    numeric_df = df.select_dtypes(include=[np.number])
    return numeric_df.corr() if not numeric_df.empty else pd.DataFrame()

def stress_test(df, shock=0.1):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame()
    stressed = numeric_df*(1-shock)
    return stressed.describe()

def stress_scenario(df, shock_pct=10):
    numeric_df = df.select_dtypes(include=[np.number])
    stressed_df = numeric_df * (1 - shock_pct/100)
    return stressed_df.describe()
