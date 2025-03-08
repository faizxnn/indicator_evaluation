import datetime as dt
import pandas as pd
import numpy as np
from util import get_data

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    # get stock prices
    prices = get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]  # just symbol prices

    # initialize trades dataframe
    trades = pd.DataFrame(0, index=prices.index, columns=[symbol])
    
    # calculate future returns
    future_returns = prices.shift(-1) / prices - 1
    
    # start with no position
    position = 0
    
    # process each day except last
    for i in range(len(prices) - 1):
        date = prices.index[i]
        future_return = future_returns.iloc[i]
        
        # set target based on future return
        target_position = 1000 if future_return > 0 else -1000
        
        # calculate needed trade
        trade = target_position - position
        
        # record trade
        trades.loc[date, symbol] = trade
        
        # update position
        position = target_position
    
    # close position on last day
    last_date = prices.index[-1]
    trades.loc[last_date, symbol] = -position
    
    return trades

def author():
    return "fhussain45" 

