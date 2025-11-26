import pandas as pd

from yahoo_talib_pipeline.indicators import compute_indicators


def test_compute_indicators_adds_columns(monkeypatch):
    # Provide deterministic outputs for talib functions
    monkeypatch.setattr("talib.RSI", lambda close: pd.Series([10, 20, 30]))
    monkeypatch.setattr("talib.SMA", lambda close, timeperiod: close.rolling(timeperiod).mean())

    df = pd.DataFrame(
        {
            "ticker": ["TST", "TST", "TST"],
            "Date": pd.date_range("2023-01-01", periods=3, freq="D"),
            "Open": [1, 2, 3],
            "High": [1, 2, 3],
            "Low": [1, 2, 3],
            "Close": [1.0, 2.0, 3.0],
            "Adj Close": [1.0, 2.0, 3.0],
            "Volume": [100, 200, 300],
        }
    )

    result = compute_indicators(df, ["RSI", "SMA_2"])
    assert "RSI" in result.columns
    assert "SMA_2" in result.columns
    assert len(result) == len(df)
