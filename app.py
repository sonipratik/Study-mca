"""MCA Insight Pro - Main Application"""
import sys
from pathlib import Path

# One-time path fix for reliable imports
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st

# Import render functions
from pages._1_dashboard import render_home
from pages._2_explorer import render_company_explorer
from pages._3_state import render_state_intelligence
from pages._4_industry import render_industry_intelligence
from pages._5_capital import render_capital_intelligence
from pages._6_comparison import render_company_comparison
from pages._7_ai import render_ai_insights
from pages._8_quality import render_data_quality
from pages._9_reports import render_reports_export
from pages._10_watchlist import render_watchlist

from utils.data_loader import load_mca_data

st.set_page_config(
    page_title="MCA Insight Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Navigation
st.sidebar.title("📊 MCA Insight Pro")
st.sidebar.markdown("---")

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

# Page Routing
if page == "Executive Dashboard":
    render_home()

elif page == "Company Explorer":
    render_company_explorer()

elif page == "State Intelligence":
    render_state_intelligence()

elif page == "Industry Intelligence":
    render_industry_intelligence()

elif page == "Capital Intelligence":
    render_capital_intelligence()

elif page == "Company Comparison":
    render_company_comparison()

elif page == "AI Insights":
    render_ai_insights()

elif page == "Data Quality":
    render_data_quality()

elif page == "Reports & Export":
    render_reports_export()

elif page == "Watchlist":
    render_watchlist()
