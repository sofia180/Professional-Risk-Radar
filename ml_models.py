import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import shap

def train_linear_model(df, target_col):
    numeric_cols = df.select_dtypes(include=[float,int]).columns.tolist()
    numeric_cols.remove(target_col)
    X = df[numeric_cols]
    y = df[target_col]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = LinearRegression()
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test,y_pred)
    r2 = r2_score(y_test,y_pred)
    return {"model":model,"mse":mse,"r2":r2,"X_test":X_test,"y_test":y_test,"y_pred":y_pred}

def train_random_forest(df, target_col):
    numeric_cols = df.select_dtypes(include=[float,int]).columns.tolist()
    numeric_cols.remove(target_col)
    X = df[numeric_cols]
    y = df[target_col]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test,y_pred)
    r2 = r2_score(y_test,y_pred)
    return {"model":model,"mse":mse,"r2":r2,"X_test":X_test,"y_test":y_test,"y_pred":y_pred}

def predict(model, df_new):
    return model.predict(df_new)

def explain_model(model, X_test):
    explainer = shap.Explainer(model, X_test)
    shap_values = explainer(X_test)
    return pd.DataFrame(shap_values.values, columns=X_test.columns)
