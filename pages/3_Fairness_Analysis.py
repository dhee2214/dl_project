import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model.train_model import train_and_evaluate
from fairness.fairness_metrics import calculate_fairness

st.set_page_config(page_title="Fairness Analysis", layout="wide")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #ffffff !important;
}

[data-testid="stApp"] {
    background-color: #ffffff !important;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.2rem;
    padding-left: 2.0rem;
    padding-right: 2.0rem;
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
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    margin-bottom: 14px;
}

.page-title {
    font-size: 30px;
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 8px;
}

.page-text {
    font-size: 15px;
    color: #475569;
    line-height: 1.6;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-top: 12px;
    margin-bottom: 8px;
}

.metric-card {
    padding: 15px;
    border-radius: 16px;
    color: white;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    min-height: 92px;
}

.metric-title {
    font-size: 14px;
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

.final-box {
    margin-top: 12px;
    padding: 16px;
    border-radius: 18px;
    background: linear-gradient(135deg, #eef2ff, #fdf2f8);
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_fairness_results():
    results = train_and_evaluate()
    y_test = results["y_test"]
    sensitive_test = results["sensitive_test"]
    y_pred = results["y_pred"]
    fairness_results = calculate_fairness(y_test, y_pred, sensitive_test)
    return fairness_results

with st.spinner("Calculating fairness metrics and loading analysis..."):
    fairness_results = get_fairness_results()

male_rate = fairness_results["male_selection_rate"]
female_rate = fairness_results["female_selection_rate"]
disparate_impact = fairness_results["disparate_impact"]
spd = fairness_results["statistical_parity_difference"]
male_accuracy = fairness_results["male_accuracy"]
female_accuracy = fairness_results["female_accuracy"]
male_tpr = fairness_results["male_tpr"]
female_tpr = fairness_results["female_tpr"]
eod = fairness_results["equal_opportunity_difference"]

selection_gap = abs(male_rate - female_rate)

st.markdown("""
<div class="page-box">
    <div class="page-title">Fairness Analysis</div>
    <div class="page-text">
        This page evaluates whether the trained model produces balanced outcomes across male and female groups.
        It focuses on selection rate comparison, disparate impact, statistical parity difference, and equal opportunity difference.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Fairness Summary</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="metric-title">Male Selection Rate</div>
        <div class="metric-value">{male_rate:.4f}</div>
        <div class="metric-sub">Positive outcomes for males</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #ec4899, #db2777);">
        <div class="metric-title">Female Selection Rate</div>
        <div class="metric-value">{female_rate:.4f}</div>
        <div class="metric-sub">Positive outcomes for females</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="metric-title">Disparate Impact</div>
        <div class="metric-value">{disparate_impact:.4f}</div>
        <div class="metric-sub">Target fairness threshold: 0.80</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="metric-title">SPD</div>
        <div class="metric-value">{spd:.4f}</div>
        <div class="metric-sub">Selection rate difference</div>
    </div>
    """, unsafe_allow_html=True)

v1, v2 = st.columns(2)

with v1:
    st.markdown('<div class="section-title">Selection Rate Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig1, ax1 = plt.subplots(figsize=(6.3, 3.2))

    groups = ["Female", "Male"]
    values = [female_rate, male_rate]
    colors = ["#ec4899", "#3b82f6"]
    y_positions = [0, 1]

    ax1.hlines(y=y_positions, xmin=0, xmax=values, color=colors, linewidth=5, alpha=0.9)
    ax1.scatter(values, y_positions, s=420, color=colors, zorder=3)

    for i, val in enumerate(values):
        ax1.text(val + 0.012, y_positions[i], f"{val:.3f}", va="center", fontsize=11, fontweight="bold")

    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(groups, fontsize=11)
    ax1.set_xlim(0, max(0.38, max(values) + 0.10))
    ax1.set_xlabel("Selection Rate", fontsize=10)
    ax1.set_title("Gender-wise Positive Outcome Rate", fontsize=14, fontweight="bold")
    ax1.grid(axis="x", linestyle="--", alpha=0.25)

    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)

    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

with v2:
    st.markdown('<div class="section-title">Disparate Impact Threshold Check</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(6.3, 3.2))

    current_value = min(disparate_impact, 1.0)

    ax2.hlines(y=0, xmin=0, xmax=1.0, color="#e5e7eb", linewidth=14)
    ax2.hlines(y=0, xmin=0, xmax=current_value, color="#8b5cf6", linewidth=14)
    ax2.scatter([current_value], [0], s=260, color="#7c3aed", zorder=3)
    ax2.axvline(x=0.8, color="#ef4444", linestyle="--", linewidth=2)

    ax2.text(current_value, 0.12, f"{disparate_impact:.3f}", ha="center", fontsize=12, fontweight="bold")
    ax2.text(0.8, -0.18, "0.80 threshold", ha="center", fontsize=10, color="#ef4444", fontweight="bold")

    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(-0.28, 0.28)
    ax2.set_yticks([])
    ax2.set_xlabel("Disparate Impact", fontsize=10)
    ax2.set_title("Fairness Threshold View", fontsize=14, fontweight="bold")

    for spine in ["top", "right", "left"]:
        ax2.spines[spine].set_visible(False)

    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

bottom_left, bottom_right = st.columns([1.15, 0.85])

with bottom_left:
    st.markdown('<div class="section-title">Fairness Metric Table</div>', unsafe_allow_html=True)

    fairness_df = pd.DataFrame({
        "Metric": [
            "Male Selection Rate",
            "Female Selection Rate",
            "Selection Rate Gap",
            "Disparate Impact",
            "Statistical Parity Difference",
            "Male Accuracy",
            "Female Accuracy",
            "Male TPR",
            "Female TPR",
            "Equal Opportunity Difference"
        ],
        "Value": [
            round(male_rate, 4),
            round(female_rate, 4),
            round(selection_gap, 4),
            round(disparate_impact, 4),
            round(spd, 4),
            round(male_accuracy, 4),
            round(female_accuracy, 4),
            round(male_tpr, 4),
            round(female_tpr, 4),
            round(eod, 4)
        ]
    })

    st.markdown('<div class="table-box">', unsafe_allow_html=True)
    st.dataframe(fairness_df, use_container_width=True, height=350)
    st.markdown('</div>', unsafe_allow_html=True)

with bottom_right:
    st.markdown('<div class="section-title">Interpretation</div>', unsafe_allow_html=True)

    if disparate_impact >= 0.8:
        fairness_note = "The disparate impact is above the common 0.80 threshold, suggesting comparatively better fairness."
    else:
        fairness_note = "The disparate impact is below the common 0.80 threshold, indicating possible gender bias."

    if abs(spd) < 0.10:
        spd_note = "The statistical parity difference is relatively small."
    else:
        spd_note = "The statistical parity difference shows a noticeable difference between groups."

    st.markdown(f"""
    <div class="insight-box">
    <b>Fairness Decision:</b> {fairness_note}<br><br>
    <b>Gap Observation:</b> The male selection rate is <b>{male_rate:.4f}</b> and the female selection rate is <b>{female_rate:.4f}</b>,
    resulting in a gap of <b>{selection_gap:.4f}</b>.<br><br>
    <b>SPD Observation:</b> {spd_note}<br><br>
    <b>EOD Observation:</b> Equal opportunity difference is <b>{eod:.4f}</b>, which helps show whether the model treats qualified
    male and female instances similarly.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="final-box">
    <h3 style="color:#1e3a8a; margin-bottom:8px;">Next Step: Bias Mitigation</h3>
    <p style="color:#475569; font-size:15px; margin-bottom:0;">
        The next page applies threshold-based mitigation and compares fairness and performance before and after correction.
    </p>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.5, 2, 1.5])

with nav1:
    st.page_link("pages/2_Model_Performance.py", label="← Back", use_container_width=True)

with nav3:
    st.page_link("pages/4_Mitigation_Comparison.py", label="Next →", use_container_width=True)