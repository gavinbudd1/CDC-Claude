"""Monthly and Sex Analysis tab."""
import streamlit as st

from src import charts, metrics


def render(df) -> None:
    st.plotly_chart(charts.monthly_trend(metrics.month_totals(df)), width="stretch", key="ms_trend")

    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(charts.sex_comparison(metrics.sex_month_totals(df)),
                        width="stretch", key="ms_sex_month")
    with right:
        st.plotly_chart(charts.sex_share(metrics.sex_totals(df)), width="stretch", key="ms_sex_total")

    if df["sex"].nunique() < 2:
        st.info("Only one infant sex is selected, so there is nothing to compare. "
                "Select both to see the female/male comparison.")
    st.caption("Monthly counts also reflect the number of days in each month.")
