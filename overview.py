"""Overview tab: the big picture for the current selection."""
import streamlit as st

from src import charts, metrics


def render(df) -> None:
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(charts.monthly_trend(metrics.month_totals(df)), width="stretch", key="ov_trend")
    with right:
        st.plotly_chart(charts.state_ranking(metrics.state_totals(df), 10),
                        width="stretch", key="ov_rank")
    st.plotly_chart(charts.choropleth(metrics.state_totals(df)), width="stretch", key="ov_map")
    st.caption("Larger states have more births simply because they have more people. "
               "These are counts, not birth rates.")
