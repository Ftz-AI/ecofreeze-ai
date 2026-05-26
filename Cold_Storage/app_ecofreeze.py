import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Page configuration
st.set_page_config(page_title="EcoFreeze AI Optimizer", page_icon="🔋", layout="wide")

# Loading the pre-trained models safely
@st.cache_resource
def load_models():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    
    discharge_path = os.path.join(base_dir, 'model_discharge.pkl')
    temp_path = os.path.join(base_dir, 'model_temp.pkl')
    

    m_discharge = joblib.load(discharge_path)
    m_temp = joblib.load(temp_path)
    return m_discharge, m_temp

model_discharge, model_temp = load_models()

# Dashboard Main Headers
st.title("🔋 EcoFreeze AI: Off-Grid Battery & Thermal Optimizer")
st.subheader("Smart Predictive Input Engine for Sub-Saharan Cold Storages")
st.markdown("---")

# --- PREMIUM CONTROL CENTER (SIDEBAR) ---

st.sidebar.markdown("## ⚙️ Control Center")
st.sidebar.markdown("Adjust environmental variables to simulate live sub-Saharan grid conditions.")


with st.sidebar.expander("🌤️ Climate & Weather Inputs", expanded=True):
    ambient_temp = st.slider(
        "Ambient Temperature", 
        min_value=25.0, max_value=45.0, value=32.0, step=0.5,
        help="Outside temperature in Nigeria. High heat increases cooling load.",
        format="%f °C"
    )
    
    solar_irradiance = st.slider(
        "Solar Irradiance", 
        min_value=0, max_value=1000, value=450, step=10,
        help="Solar radiation power. 0W/m² represents night-time simulation.",
        format="%d W/m²"
    )


with st.sidebar.expander("🔋 System Infrastructure", expanded=True):
    battery_health = st.slider(
        "Battery Health Index (SOH)", 
        min_value=50, max_value=100, value=85, step=1,
        help="State of Health of the lithium-ion storage bank.",
        format="%d %%"
    )


st.sidebar.markdown("---")
st.sidebar.caption(
    "💡 **SYSTEM ARCHITECTURE NOTE:**\n"
    "This low-compute linear model acts as a real-time edge input for Energy Management Systems "
    "to actively protect battery health and prevent deep discharge in off-grid operations."
)




# --- AI MODEL PREDICTIONS ---
# Model prediction based on live user inputs
input_data = pd.DataFrame([[ambient_temp, solar_irradiance, battery_health]], 
                          columns=['Ambient_Temperature', 'Solar_Irradiance', 'Battery_Health'])

pred_discharge = max(0.0, float(model_discharge.predict(input_data)[0]))
pred_cold_temp = float(model_temp.predict(input_data)[0])


# --- AI GUARD LOGIC & DISPLAY ---
st.markdown("### 🧠 AI Guard: Live System Status & Action Logic")

# Decision Logic using Streamlit's Native Premium Alert Components
if solar_irradiance < 200 and pred_discharge > 12:
    status_type = "CRITICAL"
    st.error("🚨 **CRITICAL RISK:** Deep Discharge Alert! Solar generation is offline and battery drain is heavy. **Action:** Dimming cold storage cooling cycles immediately to preserve battery lifespan.")
elif solar_irradiance < 400 or pred_discharge > 8:
    status_type = "WARNING"
    st.warning("⚠️ **ECONOMY MODE:** Low solar radiation detected. Switching system to low-compute prediction state to optimize battery cycles.")
else:
    status_type = "SAFE"
    st.success("🟢 **SYSTEM SAFE:** High solar irradiance. Cold storage is running at peak performance. Battery is healthily buffering energy.")

st.markdown("<br>", unsafe_allow_html=True)


# --- KPI METRICS DISPLAY ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="📉 Predicted Discharge Rate", 
        value=f"{pred_discharge:.2f} % / hr", 
        delta="- Battery Depletion Speed"
    )

with col2:
    
    delta_msg = "Critical Alert" if status_type == "CRITICAL" else ("Warning State" if status_type == "WARNING" else "Optimal State")
    st.metric(
        label="🔋 Dynamic Battery Status", 
        value=status_type, 
        delta=delta_msg,
        delta_color="inverse" if status_type != "SAFE" else "normal"
    )

with col3:
    st.metric(
        label="❄️ Cold Storage Internal Temp", 
        value=f"{pred_cold_temp:.1f} °C", 
        delta="Target Thermal Level"
    )


# --- 24-HOUR PROJECTION CHART ---
st.markdown("<br> 📊 24-Hour Battery Depletion Projection", unsafe_allow_html=True)

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
