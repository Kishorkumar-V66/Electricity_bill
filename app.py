import streamlit as st
import pandas as pd
import joblib

# -------------------- LOAD MODEL --------------------
model = joblib.load("random_forest_model.pkl")
city_encoder = joblib.load("city_encoder.pkl")
company_encoder = joblib.load("company_encoder.pkl")

# -------------------- PAGE --------------------
st.set_page_config(
    page_title="Electricity Bill Prediction",
    page_icon="⚡",
    layout="wide"
)

# -------------------- CSS --------------------
st.markdown("""
<style>
/* App background using a clean, professional deep slate gradient */
.stApp {
    background: linear-gradient(135deg, #0F172A, #1E293B);
}

/* Main container styling for a subtle glassmorphism effect */
.main .block-container {
    background: rgba(255, 255, 255, 0.04);
    padding: 40px;
    border-radius: 16px;
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
}

/* Polished Typography */
h1 {
    text-align: center;
    color: #F8FAFC;
    font-size: 40px;
    font-weight: 700;
    margin-bottom: 5px;
}

h4 {
    color: #94A3B8;
    font-weight: 400;
}

/* Fixed input wrapper selectors and polished styling */
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"],
.stSlider {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 12px;
}

/* Professional Accent Button */
.stButton>button {
    width: 100%;
    height: 52px;
    font-size: 16px;
    font-weight: 600;
    background: #10B981;
    color: white;
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: #059669;
    box-shadow: 0 6px 16px rgba(5, 150, 105, 0.3);
    transform: translateY(-1px);
}

.stButton>button:active {
    transform: translateY(1px);
}

/* Polished, elegant output card */
.result-card {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 30px;
    border-radius: 12px;
    text-align: center;
    color: #F8FAFC;
    margin-top: 20px;
}

.result-title {
    font-size: 16px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #A7F3D0;
    margin-bottom: 8px;
}

.result-value {
    font-size: 38px;
    font-weight: 700;
    color: #34D399;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------

st.title("⚡ Electricity Bill Prediction")

st.markdown(
    "<h4 style='text-align:center;'>Predict your monthly electricity consumption using machine learning</h4>",
    unsafe_allow_html=True
)

st.write("<br>", unsafe_allow_html=True)

# -------------------- INPUTS --------------------

col1, col2 = st.columns(2)

with col1:
    fan = st.number_input(
        "Fan Usage (Hours/Month)",
        min_value=0.0,
        value=10.0
    )

    refrigerator = st.number_input(
        "Refrigerator Usage (Hours/Month)",
        min_value=0.0,
        value=22.0
    )

    airconditioner = st.number_input(
        "Air Conditioner Usage (Hours/Month)",
        min_value=0.0,
        value=2.0
    )

    television = st.number_input(
        "Television Usage (Hours/Month)",
        min_value=0.0,
        value=8.0
    )

    monitor = st.number_input(
        "Monitor Usage (Hours/Month)",
        min_value=0.0,
        value=2.0
    )

with col2:
    motorpump = st.number_input(
        "Motor Pump Usage (Hours/Month)",
        min_value=0.0,
        value=0.0
    )

    month = st.slider(
        "Month",
        1, 12, 7
    )

    city = st.selectbox(
        "Select City",
        city_encoder.classes_
    )

    company = st.selectbox(
        "Select Company",
        company_encoder.classes_
    )

    monthlyhours = (
        fan + refrigerator + airconditioner + television + monitor + motorpump
    )

st.info(f"📊 Total Monthly Hours (Auto Calculated): {monthlyhours:.2f} hrs")

tariffrate = st.number_input(
    "Tariff Rate (₹/Unit)",
    min_value=0.0,
    value=8.5
)

# -------------------- PREDICTION --------------------

if st.button("Predict Electricity Bill"):

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
    <div class="result-card">
        <div class="result-title">Estimated Electricity Bill</div>
        <div class="result-value">₹ {prediction[0]:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    st.info("💡 This estimate is generated using a trained Random Forest Regressor model.")
