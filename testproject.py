import datetime as dt
import pandas as pd
import TheoreticallyOptimalStrategy as tos
import indicators as ind
import marketsimcode as msim
from util import get_data, plot_data

def main():
    # run theoretically optimal strategy
    trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    portvals = msim.compute_portvals(trades)


    plot_data(portvals, title="Theoretically Optimal Strategy vs Benchmark", xlabel="Date", ylabel="Portfolio Value")

    # run and plot indicators
    prices = get_data(['JPM'], pd.date_range(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31)))
    prices = prices['JPM'] 

    # SMA
    sma = ind.SMA(prices, window=20)
    plot_data(pd.DataFrame({'Price': prices, 'SMA': sma}), title="SMA Indicator", xlabel="Date", ylabel="Price")

    # Bollinger Bands
    bb = ind.BollingerBands(prices, window=20)
    plot_data(pd.DataFrame({'Price': prices, 'Upper Band': bb['Upper Band'], 'Lower Band': bb['Lower Band']}),
              title="Bollinger Bands", xlabel="Date", ylabel="Price")

    # RSI
    rsi = ind.RSI(prices, window=14)
    plot_data(pd.DataFrame({'RSI': rsi}), title="RSI Indicator", xlabel="Date", ylabel="RSI")

    # momentum
    momentum = ind.Momentum(prices, window=14)
    plot_data(pd.DataFrame({'Momentum': momentum}), title="Momentum Indicator", xlabel="Date", ylabel="Momentum")

    # MACD
    macd = ind.MACD(prices)
    plot_data(pd.DataFrame({'MACD': macd['MACD'], 'Signal': macd['Signal']}),
              title="MACD Indicator", xlabel="Date", ylabel="MACD")

if __name__ == "__main__":
    main()