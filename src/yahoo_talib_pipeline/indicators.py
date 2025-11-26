"""Indicator calculation helpers using TA-Lib."""
from __future__ import annotations

from typing import Iterable

import pandas as pd
import talib


SUPPORTED_INDICATORS = {
    "RSI",
    "MACD",
    "OBV",
    "SMA",
    "EMA",
    "WMA",
    "DEMA",
    "TEMA",
    "KAMA",
    "ATR",
    "ADX",
    "CCI",
    "ROC",
    "MOM",
    "BBANDS",
}


def _add_sma(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.SMA(df["Close"], timeperiod=period)


def _add_ema(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.EMA(df["Close"], timeperiod=period)


def _add_wma(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.WMA(df["Close"], timeperiod=period)


def _add_dema(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.DEMA(df["Close"], timeperiod=period)


def _add_tema(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.TEMA(df["Close"], timeperiod=period)


def _add_kama(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.KAMA(df["Close"], timeperiod=period)


def _add_rsi(df: pd.DataFrame) -> pd.Series:
    return talib.RSI(df["Close"])


def _add_macd(df: pd.DataFrame) -> pd.DataFrame:
    macd, signal, hist = talib.MACD(df["Close"])
    return pd.DataFrame({"MACD": macd, "MACD_signal": signal, "MACD_hist": hist})


def _add_atr(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.ATR(df["High"], df["Low"], df["Close"], timeperiod=period)


def _add_adx(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.ADX(df["High"], df["Low"], df["Close"], timeperiod=period)


def _add_cci(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.CCI(df["High"], df["Low"], df["Close"], timeperiod=period)


def _add_roc(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.ROC(df["Close"], timeperiod=period)


def _add_mom(df: pd.DataFrame, period: int) -> pd.Series:
    return talib.MOM(df["Close"], timeperiod=period)


def _add_obv(df: pd.DataFrame) -> pd.Series:
    return talib.OBV(df["Close"], df["Volume"])


def _add_bbands(df: pd.DataFrame, period: int) -> pd.DataFrame:
    upper, middle, lower = talib.BBANDS(df["Close"], timeperiod=period)
    return pd.DataFrame({
        f"BBANDS_upper_{period}": upper,
        f"BBANDS_middle_{period}": middle,
        f"BBANDS_lower_{period}": lower,
    })


def _apply_indicator(df: pd.DataFrame, indicator: str) -> pd.DataFrame:
    if indicator.startswith("SMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_sma(df, period)
    elif indicator.startswith("EMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_ema(df, period)
    elif indicator.startswith("WMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_wma(df, period)
    elif indicator.startswith("DEMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_dema(df, period)
    elif indicator.startswith("TEMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_tema(df, period)
    elif indicator.startswith("KAMA_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_kama(df, period)
    elif indicator.startswith("ATR_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_atr(df, period)
    elif indicator.startswith("ADX_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_adx(df, period)
    elif indicator.startswith("CCI_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_cci(df, period)
    elif indicator.startswith("ROC_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_roc(df, period)
    elif indicator.startswith("MOM_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        df[indicator] = _add_mom(df, period)
    elif indicator.startswith("BBANDS_"):
        period = int(indicator.split("_", maxsplit=1)[1])
        bbands_df = _add_bbands(df, period)
        for col in bbands_df.columns:
            df[col] = bbands_df[col]
    elif indicator == "RSI":
        df["RSI"] = _add_rsi(df)
    elif indicator == "MACD":
        macd_df = _add_macd(df)
        for col in macd_df.columns:
            df[col] = macd_df[col]
    elif indicator == "OBV":
        df["OBV"] = _add_obv(df)
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
