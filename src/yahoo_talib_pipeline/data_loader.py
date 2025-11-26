"""Functions for downloading and saving OHLCV data."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
import yfinance as yf


def _normalize_tickers(tickers: Iterable[str] | str) -> list[str]:
    """Coerce tickers into a list, handling the common case of a single string."""

    if tickers is None:
        return []
    if isinstance(tickers, str):
        tickers = [tickers]
    if isinstance(tickers, Sequence):
        return [t for t in tickers if t]
    return [t for t in list(tickers) if t]


def _normalize_date(value: str | None) -> str | None:
    """Treat empty strings as missing to align with yfinance defaults."""

    if value is None:
        return None
    value = value.strip()
    return value or None


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten any MultiIndex columns produced by yfinance."""

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    else:
        df.columns = [str(col) for col in df.columns]
    return df


def download_ohlcv(
    tickers: Iterable[str] | str,
    start: str | None = None,
    end: str | None = None,
    interval: str = "1d",
) -> pd.DataFrame:
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

    tickers_list = _normalize_tickers(tickers)
    start = _normalize_date(start)
    end = _normalize_date(end)

    if not tickers_list:
        return pd.DataFrame(columns=["ticker", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"])

    frames: list[pd.DataFrame] = []
    for ticker in tickers_list:
        data = yf.download(
            ticker,
            start=start,
            end=end,
            interval=interval,
            progress=False,
            group_by="column",
            auto_adjust=False,
        )
        if data.empty:
            continue
        data = _flatten_columns(data).reset_index()
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
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(df).to_csv(path_obj, index=False)
