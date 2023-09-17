#!/usr/bin/env python
# coding: utf-8

import os
import requests
import json
import pandas as pd
import datetime as dt
import talib
import config

spot_api_url = "https://api.binance.com"
endpoint_klines = "/api/v3/klines"
endpoint_ticker_price = "/api/v3/ticker/price"

api_key = config.api_key
secret_key = config.secret_key
token_line = config.token_line

symbol_1 = str(config.ticker_symbol_1)
symbol_2 = str(config.ticker_symbol_2)
trading_symbol = symbol_1 + symbol_2
tf = config.time_frame

def line_notify(msg, token):
    url_line_noti = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url_line_noti, headers=headers, data = {'message': msg})
    print(r.text)

def get_candlestick(symbol, interval = '4h'):   
    try:
        url = f'{spot_api_url}{endpoint_klines}?symbol={symbol}&interval={interval}'
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = ['open_time',
                     'open', 'high', 'low', 'close', 'volume',
                     'close_time', 'qav', 'num_trades',
                     'taker_base_vol', 'taker_quote_vol', 'ignore']
        # df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
        # df.drop(columns=['open_time', 'v', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 
                         # 'taker_quote_vol', 'ignore'], inplace = True)
        df = df.apply(pd.to_numeric, errors='coerce')
        df.open_time = [dt.datetime.fromtimestamp(x/1000.0) for x in df.open_time]
        df.close_time = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
        df["ohlc4"] = df[["open", "high", "low", "close"]].mean(axis=1)
        
        return df

    except Exception as e:
        print(e)

def indicator_cdc(df):
    src = df['ohlc4']
    fast_ema = 12
    slow_ema = 26
    lst_trend = []
    lst_trigger = []
    trigger = 0 

    try:
        df['avg_src'] = talib.EMA(src,2)
        df['fast_ema'] = talib.EMA(df['avg_src'], fast_ema)
        df['slow_ema'] = talib.EMA(df['avg_src'], slow_ema)
        df.dropna(subset = ['avg_src','fast_ema','slow_ema'], inplace=True)
        df = df.reset_index()
        for index, row in df.iterrows():
            if row['fast_ema'] > row['slow_ema']:
                lst_trend.append('bullish')
                
            elif row['fast_ema'] < row['slow_ema']: 
                lst_trend.append('bearish')
                
        df['trend'] = lst_trend
##        print(df.tail())
        return df

    except Exception as e:
        print(e)

df_price = get_candlestick(trading_symbol,tf)
df_price = indicator_cdc(df_price)
flg_create_order = 0 # 1 for Buy, -1 for Sell

for i in range(df_price.shape[0]-2, df_price.shape[0]-1, 1):
    if df_price['trend'][i-1] != df_price['trend'][i]:
        if df_price['trend'][i] == "bullish":
            flg_create_order = 1
            print(f'{df_price["close_time"][i]} "BUY" {flg_create_order}')
            
        elif df_price['trend'][i] == "bearish":
            flg_create_order = -1
            print(f'{df_price["close_time"][i]} "SELL" {flg_create_order}')
            
    else:
        print(f'{df_price["close_time"][i]} "Signal not found"')

from binance.client import Client
client = Client(api_key,secret_key)

bal_1 = float(client.get_asset_balance(asset=symbol_1)['free'])
bal_2 = float(client.get_asset_balance(asset=symbol_2)['free'])

last_price = float(json.loads(requests.get(f'{spot_api_url}{endpoint_ticker_price}?symbol={trading_symbol}').text)['price'])
trading_qty = round(bal_2/last_price, 2)

from binance.enums import *
##flg_create_order = 0
##bal_1 = 0.1
if flg_create_order != 0:
    if flg_create_order == 1:
##        order = client.create_order(
##        symbol=trading_symbol,
##        side=SIDE_BUY,
##        type=ORDER_TYPE_MARKET,
##        quantity=trading_qty)
        line_notify(f'"BUY"', token_line)
##        print(order)
    elif flg_create_order == -1:
##        order = client.create_order(
##        symbol=trading_symbol,
##        side=SIDE_SELL,
##        type=ORDER_TYPE_MARKET,
##        quantity=bal_1)
        line_notify(f'"SELL"', token_line)
##        print(order)
else:
    line_notify("Signal not found", token_line)
    print("Signal not found")

