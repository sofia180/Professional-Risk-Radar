def generate_report(df, column):
    """
    Генерация CSV отчёта с данными и выбранной колонкой для анализа
    """
    filename = f"report_{column}.csv"
    df.to_csv(filename, index=False)
    return filename
