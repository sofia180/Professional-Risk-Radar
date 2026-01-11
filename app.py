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

st.set_page_config(page_title="Legendary Risk Radar", layout="wide")

# ----------------------------
# Белая тема для всей страницы
bg_color = "#FFFFFF"  # белый фон
text_color = "#000000" # черный текст

st.markdown(f"""
<style>
/* Основной фон */
.css-18e3th9 {{
    background-color: {bg_color};
}}
/* Sidebar и контейнеры */
.css-1d391kg, .css-1v0mbdj, .css-1kyxreq, .css-1gkcyyc {{
    background-color: {bg_color} !important;
    color: {text_color} !important;
}}
/* Кнопки */
.stButton>button {{
    background-color: #f0f2f6;
    color: {text_color};
}}
/* DataFrames */
.stDataFrame div {{
    background-color: {bg_color} !important;
    color: {text_color} !important;
}}
/* Заголовки */
h1, h2, h3, h4, h5, h6, .css-1v0mbdj, .css-1kyxreq {{
    color: {text_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
st.title("🏦 Legendary Risk Radar")
st.success("✅ App is running")

# ----------------------------
# Sidebar
shock_pct = st.sidebar.slider("Stress Shock %", 0, 50, 10)
uploaded_file = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv","xlsx"])

if uploaded_file is None:
    st.info("👈 Upload a file to start")
    st.stop()

# ----------------------------
# Read data
try:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error(f"❌ Error reading file: {e}")
    st.stop()

df = clean_data(df)
validate_data(df)

st.subheader("📄 Data Preview")
st.dataframe(df.head(), use_container_width=True)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numeric_cols) == 0:
    st.error("❌ No numeric columns found")
    st.stop()

# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Risk Metrics","Portfolio","ML Predictions","Reports"])

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
    cols = st.columns(6)
    for i, key in enumerate(metrics.keys()):
        cols[i].metric(key, round(metrics[key],4))

    fig_hist = px.histogram(df, x=selected_col, nbins=50, title=f"Distribution of {selected_col}")
    fig_hist.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font_color=text_color
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Tab 2: Portfolio
with tab2:
    port_metrics = portfolio_risk(df[numeric_cols])
    st.write(port_metrics)
    st.write("Correlation Matrix:")
    corr = correlation_matrix(df[numeric_cols])
    st.dataframe(corr.style.background_gradient(cmap='coolwarm'))

    st.subheader("⚠️ Stress Test Simulation")
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
        shap_values = explain_model(results['model'], results['X_test'])
        st.dataframe(shap_values)

# Tab 4: Reports
with tab4:
    if st.button("Generate Report"):
        report_file = generate_report(df, numeric_cols[0])
        st.success(f"Report generated: {report_file}")
        st.download_button("Download Report", data=open(report_file,"rb").read(),
                           file_name=report_file, mime="application/octet-stream")

st.caption(f"Legendary Risk Radar • Banking & Risk Analytics • ML Integrated • {datetime.now().year}")
