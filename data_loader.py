"""Load and prepare the natality data."""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import DATA_PATH, MONTH_ORDER, REQUIRED_COLUMNS, STATE_ABBR


def read_raw(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read the CSV without Streamlit (also used by tests)."""
    return pd.read_csv(path)


def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    """Rename columns, add state abbreviations and enforce chronological month order."""
    missing = [c for c in REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(f"Data file is missing required columns: {missing}")

    df = raw.rename(columns={
        "state_of_residence": "state", "sex_of_infant": "sex",
    }).copy()
    df["state"] = df["state"].str.strip()
    df["state_abbr"] = df["state"].map(STATE_ABBR)  # NaN if unmapped; validation flags it
    # Ordered categorical => charts and tables keep January..December order.
    df["month"] = pd.Categorical(df["month"], categories=MONTH_ORDER, ordered=True)
    return df.sort_values(["state", "month", "sex"]).reset_index(drop=True)


@st.cache_data(show_spinner="Loading CDC natality data...")
def load_data() -> pd.DataFrame:
    """Cached loader: the CSV is read and prepared once per session/server process."""
    return prepare(read_raw())
