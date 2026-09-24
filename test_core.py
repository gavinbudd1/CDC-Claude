"""Run with: pytest  (from the project root)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import pytest

from src import metrics
from src.config import MONTH_ORDER, STATE_ABBR
from src.data_loader import prepare, read_raw
from src.validation import all_passed, run_validation


@pytest.fixture(scope="module")
def df():
    return prepare(read_raw())


def test_validation_passes(df):
    assert all_passed(run_validation(df))


def test_validation_catches_duplicates(df):
    bad = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    results = {r["Check"]: r["Status"] for r in run_validation(bad)}
    assert results["No duplicate state/month/sex rows"] == "FAIL"


def test_state_mapping_is_complete_and_unique(df):
    assert set(df["state"]) == set(STATE_ABBR)
    assert len(set(STATE_ABBR.values())) == 51


def test_months_are_chronological(df):
    assert list(metrics.month_totals(df)["month"].astype(str)) == MONTH_ORDER


def test_kpis_consistent(df):
    k = metrics.compute_kpis(df)
    assert k["total"] == df["births"].sum()
    assert k["n_geos"] == 51
    assert k["avg_per_month"] == pytest.approx(k["total"] / 12)


def test_single_month_average(df):
    k = metrics.compute_kpis(df[df["month"] == "July"])
    assert k["avg_per_month"] == k["total"]


def test_top_bottom_sizes(df):
    tb = metrics.top_bottom(metrics.state_totals(df), 5)
    assert len(tb) == 10
