import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model.train_model import train_and_evaluate

st.set_page_config(page_title="Model Performance", layout="wide")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #ffffff !important;
}

[data-testid="stApp"] {
    background-color: #ffffff !important;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 1.4rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
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
    border-radius: 12px !important;
    padding: 10px 14px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.20) !important;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: #ffffff !important;
    margin: 0 !important;
}

.page-box {
    background: linear-gradient(135deg, #eff6ff, #f0fdf4);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    margin-bottom: 16px;
}

.page-title {
    font-size: 32px;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 8px;
}

.page-text {
    font-size: 16px;
    color: #475569;
    line-height: 1.6;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    color: #111827;
    margin-top: 14px;
    margin-bottom: 10px;
}

.metric-card {
    padding: 16px;
    border-radius: 16px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    min-height: 96px;
}

.metric-title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 20px;
    font-weight: 800;
}

.metric-sub {
    font-size: 12px;
    opacity: 0.95;
    margin-top: 4px;
}

.chart-box {
    background: #ffffff;
    padding: 12px;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
}

.table-box {
    background: #ffffff;
    padding: 12px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
}

.insight-box {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    padding: 14px;
    border-radius: 14px;
    border-left: 5px solid #4f46e5;
    color: #334155;
    font-size: 14px;
    line-height: 1.6;
}

.next-box {
    margin-top: 14px;
    padding: 18px;
    border-radius: 18px;
    background: linear-gradient(135deg, #eef2ff, #fdf2f8);
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_results():
    return train_and_evaluate()

with st.spinner("Training model and loading performance results..."):
    results = get_results()

y_test = results["y_test"]
y_pred = results["y_pred"]
accuracy = results["accuracy"]
precision = results["precision"]
recall = results["recall"]
f1 = results["f1"]
cm = results["confusion_matrix"]
report = results["classification_report"]

st.markdown("""
<div class="page-box">
    <div class="page-title">Model Performance</div>
    <div class="page-text">
        This page presents the predictive performance of the deep learning model on the Adult Income dataset.
        Along with accuracy, it also includes precision, recall, F1-score, confusion matrix, and classification results
        to give a fuller picture of model quality before fairness evaluation.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Performance Summary</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="metric-title">Accuracy</div>
        <div class="metric-value">{accuracy:.4f}</div>
        <div class="metric-sub">Overall correctness</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="metric-title">Precision</div>
        <div class="metric-value">{precision:.4f}</div>
        <div class="metric-sub">Positive prediction quality</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
        <div class="metric-title">Recall</div>
        <div class="metric-value">{recall:.4f}</div>
        <div class="metric-sub">Positive class coverage</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="metric-title">F1-Score</div>
        <div class="metric-value">{f1:.4f}</div>
        <div class="metric-sub">Balanced performance</div>
    </div>
    """, unsafe_allow_html=True)

mid1, mid2 = st.columns([1.05, 1])

with mid1:
    st.markdown('<div class="section-title">Confusion Matrix</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(5.2, 4.0))
    im = ax.imshow(cm, cmap="Blues")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred 0", "Pred 1"])
    ax.set_yticklabels(["Actual 0", "Actual 1"])
    ax.set_title("Confusion Matrix", fontsize=13, fontweight="bold")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=12, fontweight="bold")

    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with mid2:
    st.markdown('<div class="section-title">Classification Report</div>', unsafe_allow_html=True)

    report_df = pd.DataFrame(report).transpose()
    report_df = report_df.round(4)

    st.markdown('<div class="table-box">', unsafe_allow_html=True)
    st.dataframe(report_df, use_container_width=True, height=320)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Sample Predictions</div>', unsafe_allow_html=True)

sample_count = 8
actual_values = y_test[:sample_count].values if hasattr(y_test, "values") else y_test[:sample_count]

sample_df = pd.DataFrame({
    "Actual Income": actual_values,
    "Predicted Income": y_pred[:sample_count]
})

st.markdown('<div class="table-box">', unsafe_allow_html=True)
st.dataframe(sample_df, use_container_width=True, height=220)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>Insight:</b> The model shows its predictive capability through accuracy, precision, recall, and F1-score.
However, strong performance alone does not guarantee fairness. A model can still perform well overall while producing
unequal outcomes for different gender groups. The next page will examine whether such bias exists.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="next-box">
    <h3 style="color:#1e3a8a; margin-bottom:8px;">Proceed to Fairness Analysis</h3>
    <p style="color:#475569; font-size:16px; margin-bottom:0;">
        Move to the next page to compare outcomes across gender groups using fairness metrics.
    </p>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.5, 2, 1.5])

with nav1:
    st.page_link("pages/1_Dataset_Overview.py", label="← Back", use_container_width=True)

with nav3:
    st.page_link("pages/3_Fairness_Analysis.py", label="Next →", use_container_width=True)