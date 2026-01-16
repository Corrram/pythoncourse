import pathlib

import pandas as pd
import requests
import yfinance as yf


def fetch_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # 1) Get the page with a proper User-Agent
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()  # raises if 4xx/5xx

    # 2) Let pandas parse tables from the HTML text
    tables = pd.read_html(resp.text)
    # On this page, the *first* table is the S&P 500 constituents
    df = tables[0]

    # 3) Extract the "Symbol" column
    tickers = df["Symbol"].tolist()

    # 4) Save to file
    with open("sp500-ticker-list.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(tickers))

    return tickers


def download_stock_data(tickers=None):
    match tickers:
        case None:
            with open("sp500-ticker-list.txt") as f:
                stock_list = f.read().splitlines()
        case str():
            stock_list = [tickers]
        case list():
            stock_list = tickers
        case _:
            raise ValueError("tickers must be None, a string or a list of strings")
    pathlib.Path("data").mkdir(exist_ok=True)
    for stock in ["^DJI"] + stock_list:
        data = yf.download(stock, start="2010-01-01")
        data.to_csv(f"data/{stock}.csv")


if __name__ == "__main__":
    sp500_tickers = fetch_sp500_tickers()
    download_stock_data("SPYI")
    download_stock_data()
    print("Done!")
