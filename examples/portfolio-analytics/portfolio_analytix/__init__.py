"""
econ_tools package

Provides basic tools for GDP and inflation calculations.
"""

__version__ = "0.1.0"
from portfolio_analytix.datafetch import DataFetcher
from portfolio_analytix.metrics import *
from portfolio_analytix.optimize import *

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
