"""MCA Insight Pro - Single File Version (Stable on Streamlit Cloud)"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.data_loader import load_mca_data, get_data_summary, preprocess_data
from utils.insights import generate_dataset_insights
from components.ui_components import render_header, render_kpi_card, format_number, render_metric_row
from components.charts import (
    create_state_distribution_chart,
    create_industry_distribution_chart,
    create_status_distribution_chart,
    create_incorporation_trend_chart
)

st.set_page_config(page_title="MCA Insight Pro", page_icon="📊", layout="wide")

st.sidebar.title("📊 MCA Insight Pro")
page = st.sidebar.radio("Navigate", ["Executive Dashboard"])

df = load_mca_data()
if df.empty:
    st.stop()

df = preprocess_data(df)
summary = get_data_summary(df)

if page == "Executive Dashboard":
    render_header("MCA Insight Pro", "India's Corporate Intelligence Platform", "📊")

    # KPI Cards
    st.subheader("Key Performance Indicators")
    metrics = [
        {'label': 'Total Companies', 'value': f"{summary.get('total_companies', 0):,}", 'icon': '🏢', 'color': '#667eea'},
        {'label': 'Active Companies', 'value': f"{summary.get('active_companies', 0):,}", 'icon': '✅', 'color': '#22c55e'},
        {'label': 'Total States', 'value': f"{summary.get('total_states', 0)}", 'icon': '🗺️', 'color': '#f59e0b'},
        {'label': 'Total Industries', 'value': f"{summary.get('total_industries', 0)}", 'icon': '🏭', 'color': '#764ba2'},
    ]
    render_metric_row(metrics)

    # Capital
    st.subheader("Capital Metrics")
    capital_metrics = [
        {'label': 'Total Authorized Capital', 'value': format_number(summary.get('total_authorized_capital', 0), 2), 'icon': '💰', 'color': '#667eea'},
        {'label': 'Average Authorized Capital', 'value': format_number(summary.get('avg_authorized_capital', 0), 2), 'icon': '📈', 'color': '#764ba2'},
        {'label': 'Total Paid-Up Capital', 'value': format_number(summary.get('total_paid_up_capital', 0), 2), 'icon': '💵', 'color': '#22c55e'},
    ]
    render_metric_row(capital_metrics)

    # Status
    st.subheader("Company Status Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        render_kpi_card("Active", f"{summary.get('active_companies', 0):,}", "✅", "#22c55e",
                        f"{(summary.get('active_companies', 0) / max(summary.get('total_companies', 1), 1) * 100):.1f}%")
    with col2:
        render_kpi_card("Inactive", f"{summary.get('inactive_companies', 0):,}", "❌", "#ef4444",
                        f"{(summary.get('inactive_companies', 0) / max(summary.get('total_companies', 1), 1) * 100):.1f}%")

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_status_distribution_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(create_incorporation_trend_chart(df), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_state_distribution_chart(df), use_container_width=True)
    with col2:
        st.plotly_chart(create_industry_distribution_chart(df), use_container_width=True)

    # Insights
    st.subheader("Key Insights")
    for insight in generate_dataset_insights(df)[:6]:
        st.info(insight)
