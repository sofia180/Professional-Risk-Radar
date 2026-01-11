import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def prepare_data(df, target_col):
    # берём ТОЛЬКО числовые
    df_num = df.select_dtypes(include=[np.number]).copy()

    # target должен существовать
    if target_col not in df_num.columns:
        raise ValueError("Target column must be numeric")

    # удаляем строки с NaN
    df_num = df_num.dropna()

    X = df_num.drop(columns=[target_col])
    y = df_num[target_col]

    if X.empty:
        raise ValueError("No features available after preprocessing")

    return train_test_split(X, y, test_size=0.25, random_state=42)


def train_linear_model(df, target_col):
    X_train, X_test, y_train, y_test = prepare_data(df, target_col)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return {
        "model": model,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "mse": mean_squared_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred)
    }


def train_random_forest(df, target_col):
    X_train, X_test, y_train, y_test = prepare_data(df, target_col)

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return {
        "model": model,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "mse": mean_squared_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred)
    }
