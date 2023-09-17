def cdc_scan(df, backtest_preriod = 1):
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