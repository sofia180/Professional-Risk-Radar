import pandas as pd
import numpy as np

def portfolio_risk(df):
    """
    Рассчитывает базовые метрики портфеля по всем числовым колонкам:
    - Среднее по портфелю
    - Среднее стандартное отклонение
    - Value at Risk 95% (по всем значениям портфеля)
    """
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        return {
            "Portfolio Mean": np.nan,
            "Portfolio Std": np.nan,
            "Portfolio VaR 95%": np.nan
        }

    portfolio_mean = numeric_df.mean().mean()
    portfolio_std = numeric_df.std().mean()
    
    # Flatten all values, убираем нули для более реалистичного VaR
    values = numeric_df.values.flatten()
    values = values[values != 0]
    portfolio_var_95 = np.percentile(values, 5) if len(values) > 0 else np.nan
    
    return {
        "Portfolio Mean": portfolio_mean,
        "Portfolio Std": portfolio_std,
        "Portfolio VaR 95%": portfolio_var_95
    }

def correlation_matrix(df):
    """
    Корреляционная матрица между числовыми колонками портфеля
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.corr()

def stress_test(df, shock=0.1):
    """
    Простая стресс-модель:
    - shock: процент снижения всех значений (например, 0.1 = -10%)
    Возвращает описание портфеля после шока.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame()
    
    stressed = numeric_df * (1 - shock)
    return stressed.describe()
