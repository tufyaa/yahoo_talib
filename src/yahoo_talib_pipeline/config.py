"""Configuration for file paths and defaults."""
from pathlib import Path

# Base directory for data outputs
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PRICES_CSV = DATA_DIR / "prices.csv"
PRICES_WITH_INDICATORS_CSV = DATA_DIR / "prices_with_indicators.csv"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
