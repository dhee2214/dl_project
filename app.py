import streamlit as st

st.set_page_config(
    page_title="Fairness Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ---------- Base ---------- */
html, body, [data-testid="stAppViewContainer"], .main {
    background:
        radial-gradient(circle at top left, rgba(96, 165, 250, 0.18), transparent 24%),
        radial-gradient(circle at top right, rgba(168, 85, 247, 0.18), transparent 22%),
        radial-gradient(circle at bottom left, rgba(244, 114, 182, 0.12), transparent 22%),
        linear-gradient(180deg, #eef4ff 0%, #f8fbff 55%, #fcfcff 100%) !important;
    color: #0f172a;
}

[data-testid="stApp"] {
    background: transparent !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.6rem;
    padding-bottom: 2.2rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
}

header[data-testid="stHeader"] {
    background: rgba(255,255,255,0.0) !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #172554 45%, #1e1b4b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebarNav"] {
    padding-top: 1rem;
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
    letter-spacing: 0.3px;
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

/* ---------- Hero ---------- */
.hero-shell {
    position: relative;
    overflow: hidden;
    border-radius: 34px;
    padding: 3.2rem 3rem 2.8rem 3rem;
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 28%, #7c3aed 68%, #ec4899 100%);
    box-shadow:
        0 28px 60px rgba(59, 130, 246, 0.24),
        inset 0 1px 0 rgba(255,255,255,0.18);
    margin-bottom: 30px;
}

.hero-shell::before {
    content: "";
    position: absolute;
    width: 360px;
    height: 360px;
    right: -90px;
    top: -120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.20), rgba(255,255,255,0.04) 60%, transparent 75%);
}

.hero-shell::after {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    left: -60px;
    bottom: -120px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.16), rgba(255,255,255,0.04) 60%, transparent 78%);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.20);
    backdrop-filter: blur(12px);
    color: white;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 18px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}

.hero-title {
    font-size: 52px;
    font-weight: 900;
    line-height: 1.08;
    color: white;
    max-width: 920px;
    margin-bottom: 16px;
    letter-spacing: -0.8px;
}

.hero-subtitle {
    font-size: 18px;
    line-height: 1.85;
    color: rgba(255,255,255,0.92);
    max-width: 860px;
    margin-bottom: 28px;
}

.hero-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.hero-info {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 22px;
    padding: 18px 18px;
    backdrop-filter: blur(14px);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}

.hero-info-label {
    font-size: 12px;
    font-weight: 700;
    color: rgba(255,255,255,0.76);
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 8px;
}

.hero-info-value {
    font-size: 24px;
    font-weight: 850;
    color: #ffffff;
    line-height: 1.2;
}

/* ---------- Headings ---------- */
.section-title {
    font-size: 31px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 12px;
    margin-bottom: 6px;
    letter-spacing: -0.4px;
}

.section-subtitle {
    font-size: 16px;
    color: #64748b;
    margin-bottom: 22px;
    line-height: 1.75;
}

/* ---------- Highlight cards ---------- */
.pretty-card {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    padding: 28px 24px;
    min-height: 182px;
    color: white;
    box-shadow: 0 18px 38px rgba(15, 23, 42, 0.12);
    transition: all 0.28s ease;
    border: 1px solid rgba(255,255,255,0.12);
}

.pretty-card:hover {
    transform: translateY(-7px) scale(1.01);
    box-shadow: 0 24px 44px rgba(15, 23, 42, 0.16);
}

.pretty-card::before {
    content: "";
    position: absolute;
    width: 130px;
    height: 130px;
    top: -24px;
    right: -20px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
}

.pretty-card::after {
    content: "";
    position: absolute;
    width: 85px;
    height: 85px;
    bottom: -10px;
    right: 25px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}

.pretty-icon {
    font-size: 30px;
    margin-bottom: 16px;
}

.pretty-label {
    font-size: 15px;
    font-weight: 700;
    opacity: 0.96;
    margin-bottom: 10px;
}

.pretty-value {
    font-size: 33px;
    font-weight: 900;
    line-height: 1.16;
}

/* ---------- Workflow cards ---------- */
.workflow-card {
    position: relative;
    overflow: hidden;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.75);
    backdrop-filter: blur(16px);
    border-radius: 26px;
    padding: 24px 22px;
    min-height: 228px;
    box-shadow: 0 18px 34px rgba(148, 163, 184, 0.18);
    transition: all 0.28s ease;
}

.workflow-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 24px 42px rgba(148, 163, 184, 0.24);
}

.workflow-card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 26px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(59,130,246,0.22), rgba(168,85,247,0.18), rgba(236,72,153,0.16));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
}

.flow-num {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 850;
    margin-bottom: 16px;
    box-shadow: 0 12px 22px rgba(99, 102, 241, 0.26);
}

.flow-title {
    font-size: 22px;
    font-weight: 850;
    color: #0f172a;
    margin-bottom: 10px;
}

.flow-text {
    font-size: 15px;
    color: #475569;
    line-height: 1.78;
}

/* ---------- CTA ---------- */
.cta-shell {
    position: relative;
    overflow: hidden;
    margin-top: 36px;
    background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(243,232,255,0.95), rgba(219,234,254,0.96));
    border: 1px solid rgba(255,255,255,0.70);
    border-radius: 30px;
    padding: 36px 30px;
    text-align: center;
    box-shadow: 0 22px 44px rgba(148, 163, 184, 0.20);
}

