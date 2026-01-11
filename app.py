import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

from risk_engine import calculate_pd, calculate_lgd, calculate_ead, calculate_var, calculate_es, credit_score
from portfolio import portfolio_risk, correlation_matrix, stress_scenario
from report_generator import generate_report
from utils import clean_data, validate_data
from ml_models import train_linear_model, train_random_forest, explain_model
from history import save_portfolio_history

# ----------------------------
# Настройка страницы
st.set_page_config(page_title="Legendary Financial Risk Radar", layout="wide")
st.title("🏦 Legendary Financial Risk Radar")
st.success("✅ App is running")

# ----------------------------
# Sidebar
shock_pct = st.sidebar.slider("Stress Shock %", 0, 50, 10)
uploaded_file = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv","xlsx"])

# Проверка загрузки файла
if uploaded_file is None:
    st.info("👈 Upload a CSV or XLSX file to start")
    st.stop()

# Чтение файла
try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"❌ Error reading file: {e}")
    st.stop()

# Очистка и проверка данных
df = clean_data(df)
validate_data(df)

# Превью данных
st.subheader("📄 Data Preview")
st.dataframe(df.head(), use_container_width=True)

# Определение числовых колонок
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
st.write("Numeric columns detected:", numeric_cols)
if len(numeric_cols) == 0:
    st.error("❌ No numeric columns found. Please upload a file with numeric data.")
    st.stop()

# ----------------------------
# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Risk Metrics","Portfolio","ML Predictions","Scenario Simulation","Reports"])

# Tab 1: Risk Metrics
with tab1:
    selected_col = st.selectbox("Select numeric column", numeric_cols)
    metrics = {
        "PD": calculate_pd(df[selected_col]),
        "LGD": calculate_lgd(df[selected_col]),
        "EAD": calculate_ead(df[selected_col]),
        "VaR 95%": calculate_var(df[selected_col]),
        "Expected Shortfall": calculate_es(df[selected_col]),
        "Credit Score": credit_score(df[selected_col])
    }
    cols = st.columns(len(metrics))
    for i, key in enumerate(metrics.keys()):
        cols[i].metric(key, round(metrics[key],4))

    # Гистограмма распределения
    fig_hist = px.histogram(df, x=selected_col, nbins=50, title=f"Distribution of {selected_col}")
    st.plotly_chart(fig_hist, use_container_width=True)

# Tab 2: Portfolio
with tab2:
    port_metrics = portfolio_risk(df[numeric_cols])
    st.write(port_metrics)
    st.write("Correlation Matrix:")
    corr = correlation_matrix(df[numeric_cols])
    st.dataframe(corr.style.background_gradient(cmap='coolwarm'))

    st.subheader(f"⚠️ Stress Test Simulation ({shock_pct}% shock)")
    stressed = stress_scenario(df[numeric_cols], shock_pct)
    st.dataframe(stressed)

    save_portfolio_history(port_metrics)

# Tab 3: ML Predictions
with tab3:
    ml_target = st.selectbox("Select target column", numeric_cols)
    model_type = st.radio("Choose model", ["Linear Regression", "Random Forest"])
    if st.button("Train ML Model"):
        results = train_linear_model(df, ml_target) if model_type=="Linear Regression" else train_random_forest(df, ml_target)
        st.success(f"Model trained! MSE: {results['mse']:.4f}, R²: {results['r2']:.4f}")
        pred_df = results['X_test'].copy()
        pred_df['True'] = results['y_test'].values
        pred_df['Predicted'] = results['y_pred']
        st.dataframe(pred_df.head(20))

        # SHAP объяснение
        shap_values = explain_model(results['model'], results['X_test'])
        st.subheader("SHAP values (feature impact)")
        st.dataframe(shap_values.head(20))

# Tab 4: Scenario Simulation
with tab4:
    st.subheader("📊 Monte Carlo Simulation")
    simulations = 1000
    mc_portfolio = []
    for _ in range(simulations):
        sample = df[numeric_cols].sample(frac=1, replace=True)
        mc_portfolio.append(sample.mean().mean())
    st.line_chart(mc_portfolio, use_container_width=True)

    st.subheader(f"⚠️ Shock Scenario ({shock_pct}% reduction)")
    shocked = df[numeric_cols]*(1-shock_pct/100)
    st.dataframe(shocked)

# Tab 5: Reports
with tab5:
    if st.button("Generate Report"):
        report_file = generate_report(df, numeric_cols[0])
        st.success(f"Report generated: {report_file}")
        with open(report_file, "r_
