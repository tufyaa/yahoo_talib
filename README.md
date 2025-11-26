# Yahoo Finance TA-Lib Pipeline

A simple Python project that downloads historical OHLCV data from Yahoo Finance, stores it in a single CSV for multiple tickers, and computes selected TA-Lib indicators. The pipeline is designed to be readable and split across small, focused modules.

## Project Structure
```
project_root/
  README.md
  requirements.txt
  data/
    .gitkeep
  src/
    yahoo_talib_pipeline/
      __init__.py
      config.py
      data_loader.py
      indicators.py
      pipeline.py
      cli.py
      main.py
  tests/
    test_data_loader.py
    test_indicators.py
    test_pipeline.py
```

- **config.py**: Shared configuration with data paths.
- **data_loader.py**: Functions to download OHLCV data and save to CSV.
- **indicators.py**: TA-Lib indicator calculations (15 indicators supported).
- **pipeline.py**: End-to-end orchestration of download and indicator computation.
- **cli.py**: Command-line argument parsing.
- **main.py**: Entry point that executes the full pipeline.
- **tests/**: Three basic pytest tests.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
Run the full pipeline via the CLI:

Single ticker example:
```bash
python -m yahoo_talib_pipeline.main --tickers AAPL --start 2023-01-01 --end 2023-01-31 --indicators RSI,SMA_20
```

Multiple tickers:
```bash
python -m yahoo_talib_pipeline.main --tickers AAPL,MSFT,GOOG --start 2023-01-01 --end 2023-01-31 --indicators RSI,MACD,ATR_14
```

Custom interval and indicators:
```bash
python -m yahoo_talib_pipeline.main --tickers TSLA,NVDA --start 2023-01-01 --end 2023-02-01 --interval 1h --indicators RSI,SMA_10,EMA_50,BBANDS_20
```

The pipeline will produce `data/prices.csv` and `data/prices_with_indicators.csv`.

## Supported Indicators

All indicator names are passed via `--indicators` as comma-separated tokens. Period-based indicators use the suffix `_N` to denote the timeperiod. The project currently supports 15 TA-Lib indicators:

- SMA_`N`
- EMA_`N`
- WMA_`N`
- DEMA_`N`
- TEMA_`N`
- KAMA_`N`
- ATR_`N`
- ADX_`N`
- CCI_`N`
- ROC_`N`
- MOM_`N`
- BBANDS_`N`
- RSI
- MACD
- OBV

## Tests
Run all tests with:
```bash
pytest
```
