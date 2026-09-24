"""Data-validation checks. Pure pandas, no Streamlit, so they are easy to test."""
import pandas as pd

from src.config import MONTH_ORDER, REPORTED_US_TOTAL_2025, SEXES, STATE_ABBR


def _result(name: str, passed: bool, detail: str) -> dict:
    return {"Check": name, "Status": "Pass" if passed else "FAIL", "Detail": detail}


def run_validation(df: pd.DataFrame) -> list[dict]:
    """Return a list of check results for the prepared dataframe."""
    checks = []

    nulls = int(df[["state", "month", "sex", "births"]].isna().sum().sum())
    checks.append(_result("No missing values", nulls == 0, f"{nulls} missing cells"))

    numeric = pd.api.types.is_numeric_dtype(df["births"])
    positive = bool((df["births"] > 0).all()) if numeric else False
    checks.append(_result("Births are numeric and positive", numeric and positive,
                          f"min = {df['births'].min():,}" if numeric else "non-numeric"))

    dups = int(df.duplicated(["state", "month", "sex"]).sum())
    checks.append(_result("No duplicate state/month/sex rows", dups == 0, f"{dups} duplicates"))

    n_states = df["state"].nunique()
    checks.append(_result("51 geographies (50 states + DC)", n_states == 51, f"{n_states} found"))

    months_ok = set(df["month"].dropna().unique()) == set(MONTH_ORDER)
    checks.append(_result("All 12 months present", months_ok, f"{df['month'].nunique()} found"))

    sexes_ok = set(df["sex"].unique()) == set(SEXES)
    checks.append(_result("Both infant-sex categories present", sexes_ok,
                          ", ".join(sorted(df["sex"].unique()))))

    unmapped = sorted(df.loc[df["state_abbr"].isna(), "state"].unique())
    checks.append(_result("Every state maps to an abbreviation", not unmapped,
                          "all mapped" if not unmapped else f"unmapped: {unmapped}"))

    missing = sorted(set(STATE_ABBR) - set(df["state"].unique()))
    checks.append(_result("No expected geography is missing", not missing,
                          "none missing" if not missing else f"missing: {missing}"))

    rows_per_state = df.groupby("state").size()
    complete = bool((rows_per_state == 24).all())
    checks.append(_result("Complete panel (24 rows per geography)", complete,
                          f"row counts: {sorted(rows_per_state.unique())}"))

    # month name and month_code must agree (January=1 ... December=12)
    codes_ok = bool((df["month"].cat.codes + 1 == df["month_code"]).all())
    checks.append(_result("month and month_code agree", codes_ok, "compared row by row"))

    total = int(df["births"].sum())
    diff = abs(total - REPORTED_US_TOTAL_2025) / REPORTED_US_TOTAL_2025
    checks.append(_result(
        "Total is close to NCHS published U.S. total",
        diff < 0.01,
        f"data = {total:,}; NCHS report = {REPORTED_US_TOTAL_2025:,} ({diff:.2%} difference)",
    ))
    return checks


def all_passed(results: list[dict]) -> bool:
    return all(r["Status"] == "Pass" for r in results)
