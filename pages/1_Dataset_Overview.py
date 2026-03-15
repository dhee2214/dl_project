import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dataset Overview",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PAGE STYLING ----------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background:
        radial-gradient(circle at top left, rgba(96, 165, 250, 0.18), transparent 24%),
        radial-gradient(circle at top right, rgba(168, 85, 247, 0.16), transparent 22%),
        radial-gradient(circle at bottom left, rgba(244, 114, 182, 0.10), transparent 20%),
        linear-gradient(180deg, #eef4ff 0%, #f8fbff 55%, #fcfcff 100%) !important;
    color: #0f172a;
}

[data-testid="stApp"] {
    background: transparent !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.6rem;
    padding-bottom: 2rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
}

/* Header */
header[data-testid="stHeader"] {
    background: rgba(255,255,255,0.0) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #172554 45%, #1e1b4b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebarNav"] {
    padding-top: 1rem !important;
}

[data-testid="stSidebarNav"]::before {
    content: "Project Navigation";
    display: block;
    font-size: 26px;
    font-weight: 800;
    color: white;
    margin: 0 14px 16px 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
}

[data-testid="stSidebarNav"] a {
    border-radius: 14px !important;
    margin: 7px 8px !important;
    padding: 12px 14px !important;
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.11) !important;
    transform: translateX(4px);
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899) !important;
    box-shadow: 0 10px 24px rgba(99, 102, 241, 0.32);
}

[data-testid="stSidebarNav"] span {
    color: inherit !important;
    font-size: 16px !important;
}

/* Top hero */
.page-hero {
    position: relative;
    overflow: hidden;
    border-radius: 32px;
    padding: 2.8rem 2.6rem 2.4rem 2.6rem;
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 28%, #7c3aed 68%, #ec4899 100%);
    box-shadow: 0 26px 56px rgba(59, 130, 246, 0.22);
    margin-bottom: 26px;
}

.page-hero::before {
    content: "";
    position: absolute;
    width: 320px;
    height: 320px;
    top: -110px;
    right: -70px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.22), rgba(255,255,255,0.03) 65%, transparent 76%);
}

.page-hero::after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    left: -50px;
    bottom: -90px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.18), rgba(255,255,255,0.03) 65%, transparent 78%);
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.20);
    color: white;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 16px;
    backdrop-filter: blur(12px);
}

.page-title {
    font-size: 46px;
    font-weight: 900;
    line-height: 1.1;
    color: white;
    margin-bottom: 14px;
    letter-spacing: -0.6px;
}

.page-text {
    font-size: 18px;
    color: rgba(255,255,255,0.93);
    line-height: 1.8;
    max-width: 900px;
}

/* Sections */
.section-title {
    font-size: 30px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 14px;
    letter-spacing: -0.4px;
}

.section-subtitle {
    font-size: 16px;
    color: #64748b;
    margin-top: -4px;
    margin-bottom: 18px;
    line-height: 1.75;
}

/* Intro note */
.note-box {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.7);
    box-shadow: 0 16px 30px rgba(148, 163, 184, 0.14);
    backdrop-filter: blur(14px);
    border-radius: 24px;
    padding: 22px;
    color: #334155;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 22px;
}

/* Metric cards */
.info-card {
    position: relative;
    overflow: hidden;
    padding: 22px;
    border-radius: 24px;
    color: white;
    text-align: left;
    box-shadow: 0 18px 35px rgba(15, 23, 42, 0.12);
    min-height: 140px;
}

.info-card::after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    top: -20px;
    right: -18px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
}

.info-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 12px;
    opacity: 0.96;
}

.info-value {
    font-size: 30px;
    font-weight: 900;
    line-height: 1.15;
}

/* Table box */
.table-box {
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(255,255,255,0.72);
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.14);
    backdrop-filter: blur(14px);
    border-radius: 24px;
    padding: 16px;
}

/* Chart box */
.chart-box {
    background: rgba(255,255,255,0.80);
    border: 1px solid rgba(255,255,255,0.72);
    padding: 18px;
    border-radius: 24px;
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.14);
    backdrop-filter: blur(14px);
    margin-top: 8px;
}

.chart-heading {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 10px;
}

