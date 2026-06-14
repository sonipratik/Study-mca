"""MCA Insight Pro - Main Application"""
import streamlit as st
from pathlib import Path
import sys

# Add project root to sys.path (only needed once)
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="MCA Insight Pro",
    page_icon="📊",
    layout="wide",
)

# Define all pages using st.navigation (most reliable method on Streamlit Cloud)
pages = {
    "Dashboard": [
        st.Page("pages/1_Executive_Dashboard.py", title="Executive Dashboard", icon="📊"),
        st.Page("pages/2_Company_Explorer.py", title="Company Explorer", icon="🔍"),
        st.Page("pages/3_State_Intelligence.py", title="State Intelligence", icon="🗺️"),
        st.Page("pages/4_Industry_Intelligence.py", title="Industry Intelligence", icon="🏭"),
        st.Page("pages/5_Capital_Intelligence.py", title="Capital Intelligence", icon="💰"),
        st.Page("pages/6_Company_Comparison.py", title="Company Comparison", icon="⚖️"),
        st.Page("pages/7_AI_Insights.py", title="AI Insights", icon="🤖"),
        st.Page("pages/8_Data_Quality.py", title="Data Quality", icon="✅"),
        st.Page("pages/9_Reports_Export.py", title="Reports & Export", icon="📄"),
        st.Page("pages/10_Watchlist.py", title="Watchlist", icon="⭐"),
    ]
}

pg = st.navigation(pages)
pg.run()
