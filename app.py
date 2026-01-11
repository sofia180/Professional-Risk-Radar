import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from risk_engine import calculate_risk_metrics
from report_generator import generate_report

# ----------------------------
# Настройка страницы
# ----------------------------
st.set_page_config(page_title="Professional Risk Radar", layout="wide")
st.title("🏦 Professional Risk Radar")
st.success("✅ App is running")

# ----------------------------
# Sidebar: загрузка CSV
# ----------------------------
st.sidebar.header("Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is None:
    st.info("👈 Upload a CSV file to start analysis")
    st.stop()

# ----------------------------
# Чтение CSV
# ----------------------------
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"❌ Error reading CSV: {e}")
    st.stop()

st.subheader("📄 Data Preview")
st.dataframe(df.head(), use_container_width=True)

# ----------------------------
# Выбор числовой колонки для анализа
# ----------------------------
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numeric_cols) == 0:
    st.error("❌ No numeric columns found in CSV")
    st.stop()

selected_col = st.selectbox("Select numeric column for risk analysis", numeric_cols)

# ----------------------------
# Расчёт риск-метрик через risk_engine
# ----------------------------
metrics = calculate_risk_metrics(df[selected_col])
st.subheader("📊 Risk Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Mean", round(metrics['mean'], 4))
with col2:
    st.metric("Std Dev", round(metrics['std'], 4))
with col3:
    st.metric("VaR (95%)", round(metrics['var_95'], 4))

# ----------------------------
# График распределения
# ----------------------------
st.subheader("📉 Distribution")
fig_hist = px.histogram(df, x=selected_col, nbins=50, title=f"Distribution of {selected_col}")
st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------------
# Временной ряд (если есть колонка даты)
# ----------------------------
date_cols = df.select_dtypes(include=["object"]).columns.tolist()
date_col = st.selectbox("Select date column (optional)", ["None"] + date_cols)
if date_col != "None":
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        df_sorted = df.sort_values(date_col)
        fig_ts = px.line(df_sorted, x=date_col, y=selected_col, title=f"{selected_col} over time")
        st.plotly_chart(fig_ts, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Cannot build time series: {e}")

# ----------------------------
# Генерация отчёта
# ----------------------------
st.subheader("📝 Generate Report")
if st.button("Generate CSV Report"):
    report_file = generate_report(df, selected_col)
    st.success(f"Report generated: {report_file}")
    st.download_button(
        label="Download Report",
        data=open(report_file, "rb").read(),
        file_name=report_file,
        mime="text/csv"
    )

st.divider()
st.caption("Professional Risk Radar MVP • Streamlit • Banking Prototype")
