import requests
import json
import pandas as pd
import numpy as np
import datetime as dt
import talib as ta

def getCryptoPrice(symbol, interval = '4h'):    
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
        df = df[['close_time','open', 'high', 'low', 'close']]
        df["ohlc4"] = df[["open", "high", "low", "close"]].mean(axis=1)

        return df

    except Exception as e:
        print(e)

def lineNotify(msg, token):
    url_line_noti = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + token}
    r = requests.post(url_line_noti, headers=headers, data = {'message': msg})

def waveTunnel(df):
    wavyPeriod = 34
    df['wavy_h'] = ta.EMA(df.high, wavyPeriod)
    df['wavy_c'] = ta.EMA(df.close, wavyPeriod)
    df['wavy_l'] = ta.EMA(df.low, wavyPeriod)
    df['tunnel1'] = ta.EMA(df.close, 144)
    df['tunnel2'] = ta.EMA(df.close, 169)
    return df

def AOZ(df):
    medianPrice = (df.high + df.low)/2
    df['ao'] = ta.SMA(medianPrice, 5) - ta.SMA(medianPrice, 34)
    df['ac'] = df.ao - ta.SMA(df.ao, 5)
    df['atr'] = ta.ATR(df.high, df.low, df.close, timeperiod=14)

    # drop current bar (lastest row), focus only closed bar
    df = df[-300:-1].reset_index(drop=True)
    df['zone'] = np.nan
    df['greenZoneCount'] = np.nan
    df['redZoneCount'] = np.nan
    df['entryLevel'] = np.nan
    df['sl'] = np.nan
    df['tp1'] = np.nan
    df['tp2'] = np.nan
    sl = 1.5
    tp1 = 2
    tp2 = 3

    # zone 1 = green, 0 = gray, -1 = red
    for i in range(1, len(df)):
        entryLevel = 0
        slLevel = 0
        tp1Level = 0
        tp2Level = 0
        zone = 0
        greenZoneCount = 0
        redZoneCount = 0

        if (df.ao[i] > df.ao[i-1]) & (df.ac[i] > df.ac[i-1]):
            zone = 1
            greenZoneCount = df['greenZoneCount'][i-1] + 1
            # redZoneCount = 0
        elif (df.ao[i] < df.ao[i-1]) & (df.ac[i] < df.ac[i-1]):
            zone = -1
            # greenZoneCount = 0
            redZoneCount = df['redZoneCount'][i-1] + 1
        # else:
        #     df['zone'][i] = 0
        #     df['greenZoneCount'][i] = 0
        #     df['redZoneCount'][i] = 0
        
        df.loc[i,'zone'] = zone
        df.loc[i,'greenZoneCount'] = greenZoneCount
        df.loc[i,'redZoneCount'] = redZoneCount

        # BUY Condition
        if (df.ao[i] > 0) & (df.zone[i] == 1) & (df.greenZoneCount[i] < 5) & (df.close[i] > df.wavy_c[i]) & (df.wavy_l[i] > df.tunnel1[i]):
            if (df.zone[i-1] != df.zone[i]) | (df.ao[i-1] < 0):
                entryLevel = df.high[i]
            else:
                if (df['entryLevel'][i-1] != 0) & (df['entryLevel'][i-1] > max(df.high[i-1], df.high[i])):
                    entryLevel = df['entryLevel'][i-1]
                else:
                    entryLevel = max(df.high[i-1], df.high[i])
            
            slLevel = entryLevel - (sl * df['atr'][i])
            tp1Level = entryLevel + (tp1 * df['atr'][i])
            tp2Level = entryLevel + (tp2 * df['atr'][i])
        # SELL Condition
        elif (df.ao[i] < 0) & (df.zone[i] == -1) & (df.redZoneCount[i] < 5) & (df.close[i] < df.wavy_c[i]) & (df.wavy_h[i] < df.tunnel1[i]):
            if (df.zone[i-1] != df.zone[i]) | (df.ao[i-1] > 0):
                entryLevel = df.low[i]
            else:
                if (df['entryLevel'][i-1] != 0) & (df['entryLevel'][i-1] < min(df.low[i-1], df.low[i])):
                    entryLevel = df['entryLevel'][i-1]
                else:
                    entryLevel = min(df.low[i-1], df.low[i])

            slLevel = entryLevel + (sl * df['atr'][i])
            tp1Level = entryLevel - (tp1 * df['atr'][i])
            tp2Level = entryLevel - (tp2 * df['atr'][i])

        # assign entry, stop loss and take profit
        df.loc[i,'entryLevel'] = entryLevel
        df.loc[i,'sl'] = slLevel
        df.loc[i,'tp1'] = tp1Level
        df.loc[i,'tp2'] = tp2Level


    # df['zone'] = df['zone'].astype("category")
    
    return(df)

# tickers = ['BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','ADAUSDT','DOGEUSDT','AVAXUSDT','DOTUSDT','SOLUSDT','MATICUSDT']
tickers = ['ADAUSDT']
tf = '4h'
lineToken ='jYEyzns1dt6rXVHunn4dTa2xMX06OPBsOwFJQCw1ITJ'
risk = 20 # 20USD per order

for ticker in tickers:
    df = getCryptoPrice(ticker, tf)
    df = waveTunnel(df)
    df = AOZ(df)
    zone = df.tail(1)['zone'].values[0]
    entryLevel = df.tail(1)['entryLevel'].values[0]
    slLevel = df.tail(1)['sl'].values[0]
    tp1Level = df.tail(1)['tp1'].values[0]
    tp2Level = df.tail(1)['tp2'].values[0]
    if entryLevel != 0:
        if zone == 1:
            stopLoss = entryLevel - slLevel
            size = risk / stopLoss
            cost = entryLevel * size
            margin = 5 * risk
            leverage = cost / margin
            msg = f'BUY STOP\nrisk: {risk}USDT\nticker: {ticker}\nentry: {entryLevel}\nsize: {size}\nleverage: {leverage}X\nSL: {slLevel}\nTP1: {tp1Level}\nTP2: {tp2Level}'
            lineNotify(msg, lineToken)
        elif zone == -1:
            stopLoss = slLevel - entryLevel
            size = risk / stopLoss
            cost = entryLevel * size
            margin = 5 * risk
            leverage = cost / margin
            msg = f'SELL STOP\nrisk: {risk}USDT\nticker: {ticker}\nentry: {entryLevel}\nsize: {size}\nleverage: {leverage}X\nSL: {slLevel}\nTP1: {tp1Level}\nTP2: {tp2Level}'
            lineNotify(msg, lineToken)
        else: 
            msg = f'{ticker} - NO SIGNAL'    
            lineNotify(msg, lineToken)
    # print(df)
    # df.to_excel(f'{ticker}.xlsx')

lineNotify("Completed", lineToken)