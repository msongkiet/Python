import talib

def cdc_indi(df):
    src = df['ohlc4']
    fast_ema = 12
    slow_ema = 26
    trend_list = []
    zone_list = []

    try:
        df['avg_src'] = talib.EMA(src,2)
        df['fast_ema'] = talib.EMA(df['avg_src'], fast_ema)
        df['slow_ema'] = talib.EMA(df['avg_src'], slow_ema)
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