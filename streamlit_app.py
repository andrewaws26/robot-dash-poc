import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- KIOSK CONFIGURATION ---
st.set_page_config(
    page_title="Robot Operations",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- INJECTING INDUSTRIAL KIOSK CSS ---
st.markdown("""
    <style>
    /* 1. Eliminate Scroll & Force Viewport */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden;
        height: 100vh;
    }

    /* 2. iPhone Dynamic Island / Safe Area Padding */
    .block-container {
        padding-top: 65px !important; 
        padding-bottom: 20px !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* 3. Industrial Typography */
    [data-testid="stMetricValue"] { 
        font-size: 3.2rem !important; 
        font-weight: 800; 
        color: #f1c40f; 
        line-height: 1;
    }
    [data-testid="stMetricLabel"] { 
        font-size: 0.9rem !important; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        color: #888;
    }

    /* 4. Kiosk-Style Button */
    .stButton > button {
        width: 100%;
        height: 80px;
        background-color: #c0392b !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 24px !important;
        border-radius: 0px; /* Sharp industrial corners */
        border: 2px solid #7f231c;
        text-transform: uppercase;
    }

    /* 5. Status Card Styling */
    .status-card {
        background-color: #111;
        padding: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA ---
def get_telemetry():
    return {
        "tpm": round(np.random.uniform(13.1, 14.5), 1),
        "conf": np.random.randint(91, 98),
        "status": "SYSTEM NOMINAL"
    }

# --- KIOSK UI FLOW ---

# Header (Static)
st.markdown(f'<div class="status-card"><span style="color: #444; font-size: 12px; letter-spacing: 2px;">CONNECTION: {get_telemetry()["status"]}</span></div>', unsafe_allow_html=True)

# Main Action (Static)
if st.button("REPORT PICK FAILURE"):
    st.toast("EVENT LOGGED", icon="💾")

# Refreshing Section
placeholder = st.empty()

while True:
    data = get_telemetry()
    with placeholder.container():
        
        # Primary Metrics (Two columns, no vertical waste)
        m1, m2 = st.columns(2)
        m1.metric("TIES / MIN", data['tpm'])
        m2.metric("AI CONFIDENCE", f"{data['conf']}%")

        # Trend Chart (Height constrained to prevent scrolling)
        chart_data = pd.DataFrame(np.random.randn(15, 1) + 13.5, columns=['TPM'])
        st.line_chart(chart_data, color="#f1c40f", height=220)

        # Bottom Status (Small and out of the way)
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; color: #444; font-size: 10px; font-family: monospace; border-top: 1px solid #222; padding-top: 10px;">
                <span>STAUBLI TX2-90 CONTROL</span>
                <span>SYNC: {datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(1)
