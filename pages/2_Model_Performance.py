# =========================
# STEP 1: IMPORT REQUIRED LIBRARIES
# Streamlit is used to build the web app interface
# Pandas is used for data handling and tables
# Matplotlib is used for charts and plots
# train_and_evaluate() is imported to train the model and get performance results
# =========================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model.train_model import train_and_evaluate


# =========================
# STEP 2: CONFIGURE PAGE SETTINGS
# This sets the page title, page layout,
# and keeps the sidebar expanded by default
# =========================
st.set_page_config(
    page_title="Model Performance",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# STEP 3: APPLY CUSTOM PAGE STYLING
# This CSS section is used to design the page
# with custom background, sidebar, hero section,
# metric cards, chart boxes, table boxes, and buttons
# =========================
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

/* Hero section */
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
    max-width: 920px;
}

/* Titles */
.section-title {
    font-size: 30px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 12px;
    letter-spacing: -0.4px;
}

.section-subtitle {
    font-size: 16px;
    color: #64748b;
    margin-top: -4px;
    margin-bottom: 18px;
    line-height: 1.75;
}

/* Metric cards */
.metric-card {
    position: relative;
    overflow: hidden;
    padding: 22px;
    border-radius: 24px;
    color: white;
    text-align: left;
    box-shadow: 0 18px 35px rgba(15, 23, 42, 0.12);
    min-height: 145px;
}

.metric-card::after {
    content: "";
    position: absolute;
    width: 110px;
    height: 110px;
    top: -20px;
    right: -18px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
}

.metric-title {
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 12px;
    opacity: 0.96;
}

.metric-value {
    font-size: 30px;
    font-weight: 900;
    line-height: 1.15;
}

.metric-sub {
    font-size: 14px;
    opacity: 0.95;
    margin-top: 10px;
    line-height: 1.5;
}

/* Glass boxes */
.chart-box, .table-box {
    background: rgba(255,255,255,0.80);
    border: 1px solid rgba(255,255,255,0.72);
    padding: 18px;
    border-radius: 24px;
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.14);
    backdrop-filter: blur(14px);
}

.chart-heading {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 10px;
}

/* Insight */
.insight-box {
    background: linear-gradient(135deg, rgba(238,242,255,0.92), rgba(248,250,252,0.92));
    padding: 20px;
    border-radius: 20px;
    border-left: 5px solid #6366f1;
    color: #334155;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 16px;
    box-shadow: 0 10px 24px rgba(148, 163, 184, 0.10);
}

/* Next section */
.next-box {
    margin-top: 22px;
    padding: 24px;
    border-radius: 26px;
    background: linear-gradient(135deg, #eef2ff, #fdf2f8);
    text-align: center;
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.14);
    border: 1px solid rgba(255,255,255,0.75);
}

.next-title {
    color: #1e3a8a;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 10px;
}

.next-text {
    color: #475569;
    font-size: 17px;
    line-height: 1.7;
}

/* Page buttons */
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


# =========================
# STEP 4: LOAD MODEL RESULTS
# Here we call the train_and_evaluate() function
# to train the model and return evaluation results
# st.cache_resource is used so training is not repeated
# every time the page reloads
# =========================
@st.cache_resource
def get_results():
    return train_and_evaluate()


# =========================
# STEP 5: TRAIN MODEL AND FETCH OUTPUTS
# A spinner is shown while the model is training
# and performance results are being loaded
# =========================
with st.spinner("Training model and loading performance results..."):
    results = get_results()


# =========================
# STEP 6: EXTRACT ALL RETURNED RESULTS
# We store all important outputs separately
# such as actual labels, predicted labels,
# accuracy, precision, recall, F1-score,
# confusion matrix, and classification report
# =========================
y_test = results["y_test"]
y_pred = results["y_pred"]
accuracy = results["accuracy"]
precision = results["precision"]
recall = results["recall"]
f1 = results["f1"]
cm = results["confusion_matrix"]
report = results["classification_report"]


