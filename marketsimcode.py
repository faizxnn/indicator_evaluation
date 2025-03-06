import datetime as dt
import pandas as pd
from util import get_data

def compute_portvals(trades_df, start_val=100000, commission=0.0, impact=0.0):
    
    symbol = 'JPM'

    # get start and end dates from the trades DataFrame
    start_date = trades_df.index.min()
    end_date = trades_df.index.max()

    
    prices = get_data([symbol], pd.date_range(start_date, end_date))
    prices = prices[[symbol]]  # keep only JPM prices


    holdings = pd.DataFrame(0.0, index=prices.index, columns=[symbol, 'Cash'])
    holdings['Cash'] = start_val  # initialize cash

    # process trades
    for date, trade in trades_df.iterrows():
        shares = trade[0] 
        price = prices.loc[date, symbol]

        # update holdings based on trade
        if shares > 0:  # buy
            cost = shares * price * (1 + impact)
            holdings.loc[date, symbol] += shares
            holdings.loc[date, 'Cash'] -= cost
        elif shares < 0:  # sell
            cost = shares * price * (1 - impact)
            holdings.loc[date, symbol] += shares
            holdings.loc[date, 'Cash'] -= cost

        
        holdings.loc[date, 'Cash'] -= commission

    # calculate cumulative holdings
    holdings = holdings.cumsum()

    # calculate portfolio value
    portvals = (prices[symbol] * holdings[symbol]) + holdings['Cash']
    portvals = pd.DataFrame(portvals, columns=['Portfolio Value'])

    return portvals

def author():
    return "fhussain45"