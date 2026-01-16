import pytest
import pandas as pd
import yfinance as yf
from portfolio_analytix.datafetch import DataFetcher


## --- Mocking Fixture ---

@pytest.fixture
def mock_yfinance(monkeypatch):
    """
    Intercepts yfinance.download and returns a static MultiIndex DataFrame
    consistent with yfinance's structure.
    """

    def mocked_download(tickers, *args, **kwargs):
        # yfinance returns a MultiIndex (Price, Ticker) when multiple tickers are fetched
        # or a single Index when 'Close' is selected.
        # Here we simulate the MultiIndex structure yf.download usually provides.
        data = {
            ("Close", "AAPL"): [150.0, 151.0],
            ("Close", "MSFT"): [250.0, 252.0]
        }
        df = pd.DataFrame(data, index=pd.to_datetime(["2023-01-10", "2023-01-11"]))
        df.index.name = "Date"
        return df

    monkeypatch.setattr(yf, "download", mocked_download)


@pytest.fixture
def fetcher():
    """Returns a DataFetcher instance."""
    return DataFetcher(tickers=["AAPL", "MSFT"], start="2023-01-10", end="2023-01-11")


def test_datafetch_mocked_values(mock_yfinance, fetcher):
    """
    Verify that the fetcher correctly processes the mocked yfinance data.
    """
    df = fetcher.fetch_data()

    # Check shape and columns
    assert df.shape == (2, 2)
    assert set(df.columns) == {"AAPL", "MSFT"}

    # Verify specific mocked values to ensure the 'Close' slice worked
    assert df.loc["2023-01-10", "AAPL"] == 150.0
    assert df.loc["2023-01-11", "MSFT"] == 252.0


def test_datafetch_internal_state(mock_yfinance, fetcher):
    """
    Ensure get_data() updates correctly using mocked data.
    """
    assert fetcher.get_data() is None
    fetcher.fetch_data()
    assert fetcher.get_data() is not None
    assert "AAPL" in fetcher.get_data().columns