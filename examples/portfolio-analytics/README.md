# Portfolio Analytics – Advanced Edition

A Python package offering:

- **Financial data fetching** (via `yfinance`)
- **Computation of daily/annualized returns, covariance matrices, Sharpe ratios**
- **Mean-variance optimization** (Markowitz) for minimum variance and maximum Sharpe portfolios

Designed for **Finance/Economics Master** students looking to explore real-world portfolio analytics in Python.

---

## Features

1. **DataFetch** (`datafetch.py`):
   - Fetch daily price data for multiple tickers using `yfinance`.
   - Returns a `pandas.DataFrame` of adjusted close prices.

2. **Metrics** (`metrics.py`):
   - Compute daily returns, annualized mean returns, covariance matrices.
   - Evaluate portfolio performance (return/volatility) and Sharpe ratios.

3. **Optimize** (`optimize.py`):
   - Implement **Markowitz** mean-variance optimization.
   - Find **minimum-variance** portfolio (no short-selling).
   - Find **maximum Sharpe ratio** portfolio under risk-free rate.
