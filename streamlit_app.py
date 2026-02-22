import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- MOBILE-FIRST CONFIG ---
st.set_page_config(
    page_title="Robot Monitor",
    page_icon="🤖",
    layout="centered", # Better for mobile/small screens
)

# --- INJECTION OF MOBILE CSS ---
st.markdown("""
    <style>
    /* Force metrics to be larger and centered */
    [data-testid="stMetricValue"] { font-size: 3rem !important; color: #f1c40f; }
    
    /* Optimize buttons for touch */
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    
    /* Clean up padding for small screens */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    
    .status-card {
        padding: 15px;
        border-radius: 12px;
        background-color: #1a1c24;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOCK DATA ---
def get_telemetry():
    return {
        "cycle_rate": round(np.random.uniform(12.8, 14.5), 1),
        "confidence": np.random.randint(85, 99),
        "picks": 1242,
        "status": "NOMINAL"
    }

# --- STATIC HEADER & ACTION BUTTONS ---
st.title("🚜 Robot Live")

# Big Action Button at the top for easy access
if st.button("🚩 FLAG PICK ERROR", type="primary"):
    st.toast("Error Logged!", icon="💾")

# --- REFRESHING DATA AREA ---
placeholder = st.empty()

# This loop stays stable because the buttons are OUTSIDE of it.
while True:
    data = get_telemetry()
    
    with placeholder.container():
        # Status Card
        st.markdown(f"""
            <div class="status-card">
                <span style="color: #888; font-size: 14px;">SYSTEM STATUS</span><br>
                <b style="color: #2ecc71; font-size: 24px;">● {data['status']}</b>
            </div>
        """, unsafe_allow_html=True)

        # Main Metrics (Stacked for Mobile)
        m1, m2 = st.columns(2)
        m1.metric("Picks/Min", data['cycle_rate'], delta="+0.2")
        m2.metric("AI Conf.", f"{data['confidence']}%")

        # Trend Chart (Simplified for mobile)
        st.write("### Throughput Trend")
        chart_data = pd.DataFrame(np.random.randn(15, 1) + 13.5, columns=['TPM'])
        st.line_chart(chart_data, color="#f1c40f", height=180)

        # Secondary Info
        st.write("---")
        c1, c2 = st.columns(2)
        c1.write(f"**Total Picks:** {data['picks']}")
        c2.write(f"**Updated:** {datetime.now().strftime('%H:%M:%S')}")

    time.sleep(1)
