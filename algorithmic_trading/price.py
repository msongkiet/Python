import string
import requests
import json
import pandas as pd
import datetime as dt
import talib
import yfinance as yf

def getCryptoPrice(symbol, interval = '1d'):
    try:
        spotAPI = "https://api.binance.com"
        endpointKlines = "/api/v3/klines"
        url = f'{spotAPI}{endpointKlines}?symbol={symbol}&interval={interval}'
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = ['open_time',
                     'open', 'high', 'low', 'close', 'volume',
                     'close_time', 'qav', 'num_trades',
                     'taker_base_vol', 'taker_quote_vol', 'ignore']
        df = df.apply(pd.to_numeric, errors='coerce')
        df.open_time = [dt.datetime.fromtimestamp(x/1000.0) for x in df.open_time]
        df.close_time = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
        df["ohlc4"] = df[["open", "high", "low", "close"]].mean(axis=1)

        return df

    except Exception as e:
        print(e)

def getYfPrice(ticker, period = '3mo', interval = '1d'):
    """ Get stock historical data from Yahoo Finance

    Args : 
        - ticker : Stock qoute in https://finance.yahoo.com/
        - period : valid period --> 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max (optional is '3mo')
        - interval : valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo (optional, default is '1d')

    Return :
        - df : stock historical dataframe

    """
    try:
        df = yf.Ticker(ticker)
        df = df.history(period=period ,interval=interval)
        df = df.drop(columns=['Dividends', 'Stock Splits'])
        df['ticker'] = ticker.split(".")[0]
        df['ohlc4'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
        df = df.drop(columns=['Open', 'High', 'Low', 'Close'])
        print(f'{ticker} {df.shape}')
        return df
    except Exception as e:
        print(f'{e} {ticker} {df.shape}')