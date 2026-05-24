import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page configuration
st.set_page_config(page_title="EcoFreeze AI Optimizer", page_icon="🔋", layout="wide")

# Loading the pre-trained models safely
@st.cache_resource
def load_models():
    m_discharge = joblib.load('model_discharge.pkl')
    m_temp = joblib.load('model_temp.pkl')
    return m_discharge, m_temp

model_discharge, model_temp = load_models()

# Dashboard Main Headers
st.title("🔋 EcoFreeze AI: Off-Grid Battery & Thermal Optimizer")
st.subheader("Smart Predictive Input Engine for Sub-Saharan Cold Storages")
st.markdown("---")

# Sidebar inputs (The Interactive Controls)
st.sidebar.header("📡 Real-Time Environmental Inputs")

ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 25.0, 45.0, 32.0, step=0.5)
solar_irradiance = st.sidebar.slider("Solar Irradiance (W/m²)", 0, 1000, 450, step=10)
battery_health = st.sidebar.slider("Current Battery Health (%)", 50, 100, 85, step=1)

# Expert Pitch Feature inside the sidebar
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Core Architecture Note:**\n"
    "This low-compute linear model can act as a predictive input for Energy Management Systems "
    "to optimize battery cycles and prevent deep discharge in off-grid cold storages."
)

# Model prediction based on user inputs
input_data = pd.DataFrame([[ambient_temp, solar_irradiance, battery_health]], 
                          columns=['Ambient_Temperature', 'Solar_Irradiance', 'Battery_Health'])

pred_discharge = max(0.0, float(model_discharge.predict(input_data)[0]))
pred_cold_temp = float(model_temp.predict(input_data)[0])

st.markdown("### 🧠 AI Guard: Live System Status & Action Logic")

# Decision Logic using Streamlit's Native Alert Components
if solar_irradiance < 200 and pred_discharge > 12:
    status_type = "CRITICAL"
    st.error("🚨 **CRITICAL RISK:** Deep Discharge Alert! Solar generation is offline and battery drain is heavy. **Action:** Dimming cold storage cooling cycles immediately to preserve battery lifespan.")
elif solar_irradiance < 400 or pred_discharge > 8:
    status_type = "WARNING"
    st.warning("⚠️ **ECONOMY MODE:** Low solar radiation detected. Switching system to low-compute prediction state to optimize battery cycles.")
else:
    status_type = "SAFE"
    st.success("🟢 **SYSTEM SAFE:** High solar irradiance. Cold storage is running at peak performance. Battery is healthily buffering energy.")

st.markdown("<br>", unsafe_allowed_html=True)

# KPI Cards using Streamlit's native st.metric component
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📉 Predicted Discharge Rate", value=f"{pred_discharge:.2f} % / hr", delta="- Battery Depletion")

with col2:
    st.metric(label="🔋 Dynamic Battery Status", value=status_type, delta="Protection Mode Active")

with col3:
    st.metric(label="❄️ Cold Storage Internal Temp", value=f"{pred_cold_temp:.1f} °C", delta="Thermal Target")

# Simulation (Visual Prediction Trend)
st.markdown("<br>### 📊 24-Hour Battery Depletion Projection", unsafe_allowed_html=True)

hours = list(range(1, 24))
simulated_soc = []
current_soc = 100.0

for h in hours:
    current_drain = pred_discharge if h <= 12 else pred_discharge * 1.5
    current_soc = max(10.0, current_soc - current_drain)
    simulated_soc.append(current_soc)

chart_data = pd.DataFrame({
    'Hour': hours,
    'Estimated Battery Charge (%)': simulated_soc
}).set_index('Hour')

st.line_chart(chart_data)
