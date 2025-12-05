from scipy import stats
import importlib

# Import the module in the same folder called "4_pandas_example.py"
pandas_example = importlib.import_module("4_pandas_example")

# Load Close prices as pandas Series
stock_prices = pandas_example.load_stock_prices("AAPL")["Close"]
index_prices = pandas_example.load_stock_prices("^DJI")["Close"]

# Calculate returns and drop NaNs
stock_returns = stock_prices.pct_change().dropna()
index_returns = index_prices.pct_change().dropna()

# Two-sample T-Test to check if the difference in means is significant
t_stat, p_value = stats.ttest_ind(stock_returns, index_returns)

# Output results
print("T-Statistic:", t_stat)
print("P-Value:", p_value)
