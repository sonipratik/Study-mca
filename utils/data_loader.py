"""Data loading utilities - Complete version with DuckDB + CSV fallback"""
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
    """Load MCA data with DuckDB → CSV fallback."""
    if DUCKDB_FILE.exists():
        try:
            con = duckdb.connect(str(DUCKDB_FILE), read_only=True)
            df = con.execute("SELECT * FROM company_master_data").fetch_df()
            con.close()
            logger.info(f"Loaded {len(df):,} records from DuckDB")
            return normalize_columns(df)
        except Exception as e:
            logger.warning(f"DuckDB failed: {e}. Falling back to CSV...")

    if CSV_FILE.exists():
        logger.info("Loading from CSV...")
        df = pd.read_csv(CSV_FILE, low_memory=False)
        return normalize_columns(df)

    st.error("❌ Data file not found. Please upload company_master_data_2025_06_30.csv")
    return pd.DataFrame()


@st.cache_data
def get_data_summary(df: pd.DataFrame) -> dict:
    """Generate summary statistics."""
    summary = {
        'total_companies': len(df),
        'total_states': df['registered_state'].nunique() if 'registered_state' in df.columns else 0,
        'total_industries': df['industry'].nunique() if 'industry' in df.columns else 0,
        'active_companies': 0,
        'inactive_companies': 0,
        'total_authorized_capital': 0,
        'avg_authorized_capital': 0,
        'total_paid_up_capital': 0,
        'avg_paid_up_capital': 0,
    }

    if 'company_status' in df.columns:
        status_counts = df['company_status'].value_counts()
        summary['active_companies'] = status_counts.get('Active', 0)
        summary['inactive_companies'] = status_counts.get('Inactive', 0)

    if 'authorised_capital' in df.columns:
        summary['total_authorized_capital'] = df['authorised_capital'].sum()
        summary['avg_authorized_capital'] = df['authorised_capital'].mean()

    if 'paid_up_capital' in df.columns:
        summary['total_paid_up_capital'] = df['paid_up_capital'].sum()
        summary['avg_paid_up_capital'] = df['paid_up_capital'].mean()

    return summary


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess data for analysis."""
    df = df.copy()

    # Convert date columns
    for col in ['date_of_incorporation', 'registration_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Calculate company age
    if 'date_of_incorporation' in df.columns:
        df['company_age_years'] = (pd.Timestamp.now() - df['date_of_incorporation']).dt.days / 365.25

    # Convert capital columns to numeric
    for col in ['authorised_capital', 'paid_up_capital']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Fill missing defaults
    if 'authorised_capital' not in df.columns:
        df['authorised_capital'] = 0
    if 'paid_up_capital' not in df.columns:
        df['paid_up_capital'] = 0
    if 'company_status' not in df.columns:
        df['company_status'] = 'Unknown'
    if 'registered_state' not in df.columns:
        df['registered_state'] = 'Unknown'
    if 'industry' not in df.columns:
        df['industry'] = 'Unknown'

    return df
