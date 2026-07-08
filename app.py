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

.stApp{
background: linear-gradient(135deg,#141E30,#243B55);
}

.main .block-container{
background: rgba(255,255,255,0.08);
padding:30px;
border-radius:20px;
backdrop-filter: blur(12px);
box-shadow:0px 0px 20px rgba(0,0,0,0.4);
}

h1{
text-align:center;
color:#00E5FF;
font-size:48px;
}

h4{
color:white;
}

ddiv[data-testid="stNumberInput"],
div[data-testid="stSelectbox"],
.stSlider{

background:rgba(255,255,255,0.08);
border:1px solid rgba(255,255,255,0.15);
border-radius:12px;
padding:10px;
}

.stButton>button{
width:100%;
height:58px;
font-size:20px;
font-weight:bold;
background:linear-gradient(90deg,#00c853,#00e676);
color:white;
border:none;
border-radius:15px;
box-shadow:0 0 15px rgba(0,255,120,0.5);
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.02);
background:linear-gradient(90deg,#00b248,#00c853);
}

.stButton>button:hover{
background:#009624;
color:white;
}

.result{
background:#00C853;
padding:25px;
border-radius:15px;
text-align:center;
font-size:35px;
font-weight:bold;
color:white;
}

</style>
""",unsafe_allow_html=True)

# -------------------- TITLE --------------------

st.title("⚡ Electricity Bill Prediction")

st.markdown(
"<h4 style='text-align:center;'>Predict your Monthly Electricity Bill using Machine Learning</h4>",
unsafe_allow_html=True
)

st.write("")

# -------------------- INPUTS --------------------

col1,col2=st.columns(2)

with col1:

    fan=st.number_input(
        "Fan Usage (Hours/Month)",
        min_value=0.0,
        value=10.0
    )

    refrigerator=st.number_input(
        "Refrigerator Usage (Hours/Month)",
        min_value=0.0,
        value=22.0
    )

    airconditioner=st.number_input(
        "Air Conditioner Usage (Hours/Month)",
        min_value=0.0,
        value=2.0
    )

    television=st.number_input(
        "Television Usage (Hours/Month)",
        min_value=0.0,
        value=8.0
    )

    monitor=st.number_input(
        "Monitor Usage (Hours/Month)",
        min_value=0.0,
        value=2.0
    )

with col2:

    motorpump=st.number_input(
        "Motor Pump Usage (Hours/Month)",
        min_value=0.0,
        value=0.0
    )

    month=st.slider(
        "Month",
        1,
        12,
        7
    )

    city=st.selectbox(
        "Select City",
        city_encoder.classes_
    )

    company=st.selectbox(
        "Select Company",
        company_encoder.classes_
    )

    monthlyhours=st.number_input(
        "Total Monthly Hours",
        min_value=0.0,
        value=500.0
    )

tariffrate=st.number_input(
    "Tariff Rate (₹/Unit)",
    min_value=0.0,
    value=8.5
)
# -------------------- PREDICTION --------------------

if st.button("⚡ Predict Electricity Bill"):

    city_value = city_encoder.transform([city])[0]
    company_value = company_encoder.transform([company])[0]

    input_data = pd.DataFrame({

        "Fan":[fan],
        "Refrigerator":[refrigerator],
        "AirConditioner":[airconditioner],
        "Television":[television],
        "Monitor":[monitor],
        "MotorPump":[motorpump],
        "Month":[month],
        "City":[city_value],
        "Company":[company_value],
        "MonthlyHours":[monthlyhours],
        "TariffRate":[tariffrate]

    })

    prediction = model.predict(input_data)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result">
        ⚡ Estimated Electricity Bill <br><br>
        ₹ {prediction[0]:,.2f}
    </div>
    """, unsafe_allow_html=True)


    st.info("💡 This is an estimated bill generated using the trained Random Forest Regressor model.")
st.markdown("""
<h1 style='text-align:center;
color:#FFD700;
font-size:60px;
animation: blink 0.5s infinite;'>
⚡⚡⚡
</h1>

<style>
@keyframes blink{
0%{opacity:1;}
50%{opacity:0.2;}
100%{opacity:1;}
}
</style>
""", unsafe_allow_html=True)