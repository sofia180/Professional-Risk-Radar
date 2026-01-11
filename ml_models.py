import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def train_linear_model(df, target_col):
    """
    Обучает линейную модель (Linear Regression) для выбранной колонки target_col
    Возвращает модель и метрики качества
    """
    numeric_cols = df.select_dtypes(include=[float, int]).columns.tolist()
    if target_col not in numeric_cols:
        raise ValueError(f"{target_col} is not numeric")
    
    numeric_cols.remove(target_col)
    if len(numeric_cols) == 0:
        raise ValueError("Not enough features to train model")

    X = df[numeric_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    results = {
        "model": model,
        "mse": mse,
        "r2": r2,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred
    }
    return results

def predict(model, df_new):
    """
    Делает прогноз по новым данным
    """
    return model.predict(df_new)
