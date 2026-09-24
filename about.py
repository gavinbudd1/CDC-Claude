"""About the Data tab: source, definitions, caveats and validation results."""
import pandas as pd
import streamlit as st

from src.config import REPORT_URL, SOURCE_NAME, SOURCE_URL
from src.validation import all_passed


def render(validation_results: list[dict]) -> None:
    st.markdown(f"""
### Source
{SOURCE_NAME}. Data portal: [CDC WONDER Natality]({SOURCE_URL}). National context:
[NCHS *Births: Provisional Data for 2025*]({REPORT_URL}).

### What each row means
Each row is the number of live births for one **state of residence**, one **month of 2025** and one
**infant sex**. There are 51 geographies (50 states + DC) × 12 months × 2 sexes = 1,224 rows.

### Important cautions
- **Provisional:** figures are based on records received so far and may be revised in final data.
- **Counts, not rates:** a birth *rate* divides births by a population (for example, women aged
  15–44). This dashboard shows counts only, so large states rank high mostly because they are large.
  Do not read a ranking of counts as "where people have more children."
- **Residence-based:** births are assigned to the mother's state of residence, not where the
  birth occurred.
- **One year only:** there is no multi-year trend in this file.
- Months differ in length, which affects monthly comparisons.

### Data validation
Checks run each time the data are loaded:
""")
    st.dataframe(pd.DataFrame(validation_results), hide_index=True, width="stretch")
    if all_passed(validation_results):
        st.success("All validation checks passed.")
    else:
        st.error("One or more validation checks failed. Interpret results with caution.")
