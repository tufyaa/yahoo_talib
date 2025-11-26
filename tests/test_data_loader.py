import pandas as pd

from yahoo_talib_pipeline.data_loader import download_ohlcv


def test_download_returns_dataframe(monkeypatch):
    def fake_download(ticker, start, end, interval, progress):
        dates = pd.date_range("2023-01-01", periods=3, freq="D")
        return pd.DataFrame(
            {
                "Date": dates,
                "Open": [1, 2, 3],
                "High": [2, 3, 4],
                "Low": [0, 1, 2],
                "Close": [1.5, 2.5, 3.5],
                "Adj Close": [1.5, 2.5, 3.5],
                "Volume": [100, 110, 120],
            }
        ).set_index("Date")

    monkeypatch.setattr("yfinance.download", fake_download)

    df = download_ohlcv(["FAKE"], start="2023-01-01", end="2023-01-04", interval="1d")
    assert not df.empty
    assert set(df.columns) == {"ticker", "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"}
    assert df["ticker"].iloc[0] == "FAKE"
