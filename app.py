"""MCA Insight Pro - Main Application"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.data_loader import load_mca_data, preprocess_data

st.set_page_config(
    page_title="MCA Insight Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Navigation
st.sidebar.title("📊 MCA Insight Pro")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Dashboard",
        "Company Explorer",
        "State Intelligence",
        "Industry Intelligence",
        "Capital Intelligence",
        "Company Comparison",
        "AI Insights",
        "Data Quality",
        "Reports & Export",
        "Watchlist"
    ]
)

# Load data once
df = load_mca_data()
if df.empty:
    st.stop()

df = preprocess_data(df)

# Page routing
if page == "Executive Dashboard":
    from pages._1_dashboard import render_home
    render_home(df)

elif page == "Company Explorer":
    from pages._2_explorer import render_company_explorer
    render_company_explorer(df)

elif page == "State Intelligence":
    from pages._3_state import render_state_intelligence
    render_state_intelligence(df)

elif page == "Industry Intelligence":
    from pages._4_industry import render_industry_intelligence
    render_industry_intelligence(df)

elif page == "Capital Intelligence":
    from pages._5_capital import render_capital_intelligence
    render_capital_intelligence(df)

elif page == "Company Comparison":
    from pages._6_comparison import render_company_comparison
    render_company_comparison(df)

elif page == "AI Insights":
    from pages._7_ai import render_ai_insights
    render_ai_insights(df)

elif page == "Data Quality":
    from pages._8_quality import render_data_quality
    render_data_quality(df)

elif page == "Reports & Export":
    from pages._9_reports import render_reports_export
    render_reports_export(df)

elif page == "Watchlist":
    from pages._10_watchlist import render_watchlist
    render_watchlist(df)
