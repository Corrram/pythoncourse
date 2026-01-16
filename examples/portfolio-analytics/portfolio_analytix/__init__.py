"""
econ_tools package

Provides basic tools for GDP and inflation calculations.
"""

__version__ = "0.1.0"
from portfolio_analytix.datafetch import DataFetcher
from portfolio_analytix.metrics import daily_returns, mean_returns, cov_matrix
from portfolio_analytix.optimize import (
    min_variance,
    max_sharpe,
    portfolio_performance,
    sharpe_ratio,
)

__all__ = [
    "DataFetcher",
    "min_variance",
    "max_sharpe",
    "daily_returns",
    "mean_returns",
    "cov_matrix",
    "portfolio_performance",
    "sharpe_ratio",
]
