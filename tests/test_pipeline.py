import pandas as pd

from yahoo_talib_pipeline import config
from yahoo_talib_pipeline.pipeline import run_pipeline


def test_run_pipeline_creates_files(tmp_path, monkeypatch):
    def fake_download(tickers, start, end, interval):
        dates = pd.date_range("2023-01-01", periods=2, freq="D")
        frames = []
        for ticker in tickers:
            frames.append(
                pd.DataFrame(
                    {
                        "ticker": ticker,
                        "Date": dates,
                        "Open": [1, 2],
                        "High": [1, 2],
                        "Low": [1, 2],
                        "Close": [1.0, 2.0],
                        "Adj Close": [1.0, 2.0],
                        "Volume": [100, 200],
                    }
                )
            )
        return pd.concat(frames, ignore_index=True)

    monkeypatch.setattr("yahoo_talib_pipeline.pipeline.download_ohlcv", fake_download)
    monkeypatch.setattr("yahoo_talib_pipeline.pipeline.compute_indicators", lambda df, indicators: df.assign(dummy=1))

    run_pipeline(["AAA", "BBB"], start="2023-01-01", end="2023-01-03", interval="1d", indicators=["RSI"], data_dir=tmp_path)

    prices_path = tmp_path / config.PRICES_CSV.name
    enriched_path = tmp_path / config.PRICES_WITH_INDICATORS_CSV.name
    assert prices_path.exists()
    assert enriched_path.exists()


def test_run_pipeline_defaults_to_config_dir(tmp_path, monkeypatch):
    def fake_download(tickers, start, end, interval):
        dates = pd.date_range("2023-02-01", periods=1, freq="D")
        return pd.DataFrame(
            {
                "ticker": list(tickers)[0],
                "Date": dates,
                "Open": [1],
                "High": [1],
                "Low": [1],
                "Close": [1.0],
                "Adj Close": [1.0],
                "Volume": [10],
            }
        )

    monkeypatch.setattr(config, "DATA_DIR", tmp_path, raising=False)
    monkeypatch.setattr(config, "PRICES_CSV", tmp_path / "prices.csv", raising=False)
    monkeypatch.setattr(config, "PRICES_WITH_INDICATORS_CSV", tmp_path / "prices_with_indicators.csv", raising=False)
    monkeypatch.setattr("yahoo_talib_pipeline.pipeline.download_ohlcv", fake_download)
    monkeypatch.setattr("yahoo_talib_pipeline.pipeline.compute_indicators", lambda df, indicators: df)

    run_pipeline(["AAA"], start="2023-02-01", end="2023-02-02", interval="1d", indicators=["RSI"])

    assert (tmp_path / "prices.csv").exists()
    assert (tmp_path / "prices_with_indicators.csv").exists()


def test_run_pipeline_accepts_string_ticker_and_none_indicators(tmp_path, monkeypatch):
    def fake_download(tickers, start, end, interval):
        assert tickers == "AAA"
        return pd.DataFrame(
            {
                "ticker": ["AAA"],
                "Date": pd.date_range("2023-03-01", periods=1, freq="D"),
                "Open": [1],
                "High": [1],
                "Low": [1],
                "Close": [1.0],
                "Adj Close": [1.0],
                "Volume": [10],
            }
        )

    monkeypatch.setattr(config, "DATA_DIR", tmp_path, raising=False)
    monkeypatch.setattr(config, "PRICES_CSV", tmp_path / "prices.csv", raising=False)
    monkeypatch.setattr(config, "PRICES_WITH_INDICATORS_CSV", tmp_path / "prices_with_indicators.csv", raising=False)
    monkeypatch.setattr("yahoo_talib_pipeline.pipeline.download_ohlcv", fake_download)
    monkeypatch.setattr("yahoo_talib_pipeline.pipeline.compute_indicators", lambda df, indicators: df.assign(dummy=1))

    run_pipeline("AAA", start=None, end=None, interval="1d", indicators=None)

    assert (tmp_path / "prices.csv").exists()
    assert (tmp_path / "prices_with_indicators.csv").exists()
