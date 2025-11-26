import pandas as pd

from yahoo_talib_pipeline.indicators import compute_indicators


def test_compute_indicators_adds_columns(monkeypatch):
    # Provide deterministic outputs for talib functions
    monkeypatch.setattr("talib.RSI", lambda close: pd.Series(range(len(close))))
    monkeypatch.setattr("talib.SMA", lambda close, timeperiod: pd.Series([timeperiod] * len(close)))
    monkeypatch.setattr("talib.EMA", lambda close, timeperiod: pd.Series([timeperiod + 1] * len(close)))
    monkeypatch.setattr("talib.WMA", lambda close, timeperiod: pd.Series([timeperiod + 2] * len(close)))
    monkeypatch.setattr("talib.DEMA", lambda close, timeperiod: pd.Series([timeperiod + 3] * len(close)))
    monkeypatch.setattr("talib.TEMA", lambda close, timeperiod: pd.Series([timeperiod + 4] * len(close)))
    monkeypatch.setattr("talib.KAMA", lambda close, timeperiod: pd.Series([timeperiod + 5] * len(close)))
    monkeypatch.setattr(
        "talib.MACD",
        lambda close: (
            pd.Series([1] * len(close)),
            pd.Series([2] * len(close)),
            pd.Series([3] * len(close)),
        ),
    )
    monkeypatch.setattr("talib.ATR", lambda high, low, close, timeperiod: pd.Series([4] * len(close)))
    monkeypatch.setattr("talib.ADX", lambda high, low, close, timeperiod: pd.Series([5] * len(close)))
    monkeypatch.setattr("talib.CCI", lambda high, low, close, timeperiod: pd.Series([6] * len(close)))
    monkeypatch.setattr("talib.ROC", lambda close, timeperiod: pd.Series([7] * len(close)))
    monkeypatch.setattr("talib.MOM", lambda close, timeperiod: pd.Series([8] * len(close)))
    monkeypatch.setattr("talib.OBV", lambda close, volume: pd.Series([9] * len(close)))
    monkeypatch.setattr(
        "talib.BBANDS",
        lambda close, timeperiod: (
            pd.Series([10] * len(close)),
            pd.Series([11] * len(close)),
            pd.Series([12] * len(close)),
        ),
    )

    df = pd.DataFrame(
        {
            "ticker": ["TST"] * 5,
            "Date": pd.date_range("2023-01-01", periods=5, freq="D"),
            "Open": [1, 2, 3, 4, 5],
            "High": [1, 2, 3, 4, 5],
            "Low": [1, 2, 3, 4, 5],
            "Close": [1.0, 2.0, 3.0, 4.0, 5.0],
            "Adj Close": [1.0, 2.0, 3.0, 4.0, 5.0],
            "Volume": [100, 200, 300, 400, 500],
        }
    )

    indicators = [
        "RSI",
        "SMA_2",
        "EMA_3",
        "WMA_4",
        "DEMA_5",
        "TEMA_6",
        "KAMA_7",
        "ATR_14",
        "ADX_14",
        "CCI_14",
        "ROC_10",
        "MOM_3",
        "OBV",
        "MACD",
        "BBANDS_20",
    ]

    result = compute_indicators(df, indicators)

    expected_columns = {
        "RSI",
        "SMA_2",
        "EMA_3",
        "WMA_4",
        "DEMA_5",
        "TEMA_6",
        "KAMA_7",
        "ATR_14",
        "ADX_14",
        "CCI_14",
        "ROC_10",
        "MOM_3",
        "OBV",
        "MACD",
        "MACD_signal",
        "MACD_hist",
        "BBANDS_upper_20",
        "BBANDS_middle_20",
        "BBANDS_lower_20",
    }

    assert expected_columns.issubset(set(result.columns))
    assert len(result) == len(df)


def test_compute_indicators_unsupported(monkeypatch):
    df = pd.DataFrame(
        {
            "ticker": ["TST"] * 3,
            "Date": pd.date_range("2023-01-01", periods=3, freq="D"),
            "Open": [1, 2, 3],
            "High": [1, 2, 3],
            "Low": [1, 2, 3],
            "Close": [1.0, 2.0, 3.0],
            "Adj Close": [1.0, 2.0, 3.0],
            "Volume": [100, 200, 300],
        }
    )

    # Minimal monkeypatching for required functions
    monkeypatch.setattr("talib.RSI", lambda close: pd.Series([0] * len(close)))

    try:
        compute_indicators(df, ["UNKNOWN"])
    except ValueError as exc:
        assert "Unsupported indicator" in str(exc)
    else:
        raise AssertionError("Unsupported indicator should raise ValueError")
