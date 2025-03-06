import pandas as pd
import numpy as np
from util import get_data

def SMA(prices, window=20):
    """
    Calculates the Simple Moving Average (SMA).

    :param prices: DataFrame of stock prices.
    :param window: Window size for SMA.
    :return: SMA values as a Pandas Series.
    """
    return prices.rolling(window=window).mean()

def BollingerBands(prices, window=20):
    """
    Calculates Bollinger Bands.

    :param prices: DataFrame of stock prices.
    :param window: Window size for Bollinger Bands.
    :return: DataFrame with Upper Band, Lower Band, and %B.
    """
    sma = SMA(prices, window)
    std = prices.rolling(window=window).std()
    upper_band = sma + (2 * std)
    lower_band = sma - (2 * std)
    bb_percent = (prices - lower_band) / (upper_band - lower_band)
    return pd.DataFrame({'Upper Band': upper_band, 'Lower Band': lower_band, '%B': bb_percent})

def RSI(prices, window=14):
    """
    Calculates the Relative Strength Index (RSI).

    :param prices: DataFrame of stock prices.
    :param window: Window size for RSI.
    :return: RSI values as a Pandas Series.
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def Momentum(prices, window=14):
    """
    Calculates Momentum.

    :param prices: DataFrame of stock prices.
    :param window: Window size for Momentum.
    :return: Momentum values as a Pandas Series.
    """
    return prices / prices.shift(window) - 1

def MACD(prices, short_window=12, long_window=26, signal_window=9):
    """
    Calculates the Moving Average Convergence Divergence (MACD).

    :param prices: DataFrame of stock prices.
    :param short_window: Short window for MACD.
    :param long_window: Long window for MACD.
    :param signal_window: Signal window for MACD.
    :return: DataFrame with MACD and Signal Line.
    """
    short_ema = prices.ewm(span=short_window, adjust=False).mean()
    long_ema = prices.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return pd.DataFrame({'MACD': macd, 'Signal': signal})

def author():
    return "fhussain45" 