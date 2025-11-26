"""Orchestration for the Yahoo Finance to TA-Lib pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from . import config
from .data_loader import download_ohlcv, save_to_csv
from .indicators import compute_indicators


def run_pipeline(
    tickers: Iterable[str] | str,
    start: str | None,
    end: str | None,
    interval: str,
    indicators: Iterable[str] | None,
    data_dir: Path | None = None,
) -> None:
    """Run the complete pipeline: download, save, compute indicators, save again."""

    target_dir = data_dir or config.DATA_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    prices_path = target_dir / config.PRICES_CSV.name
    prices_with_ind_path = target_dir / config.PRICES_WITH_INDICATORS_CSV.name

    prices_df = download_ohlcv(tickers, start=start, end=end, interval=interval)
    save_to_csv(prices_df, prices_path)

    indicators = list(indicators or [])
    enriched_df = compute_indicators(prices_df, indicators) if indicators else prices_df
    save_to_csv(enriched_df, prices_with_ind_path)
