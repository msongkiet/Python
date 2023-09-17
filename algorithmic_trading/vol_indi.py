import talib

def vol_indi(df):
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