/* Observation box */
.obs-box {
    background: linear-gradient(135deg, rgba(238,242,255,0.92), rgba(248,250,252,0.92));
    padding: 18px;
    border-radius: 18px;
    border-left: 5px solid #6366f1;
    color: #334155;
    font-size: 15px;
    line-height: 1.75;
    margin-top: 12px;
    box-shadow: 0 10px 24px rgba(148, 163, 184, 0.10);
}

/* Nav buttons */
[data-testid="stPageLink"] {
    text-align: center !important;
}

[data-testid="stPageLink"] a {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 55%, #ec4899 100%) !important;
    color: #ffffff !important;
    border-radius: 18px !important;
    padding: 14px 18px !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    text-decoration: none !important;
    box-shadow: 0 14px 28px rgba(99, 102, 241, 0.24) !important;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: #ffffff !important;
    margin: 0 !important;
}

/* Responsive */
@media (max-width: 700px) {
    .page-title {
        font-size: 32px;
    }
    .page-hero {
        padding: 2rem 1.4rem;
    }
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
<div class="page-hero">
    <div class="hero-badge">📁 Dataset Exploration</div>
    <div class="page-title">Dataset Overview</div>
    <div class="page-text">
        This page introduces the Adult Income dataset used in the project. It highlights the
        dataset structure, target variable, sensitive attribute, and data distribution so the user
        can understand the foundation before moving to model evaluation and fairness analysis.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- DATASET INFO ----------------
st.markdown('<div class="section-title">Dataset Information</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A quick understanding of what the dataset contains and why it matters in this project.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
The <b>Adult Income dataset</b> is widely used for classification tasks. In this project, the model predicts whether a person's income is
<b>greater than 50K</b> or <b>less than or equal to 50K</b>. The <b>income</b> column acts as the target variable, while <b>gender</b>
is treated as the sensitive attribute for fairness and bias analysis.
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
st.markdown('<div class="section-subtitle">A sample view of the first few records from the dataset.</div>', unsafe_allow_html=True)

st.markdown('<div class="table-box">', unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True, height=360)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHARTS ----------------
st.markdown('<div class="section-title">Dataset Visualizations</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Visual summaries to understand the distribution of gender and income categories.</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-heading">Gender Distribution</div>', unsafe_allow_html=True)

    gender_counts = df["gender"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(5.2, 5.2))
    ax1.pie(
        gender_counts.values,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.42, edgecolor="white"),
        colors=["#3b82f6", "#ec4899"]
    )
    ax1.set_title("Gender Share in Dataset", fontsize=14, fontweight="bold")
    st.pyplot(fig1)

    st.markdown(f"""
    <div class="obs-box">
        <b>Observation:</b> The dataset contains <b>{gender_counts.get("Male", 0)}</b> male records and
        <b>{gender_counts.get("Female", 0)}</b> female records. This helps identify whether the dataset
        is balanced across gender groups before fairness evaluation.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-heading">Income Distribution</div>', unsafe_allow_html=True)

    income_counts = df["income"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 5.2))
    bars = ax2.bar(income_counts.index, income_counts.values, color=["#60a5fa", "#34d399"], width=0.55)
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
        <b>Observation:</b> The dataset includes <b>{income_counts.iloc[0]}</b> records in one income class and
        <b>{income_counts.iloc[1]}</b> in the other. This helps us understand class imbalance, which can affect
        both predictive performance and fairness metrics.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- KEY DETAILS ----------------
st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Important takeaways from the dataset before moving to the next stage.</div>', unsafe_allow_html=True)

k1, k2 = st.columns(2)

with k1:
    st.markdown("""
    <div class="obs-box">
        <b>Target Variable:</b> The system predicts income category using demographic and work-related attributes,
        making the task a binary classification problem.
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="obs-box">
        <b>Fairness Focus:</b> Since gender is treated as the sensitive attribute, later pages compare model behaviour
        across male and female groups to identify possible bias.
    </div>
    """, unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
st.markdown("<br>", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.4, 2, 1.4])

with nav1:
    st.page_link("app.py", label="← Back to Home", use_container_width=True)

with nav3:
    st.page_link("pages/2_Model_Performance.py", label="Next →", use_container_width=True)