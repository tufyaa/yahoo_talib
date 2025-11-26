"""Functions for downloading and saving OHLCV data."""
from __future__ import annotations

from typing import Iterable

import pandas as pd
import yfinance as yf


def download_ohlcv(tickers: Iterable[str], start: str, end: str, interval: str = "1d") -> pd.DataFrame:
    """
    Download OHLCV data for the given tickers and date range.

    Args:
        tickers: Iterable of ticker symbols.
        start: Start date in YYYY-MM-DD format.
        end: End date in YYYY-MM-DD format.
        interval: Data interval supported by yfinance (e.g., "1d", "1h").

    Returns:
        Combined DataFrame with OHLCV columns and an extra "ticker" column.
    """

    frames: list[pd.DataFrame] = []
    for ticker in tickers:
        data = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
        if data.empty:
            continue
        data = data.reset_index().rename(columns={"Adj Close": "Adj Close"})
        data.insert(0, "ticker", ticker)
        frames.append(data)

    if not frames:
        return pd.DataFrame(columns=["ticker", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])

    combined = pd.concat(frames, ignore_index=True)
    # Ensure column order
    expected_cols = ["ticker", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    for col in expected_cols:
        if col not in combined.columns:
            combined[col] = pd.NA
    return combined[expected_cols]


def save_to_csv(df: pd.DataFrame, path: str | bytes | None) -> None:
    """Save a DataFrame to CSV at the given path."""

    if path is None:
        raise ValueError("Path to save CSV cannot be None.")
    pd.DataFrame(df).to_csv(path, index=False)
