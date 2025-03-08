import datetime as dt
import pandas as pd
import numpy as np
from util import get_data

def compute_portvals(trades_df, start_val=100000, commission=9.95, impact=0.005):
    # get symbol from trades
    symbol = trades_df.columns[0]
    
    # get date range
    start_date = trades_df.index.min()
    end_date = trades_df.index.max()
    
    # get prices
    prices = get_data([symbol], pd.date_range(start_date, end_date))
    prices = prices[[symbol]]
    
    # track holdings
    holdings = pd.DataFrame(0.0, index=prices.index, columns=[symbol, 'Cash'])
    holdings['Cash'] = start_val
    
    # process trades
    for date, row in trades_df.iterrows():
        shares = row[symbol]
        if shares == 0:
            continue
            
        price = prices.loc[date, symbol]
        transaction_cost = abs(shares * price * impact) + commission
        
        holdings.loc[date:, symbol] += shares
        holdings.loc[date:, 'Cash'] -= (shares * price + transaction_cost)
    
    portvals = holdings[symbol] * prices[symbol] + holdings['Cash']
    
    return pd.DataFrame(portvals, columns=['Portfolio Value'])

def author():
    return "fhussain45"