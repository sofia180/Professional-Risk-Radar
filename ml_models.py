import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import shap

def train_linear_model(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
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
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
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

def explain_model(model, X_test):
    """
    Возвращает SHAP значения для объяснения модели.
    """
    explainer = shap.Explainer(model, X_test)
    shap_values = explainer(X_test)
    shap_df = pd.DataFrame(shap_values.values, columns=X_test.columns)
    return shap_df
