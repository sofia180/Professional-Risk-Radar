import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Professional Risk Radar",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("📊 Professional Risk Radar")
st.markdown(
    """
    **MVP аналитической системы оценки рисков**  
    Загрузите CSV-файл и получите базовую аналитику и корреляции.
    """
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Управление")

uploaded_file = st.sidebar.file_uploader(
    "Загрузите CSV-файл",
    type=["csv"]
)

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file is None:
    st.info("⬅️ Загрузите CSV-файл через боковое меню")
    st.stop()

# -----------------------------
# LOAD DATA
# -----------------------------
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error("Ошибка при загрузке файла")
    st.exception(e)
    st.stop()

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("📋 Загруженные данные")
st.dataframe(df, use_container_width=True)

# -----------------------------
# BASIC INFO
# -----------------------------
st.subheader("ℹ️ Общая информация")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Строк", df.shape[0])

with col2:
    st.metric("Колонок", df.shape[1])

with col3:
    st.metric(
        "Числовых колонок",
        df.select_dtypes(include=np.number).shape[1]
    )

# -----------------------------
# DESCRIPTIVE STATS
# -----------------------------
numeric_df = df.select_dtypes(include=np.number)

if numeric_df.empty:
    st.warning("В файле нет числовых данных для анализа.")
    st.stop()

st.subheader("📈 Описательная статистика")
st.dataframe(
    numeric_df.describe().round(2),
    use_container_width=True
)

# -----------------------------
# CORRELATION
# -----------------------------
st.subheader("🔗 Корреляция показателей")

corr = numeric_df.corr()

st.dataframe(
    corr.round(2),
    use_container_width=True
)

# -----------------------------
# SIMPLE RISK SCORE (OPTIONAL)
# -----------------------------
st.subheader("⚠️ Простейший Risk Score (MVP)")

selected_columns = st.multiselect(
    "Выберите показатели для расчёта риска",
    options=numeric_df.columns.tolist()
)

if selected_columns:
    risk_score = numeric_df[selected_columns].mean(axis=1)

    result_df = df.copy()
    result_df["Risk_Score"] = risk_score.round(2)

    st.dataframe(
        result_df,
        use_container_width=True
    )

    st.success("Risk Score успешно рассчитан")
else:
    st.info("Выберите числовые колонки для расчёта Risk Score")

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Professional Risk Radar · MVP · Streamlit")
