import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from risk_engine import calculate_pd, calculate_lgd, calculate_ead, calculate_var, calculate_es, credit_score
from portfolio import portfolio_risk, correlation_matrix, stress_test
from report_generator import generate_report
from utils import clean_data, validate_data
from ml_models import train_linear_model, train_random_forest, predict, explain_model

st.set_page_config(page_title="Legendary Risk Radar", layout="wide")
st.title("🏦 Legendary Risk Radar")
st.success("✅ App is running")

# ----------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV/XLSX", type=["csv","xlsx"])
if uploaded_file is None:
    st.info("👈 Upload a file to start")
    st.stop()

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
tab1, tab2, tab3, tab4 = st.tabs(["Risk Metrics", "Portfolio", "ML Predictions", "Reports"])

# ----------------------------
with tab1:
    st.subheader("📊 Risk Metrics")
    selected_col = st.selectbox("Select numeric column", numeric_cols)
    metrics = {
        "PD": calculate_pd(df[selected_col]),
        "LGD": calculate_lgd(df[selected_col]),
        "EAD": calculate_ead(df[selected_col]),
        "VaR 95%": calculate_var(df[selected_col]),
        "Expected Shortfall": calculate_es(df[selected_col]),
        "Credit Score": credit_score(df[selected_col])
    }
    col1,col2,col3,col4,col5,col6 = st.columns(6)
    with col1: st.metric("PD", round(metrics["PD"],4))
    with col2: st.metric("LGD", round(metrics["LGD"],4))
    with col3: st.metric("EAD", round(metrics["EAD"],4))
    with col4: st.metric("VaR 95%", round(metrics["VaR 95%"],4))
    with col5: st.metric("ES", round(metrics["Expected Shortfall"],4))
    with col6: st.metric("Credit Score", round(metrics["Credit Score"],4))

    st.subheader("📉 Distribution")
    fig_hist = px.histogram(df, x=selected_col, nbins=50, title=f"Distribution of {selected_col}")
    st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------------
with tab2:
    st.subheader("📈 Portfolio Analysis")
    st.write(portfolio_risk(df[numeric_cols]))
    st.write("Correlation Matrix:")
    st.dataframe(correlation_matrix(df[numeric_cols]))
    st.subheader("⚠️ Stress Test Simulation")
    st.dataframe(stress_test(df[numeric_cols]))

# ----------------------------
with tab3:
    st.subheader("🤖 ML Risk Prediction")
    ml_target = st.selectbox("Select target column", numeric_cols)
    model_type = st.radio("Choose model", ["Linear Regression", "Random Forest"])
    
    if st.button("Train ML Model"):
        if model_type == "Linear Regression":
            results = train_linear_model(df, ml_target)
        else:
            results = train_random_forest(df, ml_target)
        
        st.success(f"Model trained! MSE: {results['mse']:.4f}, R²: {results['r2']:.4f}")
        pred_df = results['X_test'].copy()
        pred_df['True'] = results['y_test'].values
        pred_df['Predicted'] = results['y_pred']
        st.dataframe(pred_df.head(20))

        st.subheader("Feature Importance / Explainability")
        shap_values = explain_model(results['model'], results['X_test'])
        st.dataframe(shap_values)

# ----------------------------
with tab4:
    st.subheader("📝 Generate Report")
    if st.button("Generate Report"):
        report_file = generate_report(df, numeric_cols[0])
        st.success(f"Report generated: {report_file}")
        st.download_button("Download Report", data=open(report_file,"rb").read(),
                           file_name=report_file, mime="application/octet-stream")

st.caption("Legendary Risk Radar • Banking & Risk Analytics • ML Integrated • Streamlit Dashboard")
