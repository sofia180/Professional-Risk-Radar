import numpy as np

def calculate_pd(series):
    # Probability of Default
    return np.clip(series.mean()/100, 0, 1)

def calculate_lgd(series):
    # Loss Given Default
    return np.clip(series.std()/100, 0, 1)

def calculate_ead(series):
    # Exposure at Default
    return series.max()

def calculate_var(series, confidence_level=95):
    # Value at Risk
    return np.percentile(series, 100 - confidence_level)

def calculate_es(series, confidence_level=95):
    # Expected Shortfall
    var = calculate_var(series, confidence_level)
    return series[series <= var].mean()

def credit_score(series):
    # Dummy scoring function: можно подключить ML модель
    mean = series.mean()
    std = series.std()
    score = np.clip(100 - std/mean*50, 0, 100)
    return score
