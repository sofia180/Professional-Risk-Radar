def portfolio_risk(df):
    """
    Рассчитывает базовые метрики портфеля с учетом всех числовых колонок
    """
    # Средние значения по портфелю
    portfolio_mean = df.mean().mean()
    portfolio_std = df.std().mean()
    
    # Value at Risk 95% (по отрицательным изменениям)
    # Берём все значения, считаем 5-й процентиль отрицательных изменений
    values = df.values.flatten()
    values = values[values != 0]  # убираем нули
    portfolio_var_95 = np.percentile(values, 5) if len(values) > 0 else np.nan
    
    return {
        "Portfolio Mean": portfolio_mean,
        "Portfolio Std": portfolio_std,
        "Portfolio VaR 95%": portfolio_var_95
    }
