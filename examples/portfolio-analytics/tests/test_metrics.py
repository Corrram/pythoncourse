import pytest
import pandas as pd
import numpy as np
from portfolio_analytix.metrics import (
    daily_returns,
    mean_returns,
    cov_matrix,
    portfolio_performance,
    sharpe_ratio,
)

## --- Fixtures ---


@pytest.fixture
def sample_prices():
    """Simple price history for two assets."""
    return pd.DataFrame(
        {
            "A": [100.0, 101.0, 102.01],  # +1% daily
            "B": [50.0, 50.0, 50.0],  # 0% daily
        }
    )


@pytest.fixture
def sample_returns():
    """Known returns for deterministic math checks."""
    return pd.DataFrame({"A": [0.01, 0.02, 0.015], "B": [-0.005, 0.0, 0.005]})


@pytest.fixture
def portfolio_data():
    """Standardized mean returns and cov matrix for portfolio math."""
    mean_ret = pd.Series({"A": 0.1, "B": 0.05})
    # Diagonal matrix: Vol_A = sqrt(0.04)=0.2, Vol_B = sqrt(0.01)=0.1
    cov = pd.DataFrame({"A": [0.04, 0.00], "B": [0.00, 0.01]}, index=["A", "B"])
    return mean_ret, cov


## --- Tests ---


def test_daily_returns(sample_prices):
    rets = daily_returns(sample_prices)
    assert rets.shape == (2, 2)
    # Check A: (101-100)/100 = 0.01
    assert abs(rets.loc[1, "A"] - 0.01) < 1e-9
    # Check B: (50-50)/50 = 0.0
    assert rets.loc[1, "B"] == 0.0


def test_mean_returns(sample_returns):
    # Mean of A: (0.01 + 0.02 + 0.015) / 3 = 0.015
    # Annualized (factor 2): 0.015 * 2 = 0.03
    means = mean_returns(sample_returns, annualize_factor=2)
    assert abs(means["A"] - 0.03) < 1e-9


def test_cov_matrix(sample_returns):
    cv = cov_matrix(sample_returns, annualize_factor=252)
    assert cv.shape == (2, 2)
    assert cv.loc["A", "A"] > 0  # Variance must be positive


@pytest.mark.parametrize(
    "weights, expected_ret, expected_vol",
    [
        (np.array([1.0, 0.0]), 0.10, 0.20),  # 100% A -> Ret: 0.1, Vol: sqrt(0.04)
        (np.array([0.0, 1.0]), 0.05, 0.10),  # 100% B -> Ret: 0.05, Vol: sqrt(0.01)
        (
            np.array([0.5, 0.5]),
            0.075,
            0.111803398,
        ),  # 50/50 -> sqrt(0.5^2*0.04 + 0.5^2*0.01)
    ],
)
def test_portfolio_performance_parameterized(
    portfolio_data, weights, expected_ret, expected_vol
):
    mean_ret, cov = portfolio_data
    port_ret, port_vol = portfolio_performance(weights, mean_ret, cov)

    assert abs(port_ret - expected_ret) < 1e-8
    assert abs(port_vol - expected_vol) < 1e-8


def test_sharpe_ratio():
    # (0.10 - 0.02) / 0.05 = 0.08 / 0.05 = 1.6
    sr = sharpe_ratio(port_ret=0.1, port_vol=0.05, risk_free_rate=0.02)
    assert abs(sr - 1.6) < 1e-9
