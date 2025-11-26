"""Configuration for file paths and defaults."""
from pathlib import Path

# Base directory for data outputs at the repo root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PRICES_CSV = DATA_DIR / "prices.csv"
PRICES_WITH_INDICATORS_CSV = DATA_DIR / "prices_with_indicators.csv"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)
