# Download SET history price for Amibroker

# import library
import pandas as pd
import numpy as np
from tqdm import tqdm
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# import date library
from datetime import date
today = date.today().strftime("%m_%d_%y")

print('pandas v.',pd.__version__,
      '\numpy v.',np.__version__,
      '\nyfinace v.',yf.__version__)

# read SET symbol
df_symbol = pd.read_csv('download price history\Symbol_SET.csv')
tickers = df_symbol[df_symbol['Symbol'].str.contains('-R.BK') == False].reset_index(drop=True)
tickers.head()

# ticker: equity symbol in yahoo finance
# periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max (time period)
# interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo (trading interval)
# fetch data by interval (including intraday if period < 60 days)
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

period = '1mo'
interval = '1d'
savePath = 'G://My Drive//Amibroker DB//SET'

for ticker in tqdm(tickers['Symbol'][:]):
    df = yf.download(tickers = ticker, period = period, interval = interval)
    symbol = ticker.split(".")[0]
    df['Symbol'] = ticker
    df.to_csv(f'download price history//csv//{symbol}.csv')
#     df.to_csv(f'{savePath}//{symbol}.csv')

      
