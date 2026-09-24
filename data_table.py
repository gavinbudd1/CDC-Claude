"""Data Table and Download tab."""
import streamlit as st


def render(df, filter_summary: str) -> None:
    query = st.text_input("Search table", placeholder="Type a state, month or sex (e.g. Texas, July, Female)",
                          help="Case-insensitive match on state, month or infant sex.")

    view = df[["state", "month", "sex", "births"]].rename(
        columns={"state": "State", "month": "Month", "sex": "Infant sex", "births": "Births"})
    view["Month"] = view["Month"].astype(str)  # plain text so search/sort behave predictably

    if query.strip():
        q = query.strip().lower()
        text = view[["State", "Month", "Infant sex"]].agg(" ".join, axis=1).str.lower()
        view = view[text.str.contains(q, regex=False)]

    if view.empty:
        st.warning("No rows match your search. Try a different term or clear the search box.")
        return

    st.caption(f"{len(view):,} rows · Filters: {filter_summary}")
    # Styler gives thousands separators; sorting still uses the underlying numbers.
    st.dataframe(view.style.format({"Births": "{:,}"}), width="stretch",
                 hide_index=True, height=480)

    st.download_button("Download this table as CSV", view.to_csv(index=False).encode("utf-8"),
                       file_name="natality_2025_filtered.csv", mime="text/csv",
                       help="Includes the sidebar filters and the search above.")