.cta-shell::before {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    left: -40px;
    top: -70px;
    border-radius: 50%;
    background: rgba(96,165,250,0.12);
}

.cta-shell::after {
    content: "";
    position: absolute;
    width: 170px;
    height: 170px;
    right: -50px;
    bottom: -70px;
    border-radius: 50%;
    background: rgba(168,85,247,0.12);
}

.cta-title {
    position: relative;
    z-index: 2;
    font-size: 40px;
    font-weight: 900;
    color: #1e3a8a;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}

.cta-text {
    position: relative;
    z-index: 2;
    font-size: 17px;
    color: #475569;
    line-height: 1.8;
    max-width: 840px;
    margin: 0 auto 24px auto;
}

/* ---------- Buttons ---------- */
[data-testid="stPageLink"] {
    text-align: center !important;
}

[data-testid="stPageLink"] a {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 55%, #ec4899 100%) !important;
    color: white !important;
    border-radius: 18px !important;
    padding: 15px 20px !important;
    font-size: 18px !important;
    font-weight: 850 !important;
    text-decoration: none !important;
    border: none !important;
    box-shadow: 0 16px 30px rgba(99, 102, 241, 0.28) !important;
    transition: all 0.28s ease !important;
}

[data-testid="stPageLink"] a:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 20px 36px rgba(99, 102, 241, 0.34) !important;
}

[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: white !important;
    margin: 0 !important;
}

/* ---------- Responsive ---------- */
@media (max-width: 1100px) {
    .hero-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero-title {
        font-size: 42px;
    }
}

@media (max-width: 700px) {
    .hero-grid {
        grid-template-columns: 1fr;
    }
    .hero-shell {
        padding: 2rem 1.4rem 2rem 1.4rem;
    }
    .hero-title {
        font-size: 31px;
    }
    .cta-title {
        font-size: 30px;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-shell">
    <div class="hero-badge">✨ AI Fairness Project Dashboard</div>
    <div class="hero-title">Fairness Analysis and Bias Detection Using Deep Learning Models</div>
    <div class="hero-subtitle">
        A stylish and interactive final year project dashboard that explores income prediction,
        detects gender-based bias, evaluates model behaviour, and presents mitigation results
        through a modern and visually appealing interface.
    </div>
    <div class="hero-grid">
        <div class="hero-info">
            <div class="hero-info-label">Dataset</div>
            <div class="hero-info-value">Adult Income</div>
        </div>
        <div class="hero-info">
            <div class="hero-info-label">Model</div>
            <div class="hero-info-value">MLP Classifier</div>
        </div>
        <div class="hero-info">
            <div class="hero-info-label">Sensitive Attribute</div>
            <div class="hero-info-value">Gender</div>
        </div>
        <div class="hero-info">
            <div class="hero-info-label">Objective</div>
            <div class="hero-info-value">Bias Detection</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Project Highlights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">An attractive overview of the core components that make your project stand out.</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="pretty-card" style="background: linear-gradient(135deg, #3b82f6, #2563eb);">
        <div class="pretty-icon">📊</div>
        <div class="pretty-label">Dataset Used</div>
        <div class="pretty-value">Adult Income</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="pretty-card" style="background: linear-gradient(135deg, #10b981, #059669);">
        <div class="pretty-icon">🧠</div>
        <div class="pretty-label">Model Used</div>
        <div class="pretty-value">MLP Classifier</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="pretty-card" style="background: linear-gradient(135deg, #f59e0b, #d97706);">
        <div class="pretty-icon">⚖️</div>
        <div class="pretty-label">Sensitive Attribute</div>
        <div class="pretty-value">Gender</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="pretty-card" style="background: linear-gradient(135deg, #8b5cf6, #7c3aed);">
        <div class="pretty-icon">🎯</div>
        <div class="pretty-label">Goal</div>
        <div class="pretty-value">Bias Detection</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Project Workflow</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A smooth step-by-step flow that helps the evaluator understand the complete project journey clearly.</div>', unsafe_allow_html=True)

w1, w2, w3, w4 = st.columns(4)

with w1:
    st.markdown("""
    <div class="workflow-card">
        <div class="flow-num">1</div>
        <div class="flow-title">Dataset Overview</div>
        <div class="flow-text">
            Explore the dataset structure, inspect important features, and understand the sensitive attribute used for fairness evaluation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown("""
    <div class="workflow-card">
        <div class="flow-num">2</div>
        <div class="flow-title">Model Performance</div>
        <div class="flow-text">
            Review predictive quality using accuracy, precision, recall, F1-score, confusion matrix, and classification report.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown("""
    <div class="workflow-card">
        <div class="flow-num">3</div>
        <div class="flow-title">Fairness Analysis</div>
        <div class="flow-text">
            Compare gender-wise outcomes using fairness metrics such as disparate impact, statistical parity difference, and equal opportunity difference.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w4:
    st.markdown("""
    <div class="workflow-card">
        <div class="flow-num">4</div>
        <div class="flow-title">Mitigation Comparison</div>
        <div class="flow-text">
            Apply threshold-based mitigation and compare fairness and performance before and after correction to show final impact.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="cta-shell">
    <div class="cta-title">Ready to Begin the Journey?</div>
    <div class="cta-text">
        Start with the dataset overview and move through performance evaluation, fairness assessment, and mitigation comparison in a beautiful visual flow.
    </div>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([1.5, 2, 1.5])
with center:
    st.page_link("pages/1_Dataset_Overview.py", label="Start Exploring ✨", use_container_width=True)