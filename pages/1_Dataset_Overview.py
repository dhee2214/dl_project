import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dataset Overview", layout="wide")

# ---------------- PAGE STYLING ----------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #ffffff !important;
}

[data-testid="stApp"] {
    background-color: #ffffff !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

[data-testid="stPageLink"] {
    text-align: center !important;
}

[data-testid="stPageLink"] a {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22) !important;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: #ffffff !important;
    margin: 0 !important;
}

.page-box {
    background: linear-gradient(135deg, #eff6ff, #f0fdf4);
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #dbeafe;
    margin-bottom: 25px;
}

.page-title {
    font-size: 38px;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 10px;
}

.page-text {
    font-size: 18px;
    color: #475569;
    line-height: 1.7;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
    margin-top: 25px;
    margin-bottom: 15px;
}

.note-box {
    background: #f8fafc;
    border-left: 5px solid #2563eb;
    padding: 18px;
    border-radius: 14px;
    color: #334155;
    margin-bottom: 20px;
    font-size: 16px;
    line-height: 1.6;
}

.info-card {
    padding: 20px;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.info-title {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 8px;
}

.info-value {
    font-size: 22px;
    font-weight: 800;
}

.chart-box {
    background: #ffffff;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
    margin-top: 10px;
}

.obs-box {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    padding: 18px;
    border-radius: 16px;
    border-left: 5px solid #4f46e5;
    color: #334155;
    font-size: 15px;
    line-height: 1.6;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA LOADING ----------------
columns = [
    "age", "workclass", "fnlwgt", "education", "education_num", "marital_status",
    "occupation", "relationship", "race", "gender", "capital_gain", "capital_loss",
    "hours_per_week", "native_country", "income"
]

@st.cache_data
def load_data():
    df = pd.read_csv("data/adult.data", names=columns, sep=",", skipinitialspace=True)
    return df

df = load_data()

# ---------------- HEADER ----------------
st.markdown("""
<div class="page-box">
    <div class="page-title">Dataset Overview</div>
    <div class="page-text">
        This page presents the Adult Income dataset used in our fairness analysis project.
        It provides a quick understanding of the dataset structure, target variable,
        sensitive attribute, and class distributions before moving to model training
        and fairness evaluation.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- DATASET INFO ----------------
st.markdown('<div class="section-title">Dataset Information</div>', unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
The Adult Income dataset is commonly used for classification tasks. In this project,
the model predicts whether a person's income is greater than 50K or less than or equal to 50K.
The <b>income</b> column is the target variable, and <b>gender</b> is considered the sensitive attribute
for fairness and bias analysis.
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="info-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="info-title">Total Rows</div>
        <div class="info-value">{df.shape[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="info-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="info-title">Total Columns</div>
        <div class="info-value">{df.shape[1]}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="info-card" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
        <div class="info-title">Target Variable</div>
        <div class="info-value">Income</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="info-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="info-title">Sensitive Attribute</div>
        <div class="info-value">Gender</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- DATA PREVIEW ----------------
st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

# ---------------- CHARTS ----------------
st.markdown('<div class="section-title">Dataset Visualizations</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("Gender Distribution")

    gender_counts = df["gender"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax1.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.45, edgecolor="white")
    )
    ax1.set_title("Gender Share in Dataset", fontsize=14, fontweight="bold")
    st.pyplot(fig1)

    st.markdown(f"""
    <div class="obs-box">
        <b>Observation:</b> The dataset contains <b>{gender_counts.get("Male", 0)}</b> male records
        and <b>{gender_counts.get("Female", 0)}</b> female records. This visualization helps identify
        whether the dataset is balanced across gender groups before fairness evaluation.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.subheader("Income Distribution")

    income_counts = df["income"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 5))
    bars = ax2.bar(income_counts.index, income_counts.values, color=["#60a5fa", "#34d399"])
    ax2.set_title("Income Class Distribution", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Income Category")
    ax2.set_ylabel("Number of Records")

    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height + 300,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    st.pyplot(fig2)

    st.markdown(f"""
    <div class="obs-box">
        <b>Observation:</b> The dataset includes <b>{income_counts.iloc[0]}</b> records in one income class
        and <b>{income_counts.iloc[1]}</b> in the other. This helps us understand class imbalance,
        which can influence both prediction performance and fairness metrics.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- KEY DETAILS ----------------
st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

k1, k2 = st.columns(2)

with k1:
    st.markdown("""
    <div class="obs-box">
        <b>Target Variable:</b> The project predicts income category using demographic and work-related attributes.
        This makes the task a binary classification problem.
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="obs-box">
        <b>Fairness Focus:</b> Since gender is treated as the sensitive attribute, later pages will compare
        model behaviour across male and female groups to detect any bias.
    </div>
    """, unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
st.markdown("<br>", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.5, 2, 1.5])

with nav1:
    st.page_link("app.py", label="← Back to Home", use_container_width=True)

with nav3:
    st.page_link("pages/2_Model_Performance.py", label="Next →", use_container_width=True)