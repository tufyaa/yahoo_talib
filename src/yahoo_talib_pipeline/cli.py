"""Command-line argument parsing."""
from __future__ import annotations

import argparse
from typing import Iterable


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Yahoo Finance to TA-Lib pipeline")
    parser.add_argument("--tickers", required=True, help="Comma-separated tickers, e.g., AAPL,MSFT")
    parser.add_argument("--start", required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--interval", default="1d", help="Data interval, default 1d")
    parser.add_argument("--indicators", required=True, help="Comma-separated list of indicators, e.g., RSI,SMA_20")
    return parser


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(args=args)


def parse_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]

