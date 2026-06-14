"""Data loading utilities - DuckDB + CSV fallback (Fixed for Streamlit Cloud)"""
import logging
from pathlib import Path
import pandas as pd
import duckdb
import streamlit as st

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DUCKDB_FILE = DATA_DIR / "company_master_data_2025_06_30.duckdb"
CSV_FILE = BASE_DIR / "company_master_data_2025_06_30.csv"   # fallback


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names."""
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


@st.cache_data(ttl=3600)
def load_mca_data() -> pd.DataFrame:
    """
    Load MCA data with fallback.
    1. Try DuckDB first
    2. If DuckDB fails → try CSV
    """
    # === Try DuckDB ===
    if DUCKDB_FILE.exists():
        try:
            con = duckdb.connect(str(DUCKDB_FILE), read_only=True)
            df = con.execute("SELECT * FROM company_master_data").fetch_df()
            con.close()
            logger.info(f"Loaded {len(df):,} records from DuckDB")
            return normalize_columns(df)
        except Exception as e:
            logger.warning(f"DuckDB failed: {e}. Trying CSV fallback...")

    # === Fallback to CSV ===
    if CSV_FILE.exists():
        logger.info("Loading from CSV file (this may take time on first run)...")
        df = pd.read_csv(CSV_FILE, low_memory=False)
        return normalize_columns(df)

    # === Nothing worked ===
    st.error(
        "❌ Data file not found or invalid.\n\n"
        "Please upload `company_master_data_2025_06_30.csv` "
        "in the project root folder."
    )
    return pd.DataFrame()
