import numpy as np
from matplotlib import pyplot as plt


def print_mean_and_variance(**kwargs):
    for k, v in kwargs.items():
        variance = v.var()
        mean = v.mean()
        print(f"{k} variance: {variance}")
        print(f"{k} mean: {mean}")


def plot_prices(**kwargs):
    for k, v in kwargs.items():
        plt.plot(v, label=k)
    plt.legend()
    plt.grid()
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()
    plt.close()


def load_stock_values(company):
    filepath = f"data/{company}.csv"
    # FIX: skip 3 header rows, use Close column (index 1)
    return np.loadtxt(filepath, delimiter=",", skiprows=3, usecols=1)


if __name__ == "__main__":
    stock1 = "APA"
    stock2 = "CLX"
    values1 = load_stock_values(stock1)
    values2 = load_stock_values(stock2)

    # calculate correlation of daily returns
    returns1 = values1[1:] / values1[:-1] - 1
    returns2 = values2[1:] / values2[:-1] - 1
    correlation_matrix = np.corrcoef(returns1, returns2)
    correlation = correlation_matrix[0, 1]
    print(f"Correlation: {correlation}")

    print_mean_and_variance(**{stock1: values1, stock2: values2})

    # plot the prices
    plot_prices(**{stock1: values1, stock2: values2})

    # plot joint portfolio
    portfolio = (values1 + values2) / 2
    plot_prices(**{stock1: values1, stock2: values2, "Portfolio": portfolio})

    # calculate variance and mean of portfolio
    print_mean_and_variance(**{"Portfolio": portfolio})
    print("Done!")
