import pandas as pd
import numpy as np

def portfolio_risk(df_numeric):
    """
    Расчет основных метрик портфеля: среднее, стандартное отклонение, VaR 95%.
    """
    mean = df_numeric.mean().mean()
    std = df_numeric.std().mean()
    var_95 = np.percentile(df_numeric.values.flatten(), 5)
    return {
        "Portfolio Mean": mean,
        "Portfolio Std": std,
        "Portfolio VaR 95%": var_95
    }

def correlation_matrix(df_numeric):
    """
    Корреляционная матрица портфеля.
    """
    return df_numeric.corr()

def stress_scenario(df_numeric, shock_percent):
    """
    Симуляция стресс-сценария: уменьшение всех значений на shock_percent.
    """
    factor = 1 - shock_percent/100
    stressed_df = df_numeric * factor
    return stressed_df
