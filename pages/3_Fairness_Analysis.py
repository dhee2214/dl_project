# =========================
# STEP 1: IMPORT REQUIRED LIBRARIES
# Streamlit is used to create the web app interface
# Pandas is used to create and show tables
# Matplotlib is used for charts and visualizations
# train_and_evaluate() is used to get model predictions
# calculate_fairness() is used to compute fairness metrics
# =========================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model.train_model import train_and_evaluate
from fairness.fairness_metrics import calculate_fairness


# =========================
# STEP 2: CONFIGURE THE PAGE
# This sets the page title, wide layout,
# and keeps the sidebar expanded by default
# =========================
st.set_page_config(
    page_title="Fairness Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# STEP 3: APPLY CUSTOM PAGE STYLING
# This CSS block is used to design the full page,
# including background, sidebar, hero section,
# metric cards, chart boxes, tables, and buttons
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

/* Hero */
.page-hero {
    position: relative;
    overflow: hidden;
    border-radius: 32px;
    padding: 2.8rem 2.6rem 2.4rem 2.6rem;
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 35%, #7c3aed 65%, #ec4899 100%);
    box-shadow: 0 26px 56px rgba(79, 70, 229, 0.22);
    margin-bottom: 26px;
}

.page-hero::before {
    content: "";
    position: absolute;
    width: 340px;
    height: 340px;
    top: -120px;
    right: -70px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.24), rgba(255,255,255,0.04) 65%, transparent 76%);
}

.page-hero::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    left: -50px;
    bottom: -90px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.16), rgba(255,255,255,0.03) 65%, transparent 78%);
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

/* Cards */
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
.chart-box, .table-box, .insight-panel {
    background: rgba(255,255,255,0.80);
    border: 1px solid rgba(255,255,255,0.72);
    padding: 18px;
    border-radius: 24px;
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.14);
    backdrop-filter: blur(14px);
}

.insight-box {
    background: linear-gradient(135deg, rgba(238,242,255,0.92), rgba(248,250,252,0.92));
    padding: 20px;
    border-radius: 20px;
    border-left: 5px solid #6366f1;
    color: #334155;
    font-size: 15px;
    line-height: 1.8;
    box-shadow: 0 10px 24px rgba(148, 163, 184, 0.10);
}

.final-box {
    margin-top: 22px;
    padding: 24px;
    border-radius: 26px;
    background: linear-gradient(135deg, #eef2ff, #fdf2f8);
    text-align: center;
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.14);
    border: 1px solid rgba(255,255,255,0.75);
}

.final-title {
    color: #1e3a8a;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 10px;
}

