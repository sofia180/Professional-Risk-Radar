import numpy as np

def calculate_pd(series):
    return (series <= 0).mean()

def calculate_lgd(series):
    losses = series[series < 0]
    return abs(losses.mean()) if len(losses) > 0 else 0

def calculate_ead(series):
    return series.mean()

def calculate_var(series, confidence_level=0.95):
    return np.percentile(series, 100*(1-confidence_level))

def calculate_es(series, confidence_level=0.95):
    var = calculate_var(series, confidence_level)
    return series[series <= var].mean()

def credit_score(series):
    normalized = (series - series.min()) / (series.max() - series.min() + 1e-9)
    score = 300 + normalized * 550
    return score.mean()
