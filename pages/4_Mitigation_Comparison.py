import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from model.train_model import train_and_evaluate
from fairness.fairness_metrics import calculate_fairness
from fairness.mitigation import apply_threshold_mitigation

st.set_page_config(
    page_title="Mitigation Comparison",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #ffffff !important;
}

[data-testid="stApp"] {
    background-color: #ffffff !important;
}

/* Top header */
header[data-testid="stHeader"] {
    background: #0f172a !important;
}

/* Sidebar full area */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar inner spacing */
section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

/* Navigation item container */
[data-testid="stSidebarNav"] {
    padding-top: 1rem !important;
}

/* Sidebar nav links */
[data-testid="stSidebarNav"] a {
    background: transparent !important;
    color: #e2e8f0 !important;
    padding: 12px 16px !important;
    margin: 6px 10px !important;
    border-radius: 12px !important;
    text-decoration: none !important;
    transition: all 0.2s ease-in-out !important;
    border-left: 4px solid transparent !important;
}

/* Hover effect */
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
    border-left: 4px solid #60a5fa !important;
}

/* Active page */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-left: 4px solid #3b82f6 !important;
}

/* Sidebar text */
[data-testid="stSidebarNav"] span {
    color: inherit !important;
    font-size: 17px !important;
}

/* Sidebar heading */
[data-testid="stSidebarNav"]::before {
    content: "☰ Navigation";
    display: block;
    font-size: 22px;
    font-weight: 800;
    color: white;
    margin: 0 14px 16px 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
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
    padding: 14px;
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

.final-box {
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
def get_all_results():
    results = train_and_evaluate()

    y_test = results["y_test"]
    sensitive_test = results["sensitive_test"]
    y_pred_before = results["y_pred"]
    y_prob = results["y_prob"]

    male_threshold = 0.50
    female_threshold = 0.30

    y_pred_after = apply_threshold_mitigation(
        y_prob,
        sensitive_test,
        male_threshold=male_threshold,
        female_threshold=female_threshold
    )

    fairness_before = calculate_fairness(y_test, y_pred_before, sensitive_test)
    fairness_after = calculate_fairness(y_test, y_pred_after, sensitive_test)

    metrics_before = {
        "accuracy": accuracy_score(y_test, y_pred_before),
        "precision": precision_score(y_test, y_pred_before, zero_division=0),
        "recall": recall_score(y_test, y_pred_before, zero_division=0),
        "f1": f1_score(y_test, y_pred_before, zero_division=0)
    }

    metrics_after = {
        "accuracy": accuracy_score(y_test, y_pred_after),
        "precision": precision_score(y_test, y_pred_after, zero_division=0),
        "recall": recall_score(y_test, y_pred_after, zero_division=0),
        "f1": f1_score(y_test, y_pred_after, zero_division=0)
    }

    return (
        metrics_before,
        metrics_after,
        fairness_before,
        fairness_after,
        female_threshold,
        male_threshold
    )

with st.spinner("Applying mitigation and comparing final results..."):
    (
        metrics_before,
        metrics_after,
        fairness_before,
        fairness_after,
        female_threshold,
        male_threshold
    ) = get_all_results()

acc_change = metrics_after["accuracy"] - metrics_before["accuracy"]
di_change = fairness_after["disparate_impact"] - fairness_before["disparate_impact"]

st.markdown("""
<div class="page-box">
    <div class="page-title">Mitigation Comparison</div>
    <div class="page-text">
        This final page compares model performance and fairness before and after applying threshold-based mitigation.
        It shows whether fairness improved while keeping predictive performance reasonably stable.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Key Result Cards</div>', unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="metric-title">Accuracy</div>
        <div class="metric-value">{metrics_before['accuracy']:.3f} → {metrics_after['accuracy']:.3f}</div>
        <div class="metric-sub">Change: {acc_change:+.3f}</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="metric-title">F1 Score</div>
        <div class="metric-value">{metrics_before['f1']:.3f} → {metrics_after['f1']:.3f}</div>
        <div class="metric-sub">Before vs After</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="metric-title">Disparate Impact</div>
        <div class="metric-value">{fairness_before['disparate_impact']:.3f} → {fairness_after['disparate_impact']:.3f}</div>
        <div class="metric-sub">Change: {di_change:+.3f}</div>
    </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
        <div class="metric-title">Thresholds Used</div>
        <div class="metric-value">F: {female_threshold:.2f} | M: {male_threshold:.2f}</div>
        <div class="metric-sub">Post-processing mitigation</div>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([1.15, 1])

with left:
    st.markdown('<div class="section-title">Comparison Table</div>', unsafe_allow_html=True)

    comparison_df = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "Male Selection Rate",
            "Female Selection Rate",
            "Disparate Impact",
            "Statistical Parity Difference",
            "Equal Opportunity Difference"
        ],
        "Before": [
            round(metrics_before["accuracy"], 4),
            round(metrics_before["precision"], 4),
            round(metrics_before["recall"], 4),
            round(metrics_before["f1"], 4),
            round(fairness_before["male_selection_rate"], 4),
            round(fairness_before["female_selection_rate"], 4),
            round(fairness_before["disparate_impact"], 4),
            round(fairness_before["statistical_parity_difference"], 4),
            round(fairness_before["equal_opportunity_difference"], 4)
        ],
        "After": [
            round(metrics_after["accuracy"], 4),
            round(metrics_after["precision"], 4),
            round(metrics_after["recall"], 4),
            round(metrics_after["f1"], 4),
            round(fairness_after["male_selection_rate"], 4),
            round(fairness_after["female_selection_rate"], 4),
            round(fairness_after["disparate_impact"], 4),
            round(fairness_after["statistical_parity_difference"], 4),
            round(fairness_after["equal_opportunity_difference"], 4)
        ]
    })

    st.markdown('<div class="table-box">', unsafe_allow_html=True)
    st.dataframe(comparison_df, use_container_width=True, height=360)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title">Metric Shift View</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(6.2, 4.3))

    labels = ["Accuracy", "F1", "DI", "SPD", "EOD"]
    before_vals = [
        metrics_before["accuracy"],
        metrics_before["f1"],
        fairness_before["disparate_impact"],
        fairness_before["statistical_parity_difference"],
        fairness_before["equal_opportunity_difference"]
    ]
    after_vals = [
        metrics_after["accuracy"],
        metrics_after["f1"],
        fairness_after["disparate_impact"],
        fairness_after["statistical_parity_difference"],
        fairness_after["equal_opportunity_difference"]
    ]
    colors = ["#1d4ed8", "#f97316", "#16a34a", "#dc2626", "#9467bd"]

    y_pos = list(range(len(labels)))

    for i in range(len(labels)):
        ax.plot(
            [before_vals[i], after_vals[i]],
            [y_pos[i], y_pos[i]],
            color=colors[i],
            linewidth=2.5,
            alpha=0.9
        )
        ax.scatter(before_vals[i], y_pos[i], color=colors[i], s=70, zorder=3)
        ax.scatter(after_vals[i], y_pos[i], color=colors[i], s=70, zorder=3)

        ax.text(before_vals[i], y_pos[i] + 0.12, f"{before_vals[i]:.3f}", fontsize=10)
        ax.text(after_vals[i], y_pos[i] - 0.18, f"{after_vals[i]:.3f}", fontsize=10)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_title("Before vs After Metric Shift", fontsize=15, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    min_x = min(before_vals + after_vals)
    max_x = max(before_vals + after_vals)
    ax.set_xlim(min_x - 0.08, max_x + 0.08)

    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Final Interpretation</div>', unsafe_allow_html=True)

if fairness_after["disparate_impact"] > fairness_before["disparate_impact"]:
    fairness_status = "Fairness improved after mitigation."
else:
    fairness_status = "Fairness did not improve clearly after mitigation."

if metrics_after["accuracy"] >= metrics_before["accuracy"] - 0.03:
    performance_status = "Model performance remained reasonably stable after mitigation."
else:
    performance_status = "Model performance dropped noticeably after mitigation."

st.markdown(f"""
<div class="insight-box">
<b>Fairness Decision:</b> {fairness_status}<br><br>
<b>Performance Decision:</b> {performance_status}<br><br>
<b>Conclusion:</b> Threshold-based post-processing mitigation was applied using different decision thresholds
for female and male groups. The final comparison helps determine whether bias reduction was achieved with only a limited trade-off in predictive performance.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="final-box">
    <h3 style="color:#1e3a8a; margin-bottom:8px;">Project Flow Completed</h3>
    <p style="color:#475569; font-size:16px; margin-bottom:0;">
        The project now presents dataset understanding, model performance, fairness analysis, and mitigation comparison in a complete sequence.
    </p>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.5, 2, 1.5])

with nav1:
    st.page_link("pages/3_Fairness_Analysis.py", label="← Back", use_container_width=True)

with nav2:
    st.page_link("app.py", label="Home", use_container_width=True)