import numpy as np

def calculate_risk_metrics(series):
    """
    Рассчитывает базовые риск-метрики для выбранной колонки:
    - Среднее
    - Стандартное отклонение
    - Value at Risk (5% percentile)
    """
    series = series.dropna()
    mean_val = series.mean()
    std_val = series.std()
    var_95 = np.percentile(series, 5)
    return {"mean": mean_val, "std": std_val, "var_95": var_95}
