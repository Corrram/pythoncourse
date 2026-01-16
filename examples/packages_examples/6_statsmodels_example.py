import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import importlib

# Import the module in the same folder called "4_pandas_example.py"
pandas_example = importlib.import_module("4_pandas_example")

# Load your data (replace these lines with your actual data loading code)
stock_returns = pandas_example.load_stock_prices("AAPL")["Close"].pct_change().dropna()
market_returns = pandas_example.load_stock_prices("^DJI")["Close"].pct_change().dropna()

# Aligning the data
aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
aligned_data.columns = ["Stock_Returns", "Market_Returns"]

# Linear regression
X = sm.add_constant(
    aligned_data["Market_Returns"]
)  # Adds a constant term to the predictor
model = sm.OLS(aligned_data["Stock_Returns"], X)
results = model.fit()

# Output the results
print(results.summary())

# visualize the plot
plt.scatter(aligned_data["Market_Returns"], aligned_data["Stock_Returns"])
plt.plot(aligned_data["Market_Returns"], results.fittedvalues)
plt.xlabel("Market Returns")
plt.ylabel("Stock Returns")
plt.show()
