# U.S. Birth Counts, 2025 (Provisional) - Streamlit Dashboard

Interactive dashboard for exploring CDC/NCHS provisional 2025 birth **counts** (not rates)
by state, month and infant sex. Built for undergraduate business analytics students.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Push this folder to a GitHub repository (keep the `data/` folder).
2. On share.streamlit.io choose the repo and set the main file to `app.py`.

Paths are resolved relative to the code (`src/config.py`), so no changes are needed.

## Structure
| Path | Purpose |
|---|---|
| `app.py` | Page layout: header, KPIs, tabs |
| `src/config.py` | Paths, month order, state->abbreviation map, palette, source links |
| `src/data_loader.py` | Cached CSV loading and preparation |
| `src/validation.py` | Data-validation checks (shown in *About the Data*) |
| `src/filters.py` | Sidebar filters, Select All, Reset, active-filter summary |
| `src/metrics.py` | KPI and aggregation functions (no Streamlit) |
| `src/charts.py` | Plotly chart builders |
| `src/tabs/` | One module per tab |
| `tests/test_core.py` | `pytest` checks for validation and metrics |

## Adding a new chart
Write a function in `src/charts.py` that takes aggregated data and returns a Plotly figure, then call it
from the relevant tab with `st.plotly_chart(fig, width="stretch", key="a_unique_key")`.

## Data
`data/Provisional_Natality_2025_CDC.csv`: 51 geographies x 12 months x 2 sexes = 1,224 rows.
Columns: `state_of_residence, month, month_code, year_code, sex_of_infant, births`.
