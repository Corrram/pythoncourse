import pandas as pd
import pathlib
import yfinance
from matplotlib import pyplot as plt
import glob


def fetch_stock_name(ticker):
    return yfinance.Ticker(ticker).info["longName"]


def load_stock_prices(company=None):
    def load_single_stock(filepath):
        # Read raw CSV
        df = pd.read_csv(filepath)

        # Drop the two non-data rows: "Ticker,..." and "Date,,,,,"
        df = df.drop(index=[0, 1])

        # "Price" column actually contains the dates; rename it
        df = df.rename(columns={"Price": "Date"})

        # Parse dates and set as index
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")

        # Convert all remaining columns to float
        df = df.astype(float)

        return df

    if isinstance(company, str):
        filepath = f"data/{company}.csv"
        return load_single_stock(filepath)
    elif isinstance(company, list):
        return {stock: load_single_stock(f"data/{stock}.csv") for stock in company}
    else:  # when company is None
        stock_files = glob.glob("data/*.csv")
        return {
            pathlib.Path(stock_file).stem: load_single_stock(stock_file)
            for stock_file in stock_files
        }


def plot_prices(*stocks):
    for stock in stocks:
        plt.plot(stock, label=fetch_stock_name(stock))
    plt.legend()
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()
    plt.close()


def compute_beta(stock_returns, index_returns):
    covariance = stock_returns.cov(index_returns)
    variance = index_returns.var()
    return covariance / variance


if __name__ == "__main__":
    stock_prices = load_stock_prices()
    # drop empty stocks
    stock_prices = {name: data for name, data in stock_prices.items() if not data.empty}

    index_prices = load_stock_prices("^DJI")
    index_returns = index_prices["Close"].pct_change()

    stock_returns = {
        name: data["Close"].pct_change() for name, data in stock_prices.items()
    }

    betas = {
        stock: compute_beta(stock_returns[stock], index_returns)
        for stock in stock_returns
    }

    # get stock with highest beta
    highest_beta = max(betas, key=betas.get)
    print(f"Stock with highest beta: {fetch_stock_name(highest_beta)} ({highest_beta})")
