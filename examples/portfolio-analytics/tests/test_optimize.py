"""
test_optimize.py

Tests for the optimize module, focusing on min_variance and max_sharpe.
"""

import pytest
import numpy as np
import pandas as pd
from portfolio_analytix.optimize import min_variance, max_sharpe


@pytest.mark.parametrize(
    "returns_dict, cov_matrix, expected_idx_greater",
    [
        # Original case: B has lower variance (0.02 vs 0.04)
        ({"A": 0.1, "B": 0.05}, [[0.04, 0.0], [0.0, 0.02]], 1),
        # Reverse case: A has lower variance (0.01 vs 0.05)
        ({"A": 0.1, "B": 0.1}, [[0.01, 0.0], [0.0, 0.05]], 0),
        # Equal variance: Weights should be 0.5 each
        ({"A": 0.08, "B": 0.08}, [[0.03, 0.0], [0.0, 0.03]], None),
        # High correlation: B is still safer
        ({"A": 0.1, "B": 0.05}, [[0.05, 0.04], [0.04, 0.05]], None),
    ],
)
def test_min_variance_parameterized(returns_dict, cov_matrix, expected_idx_greater):
    # Setup
    assets = list(returns_dict.keys())
    mean_ret = pd.Series(returns_dict)
    cov = pd.DataFrame(cov_matrix, index=assets, columns=assets)

    # Execution
    weights = min_variance(mean_ret, cov)

    # Assertions
    # 1. Weights must sum to 1 (Full investment constraint)
    assert abs(weights.sum() - 1.0) < 1e-7

    # 2. Weights should be positive (assuming no short-selling)
    assert (weights >= 0).all()

    # 3. Relative weight check
    if expected_idx_greater is not None:
        other_idx = 1 if expected_idx_greater == 0 else 0
        assert weights[expected_idx_greater] > weights[other_idx]
    else:
        # For the equal variance case
        np.testing.assert_allclose(weights[0], weights[1], atol=1e-7)


def test_max_sharpe():
    mean_ret = pd.Series({"A": 0.1, "B": 0.05})
    cov = pd.DataFrame({"A": [0.04, 0.00], "B": [0.00, 0.02]}, index=["A", "B"])

    weights = max_sharpe(mean_ret, cov, risk_free_rate=0.02)
    assert abs(weights.sum() - 1.0) < 1e-7
    # A has higher return, so we expect more weight on A
    assert weights[0] > weights[1]


def test_max_sharpe_zero_vol():
    # If an asset has zero variance, it might dominate
    mean_ret = pd.Series({"A": 0.08, "B": 0.06})
    cov = pd.DataFrame({"A": [0.0, 0.0], "B": [0.0, 0.0]}, index=["A", "B"])
    weights = max_sharpe(mean_ret, cov, risk_free_rate=0.02)
    # The solution might put everything in the zero-vol asset with best ratio
    assert abs(weights.sum() - 1.0) < 1e-7
