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

# --- THE "NUKE" CSS: Fixes the white bar and margins ---
st.markdown("""
    <style>
    /* 1. Remove all default Streamlit padding/margins and the white sidebar area */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stHeader"] { display: none; }
    [data-testid="stAppViewContainer"] { background-color: #000; }
    
    .main .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* 2. Kiosk Container (The Parent) */
    .kiosk-wrapper {
        height: 100vh;
        width: 100vw;
        display: flex;
        flex-direction: column;
        background-color: #000;
        /* Dynamic Island Offset */
        padding-top: 60px; 
        padding-left: 15px;
        padding-right: 15px;
        padding-bottom: 20px;
        box-sizing: border-box;
        overflow: hidden;
    }

    /* 3. Typography & UI Elements */
    [data-testid="stMetricValue"] { font-size: 3.5rem !important; color: #f1c40f; line-height: 1; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: #666; letter-spacing: 2px; }

    .stButton > button {
        width: 100%;
        height: 75px;
        background-color: #c0392b !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border: none;
        text-transform: uppercase;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .status-bar {
        background-color: #111;
        padding: 10px;
        border: 1px solid #222;
        text-align: center;
        color: #444;
        font-size: 10px;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- WRAP EVERYTHING IN THE KIOSK DIV ---
# This ensures Streamlit doesn't inject its own margins
st.markdown('<div class="kiosk-wrapper">', unsafe_allow_html=True)

# 1. Status Bar
st.markdown('<div class="status-bar">CONNECTION: NOMINAL</div>', unsafe_allow_html=True)

# 2. Critical Action
if st.button("REPORT PICK FAILURE"):
    st.toast("LOGGED")

# 3. Dynamic Data Section
placeholder = st.empty()

while True:
    tpm = round(np.random.uniform(13.1, 14.5), 1)
    conf = np.random.randint(91, 98)
    
    with placeholder.container():
        # Metric Grid
        m1, m2 = st.columns(2)
        m1.metric("TIES / MIN", tpm)
        m2.metric("AI CONF", f"{conf}%")

        # Compact Chart
        chart_data = pd.DataFrame(np.random.randn(15, 1) + 13.5, columns=['TPM'])
        st.line_chart(chart_data, color="#f1c40f", height=220)

        # Bottom ID
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; color: #333; font-size: 9px; margin-top: 15px; font-family: monospace;">
                <span>UNIT-TX2-90</span>
                <span>SYNC: {datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        """, unsafe_allow_html=True)

    time.sleep(1)

st.markdown('</div>', unsafe_allow_html=True) # Close Kiosk Wrapper
