"""Geographic Analysis tab: map, ranking, top/bottom comparison and heatmap."""
import streamlit as st

from src import charts, metrics


def _count_control(label: str, max_n: int, default: int, key: str) -> int:
    """Slider when there is a range to choose from; otherwise just return the only option."""
    if max_n <= 1:
        return 1
    return st.slider(label, 1, max_n, min(default, max_n), key=key)


def render(df) -> None:
    totals = metrics.state_totals(df)
    n_geo = len(totals)

    st.plotly_chart(charts.choropleth(totals), width="stretch", key="geo_map")

    st.subheader("State ranking")
    n = _count_control("Number of geographies to show", n_geo, 15, "rank_n")
    st.plotly_chart(charts.state_ranking(totals, n), width="stretch", key="geo_rank")

    st.subheader("Highest vs. lowest")
    if n_geo < 2:
        st.info("Select at least two geographies to compare highest and lowest.")
    else:
        k = _count_control("Geographies in each group", min(10, n_geo // 2), 5, "tb_n")
        st.plotly_chart(charts.top_bottom_chart(metrics.top_bottom(totals, k)),
                        width="stretch", key="geo_topbottom")

    st.subheader("State-by-month heatmap")
    st.plotly_chart(charts.state_month_heatmap(metrics.state_month_matrix(df)),
                    width="stretch", key="geo_heatmap")
    st.caption("Lighter and darker cells show higher and lower counts. Month lengths differ, "
               "so short months such as February naturally have fewer births.")
