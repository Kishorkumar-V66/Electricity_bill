import streamlit as st
import pandas as pd
import joblib

# -------------------- LOAD MODEL --------------------
model = joblib.load("random_forest_model.pkl")
city_encoder = joblib.load("city_encoder.pkl")
company_encoder = joblib.load("company_encoder.pkl")

# -------------------- PAGE --------------------
st.set_page_config(
    page_title="Electricity Bill Estimator",
    page_icon="⚡",
    layout="wide"
)

# -------------------- CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600;700&display=swap');

:root{
    --bg-base:#FBF7EF;
    --bg-card:#FFFFFF;
    --accent-copper:#C2710C;
    --accent-copper-soft:rgba(194,113,12,0.10);
    --accent-teal:#0E8F72;
    --accent-teal-soft:rgba(14,143,114,0.08);
    --text-primary:#20242E;
    --text-muted:#6B7280;
    --border-line:rgba(194,113,12,0.28);
    --shadow-soft:rgba(31,29,20,0.08);
}

.stApp{
    background:
        radial-gradient(ellipse 1100px 600px at 10% -10%, rgba(194,113,12,0.14), transparent 55%),
        radial-gradient(ellipse 1000px 650px at 100% 0%, rgba(14,143,114,0.12), transparent 52%),
        radial-gradient(ellipse 900px 700px at 50% 115%, rgba(255,196,120,0.16), transparent 60%),
        linear-gradient(160deg, #FDF9F1 0%, #FBF6EC 45%, #FAF3E6 100%);
    background-attachment:fixed;
}

.stApp::before{
    content:"";
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(194,113,12,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(194,113,12,0.05) 1px, transparent 1px);
    background-size:42px 42px;
    mask-image:radial-gradient(ellipse 1200px 800px at 50% 0%, black, transparent 75%);
    -webkit-mask-image:radial-gradient(ellipse 1200px 800px at 50% 0%, black, transparent 75%);
    pointer-events:none;
    z-index:0;
}

html, body, [class*="css"]{
    font-family:'Inter', sans-serif;
    color:var(--text-primary);
}

.main .block-container{
    padding-top:2.5rem;
    padding-bottom:3rem;
    max-width:1200px;
}

/* -------- HEADER -------- */
.grid-eyebrow{
    font-family:'JetBrains Mono', monospace;
    letter-spacing:0.25em;
    font-size:12.5px;
    color:var(--accent-copper);
    text-transform:uppercase;
    margin-bottom:6px;
}

.grid-title{
    font-family:'Space Grotesk', sans-serif;
    font-weight:700;
    font-size:44px;
    color:var(--text-primary);
    margin:0;
    line-height:1.15;
}

.grid-sub{
    font-family:'Inter', sans-serif;
    color:var(--text-muted);
    font-size:15.5px;
    margin-top:8px;
    max-width:620px;
}

.section-divider{
    height:1px;
    margin:22px 0 30px 0;
    background:linear-gradient(90deg, rgba(194,113,12,0.45), rgba(31,29,20,0.08) 45%, rgba(14,143,114,0.40));
    border-radius:1px;
}

/* -------- PANEL CARDS -------- */
.st-key-appliance_panel > div,
.st-key-site_panel > div{
    background:var(--bg-card);
    border:1px solid rgba(31,29,20,0.08);
    border-radius:12px;
    padding:24px 26px 14px 26px;
    margin-bottom:22px;
    box-shadow:0 8px 28px -12px var(--shadow-soft);
}

.st-key-appliance_panel > div{
    border-left:3px solid var(--accent-copper);
}

.st-key-site_panel > div{
    border-left:3px solid var(--accent-teal);
}

.panel-label{
    font-family:'JetBrains Mono', monospace;
    font-size:11.5px;
    letter-spacing:0.18em;
    color:var(--text-muted);
    text-transform:uppercase;
    margin-bottom:14px;
}

.channel-tag{
    display:inline-block;
    font-family:'JetBrains Mono', monospace;
    font-size:10.5px;
    letter-spacing:0.08em;
    color:var(--accent-copper);
    background:var(--accent-copper-soft);
    border:1px solid rgba(194,113,12,0.35);
    border-radius:4px;
    padding:2px 8px;
    margin-bottom:6px;
}

/* -------- INPUTS -------- */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div{
    background:#FBFAF7 !important;
    border:1px solid rgba(31,29,20,0.14) !important;
    border-radius:8px !important;
    color:var(--text-primary) !important;
    font-family:'JetBrains Mono', monospace !important;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label{
    font-family:'Inter', sans-serif !important;
    font-size:13.5px !important;
    color:var(--text-muted) !important;
    font-weight:500 !important;
}

div[data-testid="stSlider"] div[role="slider"]{
    background:var(--accent-copper) !important;
    box-shadow:0 0 10px rgba(194,113,12,0.45);
}

div[data-baseweb="slider"] > div > div{
    background:var(--accent-copper) !important;
}

/* -------- LCD READOUT -------- */
.lcd-readout{
    font-family:'JetBrains Mono', monospace;
    background:var(--accent-teal-soft);
    border:1px solid rgba(14,143,114,0.30);
    border-radius:8px;
    padding:14px 18px;
    color:#0B6B55;
    font-size:14.5px;
    letter-spacing:0.02em;
    margin:6px 0 20px 0;
}

.lcd-readout b{
    font-size:17px;
}

/* -------- BUTTON -------- */
.stButton>button{
    width:100%;
    height:56px;
    font-family:'Space Grotesk', sans-serif;
    font-size:17px;
    font-weight:600;
    letter-spacing:0.03em;
    background:linear-gradient(90deg,#E8A33D,#C2710C);
    color:#26170A;
    border:none;
    border-radius:10px;
    box-shadow:0 10px 26px -10px rgba(194,113,12,0.55);
    transition:all 0.25s ease;
    margin-top:6px;
}

.stButton>button:hover{
    transform:translateY(-1px);
    box-shadow:0 14px 30px -10px rgba(194,113,12,0.65);
    background:linear-gradient(90deg,#EEAF52,#D07E14);
    color:#26170A;
}

/* -------- RESULT PANEL -------- */
.result-panel{
    background:linear-gradient(180deg, rgba(14,143,114,0.10), rgba(255,255,255,0.9));
    border:1px solid rgba(14,143,114,0.30);
    border-radius:14px;
    padding:34px 20px;
    text-align:center;
    margin-top:8px;
    position:relative;
    overflow:hidden;
    box-shadow:0 12px 32px -14px var(--shadow-soft);
}

.result-panel::before{
    content:"";
    position:absolute;
    top:0; left:-30%;
    width:160%; height:100%;
    background:linear-gradient(100deg, transparent 40%, rgba(14,143,114,0.10) 50%, transparent 60%);
    animation:scan 3.2s linear infinite;
}

@keyframes scan{
    0%{transform:translateX(-15%);}
    100%{transform:translateX(15%);}
}

.result-eyebrow{
    font-family:'JetBrains Mono', monospace;
    font-size:12px;
    letter-spacing:0.22em;
    color:var(--text-muted);
    text-transform:uppercase;
    position:relative;
}

.result-value{
    font-family:'JetBrains Mono', monospace;
    font-weight:700;
    font-size:52px;
    color:#0B6B55;
    margin-top:6px;
    position:relative;
}

.result-note{
    font-family:'Inter', sans-serif;
    font-size:13px;
    color:var(--text-muted);
    margin-top:14px;
    position:relative;
}

@media (prefers-reduced-motion: reduce){
    .current-line, .result-panel::before{ animation:none; }
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
<div class="grid-eyebrow">SMART UTILITY ANALYTICS</div>
<div class="grid-title">⚡ Electricity Bill Estimator</div>
<div class="grid-sub">Enter your appliance load, location, and provider to get a model-based estimate of your monthly bill.</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# -------------------- APPLIANCE LOAD PANEL --------------------
with st.container(key="appliance_panel"):
    st.markdown('<div class="panel-label">Appliance Load — Hours Run Per Month</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<span class="channel-tag">01</span>', unsafe_allow_html=True)
        fan = st.number_input("Fan Usage (Hours/Month)", min_value=0.0, value=10.0)

        st.markdown('<span class="channel-tag">02</span>', unsafe_allow_html=True)
        refrigerator = st.number_input("Refrigerator Usage (Hours/Month)", min_value=0.0, value=22.0)

        st.markdown('<span class="channel-tag">03</span>', unsafe_allow_html=True)
        airconditioner = st.number_input("Air Conditioner Usage (Hours/Month)", min_value=0.0, value=2.0)

    with col2:
        st.markdown('<span class="channel-tag">04</span>', unsafe_allow_html=True)
        television = st.number_input("Television Usage (Hours/Month)", min_value=0.0, value=8.0)

        st.markdown('<span class="channel-tag">05</span>', unsafe_allow_html=True)
        monitor = st.number_input("Monitor Usage (Hours/Month)", min_value=0.0, value=2.0)

        st.markdown('<span class="channel-tag">06</span>', unsafe_allow_html=True)
        motorpump = st.number_input("Motor Pump Usage (Hours/Month)", min_value=0.0, value=0.0)

    monthlyhours = fan + refrigerator + airconditioner + television + monitor + motorpump

    st.markdown(f"""
    <div class="lcd-readout">📊 TOTAL LOAD &nbsp;→&nbsp; <b>{monthlyhours:.2f} hrs / month</b></div>
    """, unsafe_allow_html=True)

# -------------------- SITE + TARIFF PANEL --------------------
with st.container(key="site_panel"):
    st.markdown('<div class="panel-label">Site &amp; Tariff Details</div>', unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)

    with col3:
        month = st.slider("Billing Month", 1, 12, 7)

    with col4:
        city = st.selectbox("Select City", city_encoder.classes_)

    with col5:
        company = st.selectbox("Select Provider", company_encoder.classes_)

    tariffrate = st.number_input("Tariff Rate (₹/Unit)", min_value=0.0, value=8.5)

# -------------------- PREDICTION --------------------
predict_clicked = st.button("⚡ Calculate Estimated Bill")

if predict_clicked:

    city_value = city_encoder.transform([city])[0]
    company_value = company_encoder.transform([company])[0]

    input_data = pd.DataFrame({
        "Fan": [fan],
        "Refrigerator": [refrigerator],
        "AirConditioner": [airconditioner],
        "Television": [television],
        "Monitor": [monitor],
        "MotorPump": [motorpump],
        "Month": [month],
        "City": [city_value],
        "Company": [company_value],
        "MonthlyHours": [monthlyhours],
        "TariffRate": [tariffrate]
    })

    prediction = model.predict(input_data)

    st.markdown(f"""
    <div class="result-panel">
        <div class="result-eyebrow">Estimated Monthly Bill</div>
        <div class="result-value">₹ {prediction[0]:,.2f}</div>
        <div class="result-note">Generated using the trained Random Forest Regressor model</div>
    </div>
    """, unsafe_allow_html=True)
