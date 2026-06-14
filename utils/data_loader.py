"""Data loading utilities with DuckDB + CSV fallback"""
import logging
from pathlib import Path
import pandas as pd
import duckdb
import streamlit as st

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DUCKDB_FILE = DATA_DIR / "company_master_data_2025_06_30.duckdb"
CSV_FILE = BASE_DIR / "company_master_data_2025_06_30.csv"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for consistency."""
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
    Load MCA Master Data.
    Priority: DuckDB → CSV fallback
    """
    # Try DuckDB first
    if DUCKDB_FILE.exists():
        try:
            con = duckdb.connect(str(DUCKDB_FILE), read_only=True)
            df = con.execute("SELECT * FROM company_master_data").fetch_df()
            con.close()
            logger.info(f"Loaded {len(df):,} records from DuckDB")
            return normalize_columns(df)
        except Exception as e:
            logger.warning(f"DuckDB failed: {e}. Falling back to CSV...")

    # Fallback to CSV
    if CSV_FILE.exists():
        logger.info("Loading from CSV file...")
        df = pd.read_csv(CSV_FILE, low_memory=False)
        return normalize_columns(df)

    st.error("❌ No data file found. Please place either the .duckdb or .csv file in the project root.")
    return pd.DataFrame()
