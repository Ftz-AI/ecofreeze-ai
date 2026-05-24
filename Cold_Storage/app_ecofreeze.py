import streamlit as str 
import pandas as pd
import numpy as np
import joblib

# page configuration and custom Theme (Dark & Sleek UI)
st.set_page_config(page_title="EcoFreeze AI Optimizer", page_icon="🔋", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .kpi-card {
        background-color: #1f293d; padding: 20px; border-radius: 10px;
        text-align: center; border-left: 5px solid #00f2fe;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .safe-bg { background-color: #1e4620; border: 1px solid #2e7d32; padding: 15px; border-radius: 8px; }
    .warning-bg { background-color: #664d03; border: 1px solid #ffc107; padding: 15px; border-radius: 8px; }
    .critical-bg { background-color: #58151c; border: 1px solid #dc3545; padding: 15px; border-radius: 8px; }
    </style>
""", unsafe_allowed_html=True)

# Loading the pre-trained models
@st.cache_resource
def load_models():
    m_discharge = joblib.load('model_discharge.pkl')
    m_temp = joblib.load('model_temp.pkl')
    return m_discharge, m_temp

model_discharge, model_temp = load_models()

# Dashboard title and description
st.title("🔋 EcoFreeze AI: Off-Grid Battery & Thermal Optimizer")
st.subheader("Smart Predictive Input Engine for Sub-Saharan Cold Storages")
st.markdown("---")

# sidebar inputs (The Interactive Controls)
st.sidebar.header("📡 Real-Time Environmental Inputs")

ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 25.0, 45.0, 32.0, step=0.5)
solar_irradiance = st.sidebar.slider("Solar Irradiance (W/m²)", 0, 1000, 450, step=10)
battery_health = st.sidebar.slider("Current Battery Health (%)", 50, 100, 85, step=1)

# model prediction based on user inputs
input_data = pd.DataFrame([[ambient_temp, solar_irradiance, battery_health]], 
                          columns=['Ambient_Temperature', 'Solar_Irradiance', 'Battery_Health'])

pred_discharge = max(0.0, float(model_discharge.predict(input_data)[0]))
pred_cold_temp = float(model_temp.predict(input_data)[0])


st.markdown("### 🧠 AI Guard: Live System Status & Action Logic")

# Desicion Logic:
if solar_irradiance < 200 and pred_discharge > 12:
    status_type = "CRITICAL"
    status_class = "critical-bg"
    status_msg = "🚨 **CRITICAL RISK:** Deep Discharge Alert! Solar generation is offline and battery drain is heavy. **Action:** Dimming cold storage cooling cycles immediately to preserve battery lifespan."
elif solar_irradiance < 400 or pred_discharge > 8:
    status_type = "WARNING"
    status_class = "warning-bg"
    status_msg = "⚠️ **ECONOMY MODE:** Low solar radiation detected. Switching system to low-compute prediction state to optimize battery cycles."
else:
    status_type = "SAFE"
    status_class = "safe-bg"
    status_msg = "🟢 **SYSTEM SAFE:** High solar irradiance. Cold storage is running at peak performance. Battery is healthily buffering energy."

st.markdown(f'<div class="{status_class}">{status_msg}</div>', unsafe_allowed_html=True)
st.markdown("<br>", unsafe_allowed_html=True)

# KPI Cards (The visual status indicators)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <h3 style="color: #00f2fe; margin:0;">📉 Predicted Discharge</h3>
            <h2 style="margin:10px 0;">{pred_discharge:.2f} % / hr</h2>
            <p style="color: #aaa; font-size: 12px;">Battery Depletion Speed</p>
        </div>
    """, unsafe_allowed_html=True)

with col2:
    # changing the border color of the card based on the status type to visually indicate the severity of the situation 
    b_color = "#dc3545" if status_type == "CRITICAL" else ("#ffc107" if status_type == "WARNING" else "#2e7d32")
    st.markdown(f"""
        <div class="kpi-card" style="border-left: 5px solid {b_color};">
            <h3 style="color: {b_color}; margin:0;">🔋 Dynamic Battery Status</h3>
            <h2 style="margin:10px 0;">{status_type}</h2>
            <p style="color: #aaa; font-size: 12px;">Deep Discharge Protection Mode</p>
        </div>
    """, unsafe_allowed_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <h3 style="color: #00f2fe; margin:0;">❄️ Cold Storage Temp</h3>
            <h2 style="margin:10px 0;">{pred_cold_temp:.1f} °C</h2>
            <p style="color: #aaa; font-size: 12px;">Internal Thermal Target</p>
        </div>
    """, unsafe_allowed_html=True)

# simulation (Visual Prediction Trend)
st.markdown("<br>### 📊 24-Hour Battery Depletion Projection", unsafe_allowed_html=True)

# Generate a simulated time series so the user can visualize the trend
hours = list(range(1, 25))
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