.final-text {
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
# STEP 4: DEFINE FUNCTION TO GET FAIRNESS RESULTS
# This function first trains the model,
# then gets actual labels, predictions,
# and sensitive attribute values.
# After that, fairness metrics are calculated.
# cache_resource is used so it does not run again and again
# =========================
@st.cache_resource
def get_fairness_results():
    results = train_and_evaluate()
    y_test = results["y_test"]
    sensitive_test = results["sensitive_test"]
    y_pred = results["y_pred"]
    fairness_results = calculate_fairness(y_test, y_pred, sensitive_test)
    return fairness_results


# =========================
# STEP 5: CALCULATE FAIRNESS METRICS
# A loading spinner is shown while
# fairness metrics are being calculated
# =========================
with st.spinner("Calculating fairness metrics and loading analysis..."):
    fairness_results = get_fairness_results()


# =========================
# STEP 6: EXTRACT INDIVIDUAL FAIRNESS VALUES
# Here we separately store all fairness-related results
# so they can be displayed in cards, tables, and charts
# =========================
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


# =========================
# STEP 7: CREATE HERO SECTION
# This top section introduces the purpose
# of the fairness analysis page
# =========================
st.markdown("""
<div class="page-hero">
    <div class="hero-badge">⚖️ Core Bias Evaluation</div>
    <div class="page-title">Fairness Analysis</div>
    <div class="page-text">
        This page examines whether the trained model produces balanced decisions for male and female groups.
        It highlights selection rates, disparate impact, statistical parity difference, and equal opportunity
        difference to identify whether the model behaves fairly across sensitive groups.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# STEP 8: DISPLAY FAIRNESS SUMMARY CARDS
# These cards show the main fairness measures
# such as male selection rate, female selection rate,
# disparate impact, and SPD
# =========================
st.markdown('<div class="section-title">Fairness Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Key fairness indicators that help reveal whether one gender group receives more favorable outcomes than the other.</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="metric-title">Male Selection Rate</div>
        <div class="metric-value">{male_rate:.4f}</div>
        <div class="metric-sub">Positive outcome rate observed for male instances.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #ec4899, #db2777);">
        <div class="metric-title">Female Selection Rate</div>
        <div class="metric-value">{female_rate:.4f}</div>
        <div class="metric-sub">Positive outcome rate observed for female instances.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="metric-title">Disparate Impact</div>
        <div class="metric-value">{disparate_impact:.4f}</div>
        <div class="metric-sub">A value near or above 0.80 is generally preferred.</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="metric-title">SPD</div>
        <div class="metric-value">{spd:.4f}</div>
        <div class="metric-sub">Difference between group selection rates.</div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# STEP 9: CREATE TWO COLUMNS FOR CHARTS
# Left side is for selection rate comparison
# Right side is for disparate impact threshold check
# =========================
v1, v2 = st.columns(2)


# =========================
# STEP 10: SHOW SELECTION RATE COMPARISON CHART
# This chart visually compares positive outcome rates
# for male and female groups
# =========================
with v1:
    st.markdown('<div class="section-title">Selection Rate Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Compares positive prediction rates between female and male groups.</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig1, ax1 = plt.subplots(figsize=(6.3, 3.5))

    groups = ["Female", "Male"]
    values = [female_rate, male_rate]
    colors = ["#ec4899", "#3b82f6"]
    y_positions = [0, 1]

    ax1.hlines(y=y_positions, xmin=0, xmax=values, color=colors, linewidth=6, alpha=0.92)
    ax1.scatter(values, y_positions, s=440, color=colors, zorder=3)

    for i, val in enumerate(values):
        ax1.text(val + 0.012, y_positions[i], f"{val:.3f}", va="center", fontsize=11, fontweight="bold")

    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(groups, fontsize=11)
    ax1.set_xlim(0, max(0.38, max(values) + 0.10))
    ax1.set_xlabel("Selection Rate", fontsize=10)
    ax1.set_title("Gender-wise Positive Outcome Rate", fontsize=14, fontweight="bold", pad=10)
    ax1.grid(axis="x", linestyle="--", alpha=0.25)

    for spine in ["top", "right"]:
        ax1.spines[spine].set_visible(False)

    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# STEP 11: SHOW DISPARATE IMPACT THRESHOLD CHART
# This chart checks whether the disparate impact
# is above or below the fairness threshold of 0.80
# =========================
with v2:
    st.markdown('<div class="section-title">Disparate Impact Threshold Check</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Shows how close the model is to the commonly used 0.80 fairness threshold.</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig2, ax2 = plt.subplots(figsize=(6.3, 3.5))

    current_value = min(disparate_impact, 1.0)

    ax2.hlines(y=0, xmin=0, xmax=1.0, color="#e5e7eb", linewidth=16)
    ax2.hlines(y=0, xmin=0, xmax=current_value, color="#8b5cf6", linewidth=16)
    ax2.scatter([current_value], [0], s=280, color="#7c3aed", zorder=3)
    ax2.axvline(x=0.8, color="#ef4444", linestyle="--", linewidth=2)

    ax2.text(current_value, 0.13, f"{disparate_impact:.3f}", ha="center", fontsize=12, fontweight="bold")
    ax2.text(0.8, -0.20, "0.80 threshold", ha="center", fontsize=10, color="#ef4444", fontweight="bold")

    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(-0.30, 0.30)
    ax2.set_yticks([])
    ax2.set_xlabel("Disparate Impact", fontsize=10)
    ax2.set_title("Fairness Threshold View", fontsize=14, fontweight="bold", pad=10)

    for spine in ["top", "right", "left"]:
        ax2.spines[spine].set_visible(False)

    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# STEP 12: CREATE TWO COLUMNS FOR TABLE AND INTERPRETATION
# Left side shows the fairness metrics table
# Right side explains what the values mean
# =========================
bottom_left, bottom_right = st.columns([1.15, 0.85])


# =========================
# STEP 13: DISPLAY FAIRNESS METRIC TABLE
# This table gives a compact summary
# of all main fairness-related values
# =========================
with bottom_left:
    st.markdown('<div class="section-title">Fairness Metric Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">A compact summary of the main fairness metrics computed for the model.</div>', unsafe_allow_html=True)

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
    st.dataframe(fairness_df, use_container_width=True, height=375)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# STEP 14: INTERPRET THE FAIRNESS RESULTS
# This section explains whether the model
# appears fair or biased based on the metric values
# =========================
with bottom_right:
    st.markdown('<div class="section-title">Interpretation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Quick explanation of what the fairness values indicate.</div>', unsafe_allow_html=True)

    if disparate_impact >= 0.8:
        fairness_note = "The disparate impact is above the common 0.80 threshold, suggesting comparatively better fairness across groups."
    else:
        fairness_note = "The disparate impact is below the common 0.80 threshold, indicating possible gender bias in model outcomes."

    if abs(spd) < 0.10:
        spd_note = "The statistical parity difference is relatively small, which suggests the selection rates are closer between groups."
    else:
        spd_note = "The statistical parity difference is noticeable, showing that the model treats the two groups differently in outcome rate."

    st.markdown(f"""
    <div class="insight-box">
    <b>Fairness Decision:</b> {fairness_note}<br><br>
    <b>Gap Observation:</b> The male selection rate is <b>{male_rate:.4f}</b> and the female selection rate is <b>{female_rate:.4f}</b>,
    resulting in a gap of <b>{selection_gap:.4f}</b>.<br><br>
    <b>SPD Observation:</b> {spd_note}<br><br>
    <b>EOD Observation:</b> Equal opportunity difference is <b>{eod:.4f}</b>, which helps indicate whether qualified male and female
    instances are treated similarly by the model.
    </div>
    """, unsafe_allow_html=True)


# =========================
# STEP 15: SHOW NEXT STEP MESSAGE
# This tells the user that the next stage
# is bias mitigation and comparison
# =========================
st.markdown("""
<div class="final-box">
    <div class="final-title">Next Step: Bias Mitigation</div>
    <div class="final-text">
        Continue to the next page to apply threshold-based mitigation and compare fairness
        and model performance before and after correction.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# STEP 16: ADD NAVIGATION BUTTONS
# These buttons help move to the previous page
# or the next mitigation page
# =========================
st.markdown("<br>", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns([1.4, 2, 1.4])

with nav1:
    st.page_link("pages/2_Model_Performance.py", label="← Back", use_container_width=True)

with nav3:
    st.page_link("pages/4_Mitigation_Comparison.py", label="Next →", use_container_width=True)