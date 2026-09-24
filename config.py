"""Constants shared across the dashboard: paths, month order, state codes, palette."""
from pathlib import Path

# Resolve paths from this file so they work locally and on Streamlit Community Cloud
# regardless of the directory the app is launched from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "Provisional_Natality_2025_CDC.csv"

# Columns we expect in the CSV.
REQUIRED_COLUMNS = [
    "state_of_residence", "month", "month_code", "year_code", "sex_of_infant", "births",
]

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

# Explicit mapping (50 states + DC) used for the choropleth. Kept hand-written so a
# missing or misspelled state is caught by validation rather than silently dropped.
STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}

SEXES = ["Female", "Male"]

# Okabe-Ito colorblind-safe colors; sex is also encoded by position/legend, not color alone.
SEX_COLORS = {"Female": "#E69F00", "Male": "#0072B2"}
PRIMARY_COLOR = "#0072B2"
SEQUENTIAL_SCALE = "Viridis"  # perceptually uniform and colorblind-friendly

SOURCE_NAME = "CDC / National Center for Health Statistics (NCHS), Provisional Natality data via CDC WONDER"
SOURCE_URL = "https://wonder.cdc.gov/natality-current.html"
REPORT_URL = "https://www.cdc.gov/nchs/data/vsrr/vsrr043.pdf"
# Published provisional 2025 U.S. total (NCHS VSRR Report No. 43), used as a sanity check.
REPORTED_US_TOTAL_2025 = 3_606_400
