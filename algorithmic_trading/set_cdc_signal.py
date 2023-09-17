from datetime import date
from yf_price import get_yf_price
from cdc_indi import cdc_indi
from cdc_scan import cdc_scan
from vol_indi import vol_indi
from line import lineNotify

import pandas as pd
import os

# token = os.environ.get('token_line_trading_signal')
token = os.environ.get('token_line_test')
googleSheetId = os.environ.get('googleSheetId_quote')

worksheetName = ['SET100', 'sSET']
period = ["3mo"]
interval = ["1d"]

if date.today().isoweekday() == 5: # 5 is Friday
    period = ["3mo", "1y"]
    interval = ["1d", "1wk"]

for k in range(len(period)):
    for i in range(len(worksheetName)):
        url_google_sheet = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(googleSheetId, worksheetName[i])
        tickers = pd.read_csv(url_google_sheet)
        tickers = (tickers['Quote'].values.tolist())

        msg_golden_cross = ''
        msg_dead_cross = ''
        msg_pre_buy = ''
        msg_pre_sell = ''
        df_vol = pd.DataFrame()
        
        for j in range(len(tickers)):
            try:
                df_price = get_yf_price(tickers[j], period[k], interval[k])
                df_price = cdc_indi(df_price)
                df_price = vol_indi(df_price)
                print('{0} {1}'.format(tickers[j], df_price.shape))
                df_vol = df_vol.append(df_price.tail(1),ignore_index=False)

                signal = cdc_scan(df_price)
                if(len(signal)!=0):
                    if(signal == 'bullish'):
                        msg_golden_cross += '{0} '.format(tickers[j].split(".")[0])
                    elif(signal == 'bearish'):
                        msg_dead_cross += '{0} '.format(tickers[j].split(".")[0])
                    elif(signal == 'blue'):
                        msg_pre_buy += '{0} '.format(tickers[j].split(".")[0])
                    elif(signal == 'yellow'):
                        msg_pre_sell += '{0} '.format(tickers[j].split(".")[0])
            except Exception as e:
                print(e)

        df_vol = df_vol.sort_values(by=['x_of_vol_ma'],ascending=False)   
        msg_vol_change = ''

        for row in df_vol.itertuples():
            if row.x_of_vol_ma >= 1.50:
                msg_vol_change += '{0}:{1}X, '.format(row.ticker, row.x_of_vol_ma)
            else:
                break
 
        # line_notify(f'{worksheetName[i]} TF:{interval[k]} CDC Golden Cross: {msg_golden_cross}', token)
        line_notify('{0} TF:{1} CDC Golden Cross: {2}'.format(worksheetName[i], interval[k], msg_golden_cross), token)
        line_notify('{0} TF:{1} CDC Dead Cross: {2}'.format(worksheetName[i], interval[k], msg_dead_cross), token)
        line_notify('{0} TF:{1} CDC Pre-Buy Zone: {2}'.format(worksheetName[i], interval[k], msg_pre_buy), token)
        line_notify('{0} TF:{1} CDC Pre-Sell Zone: {2}'.format(worksheetName[i], interval[k], msg_pre_sell), token)
        line_notify('{0} TF:{1} Vol change (x of vol ma): {2}'.format(worksheetName[i], interval[k], msg_vol_change), token)

        # line_notify(f'{worksheetName[i]} TF:{interval[k]} CDC Dead Cross: {msg_dead_cross}', token)
        # line_notify(f'{worksheetName[i]} TF:{interval[k]} CDC Pre-Buy Zone: {msg_pre_buy}', token)
        # line_notify(f'{worksheetName[i]} TF:{interval[k]} CDC Pre-Sell Zone: {msg_pre_sell}', token)
        # line_notify(f'{worksheetName[i]} TF:{interval[k]} Vol change (x of vol ma): {msg_vol_change}', token)