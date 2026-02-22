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

# --- THE "NO-GHOSTING" KIOSK CSS ---
st.markdown("""
    <style>
    /* Force height and hide scrollbars */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow: hidden !important;
        height: 100vh !important;
        position: fixed;
        width: 100%;
        background-color: #000;
    }

    /* iPhone Island / Safe Area */
    .block-container {
        padding-top: 60px !important;
        max-width: 100% !important;
    }

    [data-testid="stMetricValue"] { font-size: 3.2rem !important; color: #f1c40f; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: #666; letter-spacing: 2px; }

    .stButton > button {
        width: 100%;
        height: 70px;
        background-color: #c0392b !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border: none;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STATIC TOP SECTION ---
st.markdown('<div style="color: #333; font-size: 10px; text-align: center; letter-spacing: 2px;">V-SYSTEM LIVE FEED</div>', unsafe_allow_html=True)

# Putting the button in a container ensures it doesn't shift
if st.button("REPORT PICK FAILURE", key="main_report_btn"):
    st.toast("EVENT LOGGED")

# --- DYNAMIC DATA SECTION ---
# This "placeholder" is the key to preventing duplicates. 
# Everything inside this container is wiped and replaced every second.
placeholder = st.empty()

# Initialization for mock trend
if 'data_history' not in st.session_state:
    st.session_state.data_history = [13.5] * 15

while True:
    # 1. Update Mock Data
    new_val = round(np.random.uniform(13.1, 14.5), 1)
    st.session_state.data_history.append(new_val)
    st.session_state.data_history = st.session_state.data_history[-15:]
    conf = np.random.randint(91, 98)
    
    # 2. Render inside the placeholder
    with placeholder.container():
        m1, m2 = st.columns(2)
        m1.metric("TIES / MIN", new_val)
        m2.metric("AI CONF", f"{conf}%")

        # Create a clean chart using the history
        chart_df = pd.DataFrame(st.session_state.data_history, columns=['TPM'])
        st.line_chart(chart_df, color="#f1c40f", height=200)

        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; color: #333; font-size: 9px; margin-top: 10px; font-family: monospace;">
                <span>UNIT-TX2-90</span>
                <span>SYNC: {datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        """, unsafe_allow_html=True)

    # 3. Controlled Sleep
    time.sleep(1)
