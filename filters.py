"""Sidebar filters, Select All / Reset behavior and the active-filter summary."""
from dataclasses import dataclass

import pandas as pd
import streamlit as st

from src.config import MONTH_ORDER, SEXES

# (session_state key, select-all checkbox key) for each filter
_FILTERS = {
    "states": "all_states",
    "months": "all_months",
    "sexes": "all_sexes",
}


@dataclass
class FilterState:
    states: list
    months: list
    sexes: list
    n_states_total: int

    @property
    def is_empty(self) -> bool:
        return not (self.states and self.months and self.sexes)


def _defaults(all_states: list) -> dict:
    return {"states": list(all_states), "months": list(MONTH_ORDER), "sexes": list(SEXES)}


def _init_state(all_states: list) -> None:
    """Set defaults once per session (everything selected)."""
    for key, value in _defaults(all_states).items():
        if key not in st.session_state:
            st.session_state[key] = value
            st.session_state[_FILTERS[key]] = True


def _on_select_all(key: str, options: list) -> None:
    """Checkbox callback: check => select every option, uncheck => clear."""
    st.session_state[key] = list(options) if st.session_state[_FILTERS[key]] else []


def _on_multiselect(key: str, options: list) -> None:
    """Multiselect callback: keep the Select All checkbox in sync."""
    st.session_state[_FILTERS[key]] = len(st.session_state[key]) == len(options)


def _reset(all_states: list) -> None:
    for key, value in _defaults(all_states).items():
        st.session_state[key] = value
        st.session_state[_FILTERS[key]] = True


def _filter_block(label: str, key: str, options: list, help_text: str) -> None:
    st.checkbox("Select all", key=_FILTERS[key], on_change=_on_select_all,
                args=(key, options), help=f"Select or clear every {label.lower()}.")
    st.multiselect(label, options, key=key, on_change=_on_multiselect,
                   args=(key, options), help=help_text)


def render_sidebar(df: pd.DataFrame) -> FilterState:
    """Draw all sidebar controls and return the current selections."""
    all_states = sorted(df["state"].unique())
    _init_state(all_states)

    st.sidebar.header("Filters")
    with st.sidebar:
        _filter_block("State / geography", "states", all_states,
                      "50 states plus the District of Columbia (state of mother's residence).")
        _filter_block("Month", "months", MONTH_ORDER, "Months of 2025 in which births occurred.")
        _filter_block("Infant sex", "sexes", SEXES, "Female, male, or both.")
        st.button("Reset filters", on_click=_reset, args=(all_states,),
                  width="stretch")

    # Keep months chronological even if the user picked them out of order.
    months = [m for m in MONTH_ORDER if m in st.session_state["months"]]
    return FilterState(
        states=list(st.session_state["states"]),
        months=months,
        sexes=[s for s in SEXES if s in st.session_state["sexes"]],
        n_states_total=len(all_states),
    )


def apply_filters(df: pd.DataFrame, f: FilterState) -> pd.DataFrame:
    mask = (df["state"].isin(f.states) & df["month"].isin(f.months) & df["sex"].isin(f.sexes))
    return df[mask]


def _describe(selected: list, total: int, noun: str) -> str:
    if len(selected) == total:
        return f"All {total} {noun}"
    if not selected:
        return f"No {noun}"
    if len(selected) <= 3:
        return ", ".join(selected)
    return f"{len(selected)} of {total} {noun}"


def render_active_summary(f: FilterState) -> None:
    """Plain-language summary of what is currently selected."""
    st.sidebar.divider()
    st.sidebar.subheader("Active filters")
    st.sidebar.markdown(
        f"- **Geography:** {_describe(f.states, f.n_states_total, 'geographies')}\n"
        f"- **Months:** {_describe(f.months, 12, 'months')}\n"
        f"- **Infant sex:** {_describe(f.sexes, 2, 'sexes')}"
    )
