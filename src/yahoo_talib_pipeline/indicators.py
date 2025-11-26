"""Indicator calculation helpers using TA-Lib."""
from __future__ import annotations

from typing import Iterable

import pandas as pd
import talib


SUPPORTED_INDICATORS = {"RSI", "MACD"}


def _add_sma(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.SMA(df["Close"], timeperiod=period)


def _add_ema(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.EMA(df["Close"], timeperiod=period)


def _add_rsi(df: pd.DataFrame) -> pd.Series:
    return talib.RSI(df["Close"])


def _add_macd(df: pd.DataFrame) -> pd.DataFrame:
    macd, signal, hist = talib.MACD(df["Close"])
    return pd.DataFrame({"MACD": macd, "MACD_signal": signal, "MACD_hist": hist})


def _apply_indicator(df: pd.DataFrame, indicator: str) -> pd.DataFrame:
    if indicator.startswith("SMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_sma(df, period)
    elif indicator.startswith("EMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_ema(df, period)
    elif indicator == "RSI":
        df["RSI"] = _add_rsi(df)
    elif indicator == "MACD":
        macd_df = _add_macd(df)
        for col in macd_df.columns:
            df[col] = macd_df[col]
    else:
        raise ValueError(f"Unsupported indicator: {indicator}")
    return df


def compute_indicators(df: pd.DataFrame, indicators: Iterable[str]) -> pd.DataFrame:
    """Compute TA-Lib indicators for each ticker.

    Args:
        df: Input OHLCV DataFrame with a "ticker" column.
        indicators: Iterable of indicator identifiers (e.g., "RSI", "SMA_20").

    Returns:
        DataFrame with indicator columns appended per ticker.
    """

    if df.empty:
        return df

    indicators_list = list(indicators)
    grouped = []
    for ticker, group in df.groupby("ticker", sort=False):
        group = group.copy()
        for indicator in indicators_list:
            group = _apply_indicator(group, indicator)
        grouped.append(group)

    return pd.concat(grouped, ignore_index=True)
