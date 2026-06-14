"""Data loading with DuckDB + CSV fallback"""
import logging
from pathlib import Path
import pandas as pd
import duckdb
import streamlit as st

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DUCKDB_FILE = BASE_DIR / "data" / "company_master_data_2025_06_30.duckdb"
CSV_FILE = BASE_DIR / "company_master_data_2025_06_30.csv"

def normalize_columns(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    return df

@st.cache_data(ttl=3600)
def load_mca_data():
    if DUCKDB_FILE.exists():
        try:
            con = duckdb.connect(str(DUCKDB_FILE), read_only=True)
            df = con.execute("SELECT * FROM company_master_data").fetch_df()
            con.close()
            return normalize_columns(df)
        except:
            pass

    if CSV_FILE.exists():
        df = pd.read_csv(CSV_FILE, low_memory=False)
        return normalize_columns(df)

    st.error("Data file not found. Please upload company_master_data_2025_06_30.csv")
    return pd.DataFrame()
