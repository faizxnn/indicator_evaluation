import datetime as dt
import pandas as pd
from util import get_data

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    """
    Generates trades for the Theoretically Optimal Strategy.

    :param symbol: Stock symbol (default: JPM).
    :param sd: Start date.
    :param ed: End date.
    :param sv: Starting value of the portfolio.
    :return: DataFrame of trades.
    """
    # get stock prices
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[[symbol]]  # keep only JPM prices

    # initialize trades DataFrame
    trades = pd.DataFrame(0, index=prices.index, columns=[symbol])  # changed to use symbol as column name

    # generate trades based on future knowledge
    for i in range(1, len(prices)):
        current_price = prices[symbol].iloc[i]
        prev_price = prices[symbol].iloc[i - 1]
        
        if current_price > prev_price:  # price will go up
            trades.iloc[i] = 1000  # buy
        elif current_price < prev_price:  # price will go down
            trades.iloc[i] = -1000  # sell

    return trades

def author():
    return "fhussain45" 