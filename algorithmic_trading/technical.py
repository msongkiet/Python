import requests
import json
import pandas as pd
import datetime as dt
import talib
import yfinance as yf

def getEma(df, fastPeriod, slowPeriod):
    src = df['ohlc4']
    fastEma = fastPeriod
    slowEma = slowPeriod
    trend_list = []
    zone_list = []

    try:
        df['avg_src'] = talib.EMA(src,2)
        df['fast_ema'] = talib.EMA(df['avg_src'], fastEma)
        df['slow_ema'] = talib.EMA(df['avg_src'], slowEma)
        df.dropna(subset = ['avg_src','fast_ema','slow_ema'], inplace=True)

        for i in range(df.shape[0]):
            if df['fast_ema'][i] > df['slow_ema'][i]:
                trend_list.append('bullish')
                if df['avg_src'][i] > df['fast_ema'][i]:
                    zone_list.append('green')
                elif df['avg_src'][i] < df['fast_ema'][i]:
                    zone_list.append('yellow')
            elif df['fast_ema'][i] < df['slow_ema'][i]: 
                trend_list.append('bearish')
                if df['avg_src'][i] > df['fast_ema'][i]:
                    zone_list.append('blue')
                elif df['avg_src'][i] < df['fast_ema'][i]:
                    zone_list.append('red')

        df['trend'] = trend_list
        df['zone'] = zone_list

        return df

    except Exception as e:
        print(e)


def emaCrossScan(df, backtest_preriod = 1):
    try:
        message = ''

        if df.shape[0] > backtest_preriod:
            for i in range(df.shape[0]-backtest_preriod, df.shape[0], 1):
                if df['trend'][i-1] != df['trend'][i]:
                    message = df['trend'][i]

                if df['zone'][i] == 'blue' or df['zone'][i] == 'yellow':
                    message = df['zone'][i]

        return message

    except Exception as e:
        print(e)

def getVol(df):
    src = df['Volume']
    sma = 5
    try:
        df['vol_ma'] = talib.SMA(src,sma)
        df.dropna(subset = ['vol_ma'], inplace=True)
        # df['x of vol_ma'] = (df['Volume']-df['vol_ma'])/df['vol_ma']
        df['x_of_vol_ma'] = (df['Volume']/df['vol_ma']).round(2)
        return df

    except Exception as e:
        print(e)

# def cdc_indi(df):
#     src = df['ohlc4']
#     fast_ema = 12
#     slow_ema = 26
#     trend_list = []
#     zone_list = []

#     try:
#         df['avg_src'] = talib.EMA(src,2)
#         df['fast_ema'] = talib.EMA(df['avg_src'], fast_ema)
#         df['slow_ema'] = talib.EMA(df['avg_src'], slow_ema)
#         df.dropna(subset = ['avg_src','fast_ema','slow_ema'], inplace=True)

#         for i in range(df.shape[0]):
#             if df['fast_ema'][i] > df['slow_ema'][i]:
#                 trend_list.append('bullish')
#                 if df['avg_src'][i] > df['fast_ema'][i]:
#                     zone_list.append('green')
#                 elif df['avg_src'][i] < df['fast_ema'][i]:
#                     zone_list.append('yellow')
#             elif df['fast_ema'][i] < df['slow_ema'][i]: 
#                 trend_list.append('bearish')
#                 if df['avg_src'][i] > df['fast_ema'][i]:
#                     zone_list.append('blue')
#                 elif df['avg_src'][i] < df['fast_ema'][i]:
#                     zone_list.append('red')

#         df['trend'] = trend_list
#         df['zone'] = zone_list

#         return df

#     except Exception as e:
#         print(e)


