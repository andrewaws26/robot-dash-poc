import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Stäubli TX2-90 Mission Control",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR INDUSTRIAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 48px; color: #f1c40f; }
    div[data-testid="stMetricDelta"] { font-size: 20px; }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
        background-color: #1a1c24;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA GENERATOR ---
# In production, replace these with requests.get() calls to the Stäubli/Apera APIs
def get_telemetry():
    return {
        "cycle_rate": round(np.random.uniform(12.8, 14.2), 1),
        "confidence": np.random.randint(88, 99),
        "pick_count": 1242,
        "magnet_temp": 42,
        "vision_latency": 142,
        "status": "NOMINAL"
    }

# --- HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🚜 Truck-Bed Robot Monitor")
    st.caption(f"System Active | Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
with col_h2:
    if st.button("🚩 FLAG PICK ERROR", use_container_width=True):
        st.toast("Error Event Logged for Analysis", icon="💾")

st.divider()

# --- MAIN DASHBOARD LAYOUT ---
# We use an empty container to refresh the data every second
placeholder = st.empty()

while True:
    data = get_telemetry()
    
    with placeholder.container():
        # ROW 1: MISSION CRITICAL METRICS
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Picks / Min", f"{data['cycle_rate']}", delta="Target: 15.0")
        m2.metric("AI Confidence", f"{data['confidence']}%", delta="High")
        m3.metric("Total Picks", f"{data['pick_count']:,}")
        m4.metric("Vision Latency", f"{data['vision_latency']}ms", delta="-12ms")

        st.write("###") # Vertical Spacing

        # ROW 2: SYSTEM HEALTH & LIVE TELEMETRY
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("📊 Production Trend (Last 60s)")
            # Simulating a trend line for throughput
            chart_data = pd.DataFrame(
                np.random.randn(20, 1) + 13.5,
                columns=['Ties/Min']
            )
            st.line_chart(chart_data, color="#f1c40f", height=250)

        with col_right:
            st.subheader("🔧 System Triage")
            
            # Status Indicator Display
            st.markdown(f"""
                <div class="status-box">
                    <p style="color: #888; margin-bottom: 5px;">CONTROLLER STATE</p>
                    <h2 style="color: #2ecc71; margin: 0;">{data['status']}</h2>
                    <hr style="border-color: #333;">
                    <p style="color: #888; margin-top: 10px;">SUBSYSTEMS</p>
                    <div style="text-align: left; padding-left: 20%;">
                        🟢 Stäubli CS9 Link<br>
                        🟢 Apera Vue Edge<br>
                        🟢 Imperx Cam 01
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("###")
            if st.button("🔄 Reset Cycle Timer", use_container_width=True):
                pass

        # FOOTER / LOGS
        with st.expander("View Raw Telemetry Stream"):
            st.write(data)

    time.sleep(1) # Refresh rate
