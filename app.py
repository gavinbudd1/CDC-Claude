"""Streamlit dashboard: 2025 provisional U.S. birth counts by state, month and infant sex."""
import streamlit as st

from src import filters, metrics
from src.config import SOURCE_NAME, SOURCE_URL
from src.data_loader import load_data
from src.tabs import about, data_table, geographic, monthly_sex, overview
from src.validation import all_passed, run_validation

st.set_page_config(page_title="U.S. Births 2025 (Provisional)", page_icon="📊", layout="wide")


def render_header() -> None:
    st.title("U.S. Birth Counts, 2025")
    st.write("Explore how births differ across states, months and infant sex. "
             "Use the sidebar filters to change what every chart and number shows.")
    st.caption(f"Source: [{SOURCE_NAME}]({SOURCE_URL}).")
    st.warning("**Provisional data.** These figures are preliminary and may be revised.", icon="⚠️")
    st.info("**These are birth counts, not birth rates.** Counts mostly reflect population size, "
            "so they should not be used to say one state has higher fertility than another.",
            icon="ℹ️")


def render_kpis(df) -> None:
    k = metrics.compute_kpis(df)
    cols = st.columns(5)
    cols[0].metric("Total births", f"{k['total']:,}")
    cols[1].metric("Geographies selected", f"{k['n_geos']:,}")
    cols[2].metric("Avg births per month", f"{k['avg_per_month']:,.0f}",
                   help="Total births divided by the number of selected months.")
    cols[3].metric("Top geography", k["top_state"], f"{k['top_state_births']:,} births",
                   delta_color="off")
    cols[4].metric("Top month", k["top_month"], f"{k['top_month_births']:,} births",
                   delta_color="off")


def main() -> None:
    df = load_data()
    validation = run_validation(df)

    render_header()
    if not all_passed(validation):
        st.error("Data validation failed. See the *About the Data* tab for details.")

    f = filters.render_sidebar(df)
    filters.render_active_summary(f)
    filtered = filters.apply_filters(df, f)

    if filtered.empty:
        st.warning("No observations match the current filters. Select at least one geography, "
                   "one month and one infant sex, or press **Reset filters**.")
        st.stop()

    render_kpis(filtered)

    tabs = st.tabs(["Overview", "Geographic Analysis", "Monthly and Sex Analysis",
                    "Data Table and Download", "About the Data"])
    with tabs[0]:
        overview.render(filtered)
    with tabs[1]:
        geographic.render(filtered)
    with tabs[2]:
        monthly_sex.render(filtered)
    with tabs[3]:
        data_table.render(filtered, filter_summary=(
            f"{len(f.states)} geographies, {len(f.months)} months, {', '.join(f.sexes)}"))
    with tabs[4]:
        about.render(validation)


main()
