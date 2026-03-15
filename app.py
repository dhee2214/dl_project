import streamlit as st

st.set_page_config(
    page_title="Fairness Analysis Project",
    layout="wide"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: #ffffff !important;
}

[data-testid="stApp"] {
    background-color: #ffffff !important;
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
    padding: 14px 18px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    text-decoration: none !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.25) !important;
}

[data-testid="stPageLink"] a:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
    color: #ffffff !important;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: #ffffff !important;
    margin: 0 !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    background-color: white;
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #1e3a8a;
    line-height: 1.2;
    margin-bottom: 10px;
}

.tagline {
    font-size: 20px;
    color: #475569;
    margin-top: 10px;
}

.hero-box {
    background: linear-gradient(135deg, #eff6ff, #f0fdf4);
    padding: 35px;
    border-radius: 24px;
    border: 1px solid #dbeafe;
    margin-bottom: 30px;
}

.card {
    padding: 22px;
    border-radius: 18px;
    color: white;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.card-title {
    font-size: 18px;
    margin-bottom: 8px;
}

.card-value {
    font-size: 21px;
    font-weight: 700;
}

.workflow-title {
    font-size: 28px;
    font-weight: 700;
    color: #111827;
    margin-top: 35px;
    margin-bottom: 18px;
}

.step-box {
    background: #f8fafc;
    padding: 18px;
    border-radius: 16px;
    border-left: 5px solid #2563eb;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    min-height: 105px;
}

.step-head {
    font-size: 17px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 6px;
}

.step-text {
    font-size: 14px;
    color: #475569;
}

.bottom-box {
    margin-top: 30px;
    padding: 28px;
    border-radius: 20px;
    background: linear-gradient(135deg, #eef2ff, #fdf2f8);
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

.bottom-title {
    color: #1e3a8a;
    margin-bottom: 8px;
    font-size: 28px;
    font-weight: 700;
}

.bottom-text {
    color: #475569;
    font-size: 17px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    st.markdown("""
    <div class="hero-box">
        <div class="main-title">
            Fairness Analysis and Bias Detection Using Deep Learning Models
        </div>
        <div class="tagline">
            Detecting, evaluating, and reducing gender bias in income prediction using the Adult Income Dataset.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.image("https://cdn-icons-png.flaticon.com/512/4149/4149653.png", width=240)

st.markdown("## Project Highlights")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="card-title">Dataset Used</div>
        <div class="card-value">Adult Income</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="card-title">Model Used</div>
        <div class="card-value">MLP Classifier</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
        <div class="card-title">Sensitive Attribute</div>
        <div class="card-value">Gender</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="card-title">Goal</div>
        <div class="card-value">Bias Detection</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="workflow-title">Project Workflow</div>', unsafe_allow_html=True)

w1, w2, w3, w4 = st.columns(4)

with w1:
    st.markdown("""
    <div class="step-box">
        <div class="step-head">Dataset</div>
        <div class="step-text">Load the Adult dataset and understand its structure.</div>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown("""
    <div class="step-box">
        <div class="step-head">Performance</div>
        <div class="step-text">Train the model and evaluate prediction accuracy.</div>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown("""
    <div class="step-box">
        <div class="step-head">Fairness</div>
        <div class="step-text">Compare fairness metrics across male and female groups.</div>
    </div>
    """, unsafe_allow_html=True)

with w4:
    st.markdown("""
    <div class="step-box">
        <div class="step-head">Mitigation</div>
        <div class="step-text">Apply threshold-based mitigation and compare results.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="bottom-box">
    <div class="bottom-title">Ready to Explore the Dataset?</div>
    <div class="bottom-text">
        Move to the next page to load the Adult Income dataset and view its structure, groups, and key details.
    </div>
</div>
""", unsafe_allow_html=True)

_, center_col, _ = st.columns([2, 2, 2])

with center_col:
    st.page_link("pages/1_Dataset_Overview.py", label="Start Analysis", use_container_width=True)