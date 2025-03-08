import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import TheoreticallyOptimalStrategy as tos
import indicators as ind
import marketsimcode as msim
from util import get_data, plot_data

def main():
    # Define date range and starting value
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    sv = 100000
    
    # Get price data
    prices = get_data([symbol], pd.date_range(start_date, end_date))
    prices = prices[symbol]
    
    # Run theoretically optimal strategy
    trades_tos = tos.testPolicy(symbol=symbol, sd=start_date, ed=end_date, sv=sv)
    portvals_tos = msim.compute_portvals(trades_tos, start_val=sv)
    
    # Create benchmark - buy and hold 1000 shares
    benchmark_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])
    benchmark_trades.loc[prices.index[0], symbol] = 1000  # Buy 1000 shares on the first day only

    # Compute portfolio values
    portvals = msim.compute_portvals(trades_tos, start_val=sv)
    portvals_bench = msim.compute_portvals(benchmark_trades, start_val=sv)

    # Normalize both portfolio values to start at 1.0
    portvals_norm = portvals / portvals.iloc[0]
    portvals_bench_norm = portvals_bench / portvals_bench.iloc[0]

    # Plot normalized portfolio values
    plt.figure(figsize=(10, 6))
    plt.plot(portvals_norm, 'r-', label='Portfolio')
    plt.plot(portvals_bench_norm, 'g-', label='Benchmark')
    plt.title(f'Daily Portfolio Performance vs Benchmark ({symbol})')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.grid()
    plt.legend()
    plt.savefig('comparison.png')
    plt.close()
    
    # Calculate statistics
    tos_cr = (portvals_tos.iloc[-1] / portvals_tos.iloc[0]) - 1
    bench_cr = (portvals_bench.iloc[-1] / portvals_bench.iloc[0]) - 1
    
    tos_daily_returns = portvals_tos.pct_change().dropna()
    bench_daily_returns = portvals_bench.pct_change().dropna()
    
    tos_adr = tos_daily_returns.mean()
    bench_adr = bench_daily_returns.mean()
    
    tos_sddr = tos_daily_returns.std()
    bench_sddr = bench_daily_returns.std()
    
    # Print statistics
    print(f"Theoretically Optimal Strategy:")
    print(f"Cumulative Return: {tos_cr[0]:.6f}")
    print(f"Average Daily Return: {tos_adr[0]:.6f}")
    print(f"Standard Deviation of Daily Returns: {tos_sddr[0]:.6f}")
    
    print(f"\nBenchmark:")
    print(f"Cumulative Return: {bench_cr[0]:.6f}")
    print(f"Average Daily Return: {bench_adr[0]:.6f}")
    print(f"Standard Deviation of Daily Returns: {bench_sddr[0]:.6f}")
    
    # Generate and plot indicators
    # SMA
    sma = ind.SMA(prices, window=20)
    price_sma_ratio = prices / sma
    
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(prices, label='Price', color='blue')
    plt.plot(sma, label='SMA', color='orange')
    plt.title('SMA Indicator')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(price_sma_ratio, label='Price/SMA', color='green')
    plt.axhline(y=1, color='r', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price/SMA')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('sma.png')
    plt.close()

    # Bollinger Bands
    bb = ind.BollingerBands(prices, window=20)
    
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(prices, label='Price', color='blue')
    plt.plot(bb['Upper Band'], label='Upper Band', color='green')
    plt.plot(bb['Lower Band'], label='Lower Band', color='red')
    plt.title('Bollinger Bands')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(bb['%B'], label='%B', color='purple')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.axhline(y=1, color='r', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('%B')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('bollinger_bands.png')
    plt.close()

    # RSI
    rsi = ind.RSI(prices, window=14)
    
    plt.figure(figsize=(10, 6))
    plt.plot(rsi, label='RSI', color='purple')
    plt.axhline(y=70, color='r', linestyle='--')
    plt.axhline(y=30, color='g', linestyle='--')
    plt.title('RSI Indicator')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid()
    plt.savefig('rsi.png')
    plt.close()

    # Momentum
    momentum = ind.Momentum(prices, window=14)
    
    plt.figure(figsize=(10, 6))
    plt.plot(momentum, label='Momentum', color='blue')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Momentum Indicator')
    plt.xlabel('Date')
    plt.ylabel('Momentum')
    plt.legend()
    plt.grid()
    plt.savefig('momentum.png')
    plt.close()

    # MACD
    macd = ind.MACD(prices)
    
    plt.figure(figsize=(10, 6))
    plt.plot(macd['MACD'], label='MACD', color='blue')
    plt.plot(macd['Signal'], label='Signal', color='red')
    plt.title('MACD Indicator')
    plt.xlabel('Date')
    plt.ylabel('MACD')
    plt.legend()
    plt.grid()
    plt.savefig('macd.png')
    plt.close()

if __name__ == "__main__":
    main()

