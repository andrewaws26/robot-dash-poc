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

# --- THE KIOSK "LOCK" CSS ---
st.markdown("""
    <style>
    /* 1. Nuke the ability to scroll anywhere */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow: hidden !important;
        height: 100vh !important;
        position: fixed;
        width: 100%;
    }

    /* 2. Remove Streamlit's default padding/header */
    [data-testid="stHeader"] { display: none; }
    .block-container {
        padding-top: 55px !important; /* iPhone Island Clear */
        padding-bottom: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* 3. Scale text for Dash visibility */
    [data-testid="stMetricValue"] { font-size: 2.8rem !important; color: #f1c40f; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; letter-spacing: 2px; }

    /* 4. Industrial Button Style */
    .stButton > button {
        width: 100%;
        height: 65px;
        background-color: #c0392b !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        border-radius: 4px;
        border: none;
        text-transform: uppercase;
    }

    /* 5. Status strip */
    .status-strip {
        background-color: #111;
        padding: 8px;
        border: 1px solid #222;
        text-align: center;
        color: #555;
        font-size: 10px;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP CONTENT ---

# Connection Bar
st.markdown('<div class="status-strip">STAUBLI CS9: CONNECTED</div>', unsafe_allow_html=True)

# Action Button
if st.button("REPORT PICK FAILURE"):
    st.toast("EVENT LOGGED")

# Live Data Region
placeholder = st.empty()

while True:
    tpm = round(np.random.uniform(13.1, 14.5), 1)
    conf = np.random.randint(91, 98)
    
    with placeholder.container():
        # Metrics Grid
        m1, m2 = st.columns(2)
        m1.metric("TIES / MIN", tpm)
        m2.metric("AI CONF", f"{conf}%")

        # Compact Chart (Set specifically to 180 to prevent overflow)
        chart_data = pd.DataFrame(np.random.randn(15, 1) + 13.5, columns=['TPM'])
        st.line_chart(chart_data, color="#f1c40f", height=180)

        # Bottom Footer
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; color: #333; font-size: 9px; margin-top: 10px; font-family: monospace;">
                <span>V-SYSTEM 1.0</span>
                <span>{datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(1)
