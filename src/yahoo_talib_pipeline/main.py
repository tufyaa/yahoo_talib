"""Entry point for running the full pipeline."""
from __future__ import annotations

from .cli import parse_args, parse_list
from .pipeline import run_pipeline


def main() -> None:
    args = parse_args()
    tickers = parse_list(args.tickers)
    indicators = parse_list(args.indicators)
    run_pipeline(
        tickers=tickers,
        start=args.start,
        end=args.end,
        interval=args.interval,
        indicators=indicators,
    )


if __name__ == "__main__":
    main()
