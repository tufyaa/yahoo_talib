"""Orchestration for the Yahoo Finance to TA-Lib pipeline."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from . import config
from .data_loader import download_ohlcv, save_to_csv
from .indicators import compute_indicators

logger = logging.getLogger(__name__)


def run_pipeline(
    tickers: Iterable[str] | str,
    start: str | None,
    end: str | None,
    interval: str,
    indicators: Iterable[str] | None,
    data_dir: Path | None = None,
) -> None:
    """Run the complete pipeline: download, save, compute indicators, save again."""

    indicators_list = list(indicators or [])
    logger.info(
        "run_pipeline start tickers=%s start=%s end=%s interval=%s indicators=%s data_dir=%s",
        tickers,
        start,
        end,
        interval,
        indicators_list,
        data_dir,
    )

    # Accept either Path or string for the output directory to be resilient to caller inputs
    target_dir = config.DATA_DIR if data_dir is None else Path(data_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    prices_path = target_dir / config.PRICES_CSV.name
    prices_with_ind_path = target_dir / config.PRICES_WITH_INDICATORS_CSV.name

    prices_df = download_ohlcv(tickers, start=start, end=end, interval=interval)
    save_to_csv(prices_df, prices_path)

    enriched_df = compute_indicators(prices_df, indicators_list) if indicators_list else prices_df
    save_to_csv(enriched_df, prices_with_ind_path)

    result = {
        "prices_path": str(prices_path),
        "prices_rows": len(prices_df.index),
        "enriched_path": str(prices_with_ind_path),
        "enriched_rows": len(enriched_df.index),
        "indicators": indicators_list,
    }
    logger.info(
        "run_pipeline finished rows_raw=%s rows_enriched=%s prices_path=%s enriched_path=%s",
        result["prices_rows"],
        result["enriched_rows"],
        prices_path,
        prices_with_ind_path,
    )
    return result
