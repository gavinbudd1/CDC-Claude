"""Aggregations and KPIs on the filtered data. Pure pandas, no Streamlit."""
import pandas as pd


def state_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Births per state, highest first, with abbreviations for mapping."""
    out = df.groupby(["state", "state_abbr"], as_index=False, observed=True)["births"].sum()
    return out.sort_values("births", ascending=False).reset_index(drop=True)


def month_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Births per month in calendar order (months with no data are omitted)."""
    out = df.groupby("month", as_index=False, observed=True)["births"].sum()
    return out.sort_values("month").reset_index(drop=True)


def sex_month_totals(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby(["month", "sex"], as_index=False, observed=True)["births"].sum()
    return out.sort_values(["month", "sex"]).reset_index(drop=True)


def sex_totals(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("sex", as_index=False, observed=True)["births"].sum()


def compute_kpis(df: pd.DataFrame) -> dict:
    """KPI values for the current selection (df must be non-empty)."""
    by_state = state_totals(df)
    by_month = month_totals(df)
    total = int(df["births"].sum())
    top_month_row = by_month.loc[by_month["births"].idxmax()]
    return {
        "total": total,
        "n_geos": int(df["state"].nunique()),
        "avg_per_month": total / df["month"].nunique(),
        "top_state": by_state.iloc[0]["state"],
        "top_state_births": int(by_state.iloc[0]["births"]),
        "top_month": str(top_month_row["month"]),
        "top_month_births": int(top_month_row["births"]),
    }


def state_month_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Rows = states (largest total first), columns = months in calendar order."""
    pivot = df.pivot_table(index="state", columns="month", values="births",
                           aggfunc="sum", observed=True)
    return pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]


def top_bottom(totals: pd.DataFrame, n: int) -> pd.DataFrame:
    """Highest-n and lowest-n geographies from a state_totals frame, labeled by group."""
    n = max(1, min(n, len(totals) // 2 or 1))
    top = totals.head(n).assign(group=f"Highest {n}")
    bottom = totals.tail(n).assign(group=f"Lowest {n}")
    return pd.concat([top, bottom], ignore_index=True)