# =========================
# STEP 7: CREATE HERO SECTION
# This is the top section of the page
# that explains what this page shows
# =========================
st.markdown("""
<div class="page-hero">
    <div class="hero-badge">📊 Performance Evaluation</div>
    <div class="page-title">Model Performance</div>
    <div class="page-text">
        This page presents how well the deep learning model performs on the Adult Income dataset.
        It includes the key evaluation metrics, confusion matrix, classification report, and sample
        predictions to understand model quality before checking fairness across gender groups.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# STEP 8: DISPLAY PERFORMANCE METRICS
# This section shows the main evaluation metrics:
# Accuracy, Precision, Recall, and F1-Score
# =========================
st.markdown('<div class="section-title">Performance Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Core evaluation metrics that describe how effectively the model makes predictions.</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="metric-title">Accuracy</div>
        <div class="metric-value">{accuracy:.4f}</div>
        <div class="metric-sub">Measures the overall correctness of predictions.</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="metric-title">Precision</div>
        <div class="metric-value">{precision:.4f}</div>
        <div class="metric-sub">Shows how reliable the positive predictions are.</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
        <div class="metric-title">Recall</div>
        <div class="metric-value">{recall:.4f}</div>
        <div class="metric-sub">Indicates how much of the positive class is captured.</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="metric-title">F1-Score</div>
        <div class="metric-value">{f1:.4f}</div>
        <div class="metric-sub">Balances precision and recall into one score.</div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# STEP 9: CREATE TWO COLUMNS
# Left side shows confusion matrix
# Right side shows classification report
# =========================
mid1, mid2 = st.columns([1.05, 1])


# =========================
# STEP 10: DISPLAY CONFUSION MATRIX
# This helps us compare actual values
# with predicted values visually
# =========================
with mid1:
    st.markdown('<div class="section-title">Confusion Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">A visual comparison of actual and predicted classes.</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(5.4, 4.3))
    im = ax.imshow(cm, cmap="Blues")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Predicted ≤50K", "Predicted >50K"], fontsize=10)
    ax.set_yticklabels(["Actual ≤50K", "Actual >50K"], fontsize=10)
    ax.set_title("Confusion Matrix", fontsize=14, fontweight="bold", pad=12)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j, i, str(cm[i, j]),
                ha="center", va="center",
                fontsize=13, fontweight="bold",
                color="black"
            )

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# STEP 11: DISPLAY CLASSIFICATION REPORT
# This table shows class-wise performance
# like precision, recall, F1-score, and support
# =========================
with mid2:
    st.markdown('<div class="section-title">Classification Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Detailed class-wise evaluation scores for the trained model.</div>', unsafe_allow_html=True)

    report_df = pd.DataFrame(report).transpose().round(4)

    st.markdown('<div class="table-box">', unsafe_allow_html=True)
    st.dataframe(report_df, use_container_width=True, height=340)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# STEP 12: SHOW SAMPLE PREDICTIONS
# This section displays a few actual values
# and predicted values from the test data
# so that users can directly compare them
# =========================
st.markdown('<div class="section-title">Sample Predictions</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A quick preview of actual and predicted outcomes from the test set.</div>', unsafe_allow_html=True)

sample_count = 8
actual_values = y_test[:sample_count].values if hasattr(y_test, "values") else y_test[:sample_count]

sample_df = pd.DataFrame({
    "Actual Income": actual_values,
    "Predicted Income": y_pred[:sample_count]
})

st.markdown('<div class="table-box">', unsafe_allow_html=True)
st.dataframe(sample_df, use_container_width=True, height=240)
st.markdown('</div>', unsafe_allow_html=True)


# =========================
# STEP 13: DISPLAY FINAL INSIGHT
# This section explains that good performance
# does not always mean the model is fair
# =========================
st.markdown("""
<div class="insight-box">
<b>Insight:</b> The model demonstrates good predictive capability through accuracy, precision, recall, and F1-score.
Still, strong performance alone does not confirm fairness. A model can perform well overall and yet produce unequal
outcomes across different gender groups. That is why the next stage focuses on fairness analysis.
</div>
""", unsafe_allow_html=True)


# =========================
# STEP 14: SHOW NEXT PAGE MESSAGE
# This section tells the user to continue
# to the fairness analysis page
# =========================
st.markdown("""
<div class="next-box">
    <div class="next-title">Ready for Fairness Analysis?</div>
    <div class="next-text">
        Continue to the next page to compare outcomes across gender groups using fairness metrics
        and identify whether any bias exists in the model.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# STEP 15: ADD NAVIGATION BUTTONS
# These buttons help the user
# move to previous or next page
# =========================
st.markdown("<br>", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.4, 2, 1.4])

with nav1:
    st.page_link("pages/1_Dataset_Overview.py", label="← Back", use_container_width=True)

with nav3:
    st.page_link("pages/3_Fairness_Analysis.py", label="Next →", use_container_width=True)