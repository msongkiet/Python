import pandas as pd
import numpy as np

df = pd.read_csv(r'D:\nextcloud\Home Share Folder\SM\algo101\Data 1min_20170111_CSV\EURUSD_1_MT4.csv', header=None)
df.columns = ['date','time','o','h','l','c','v']
df['checkOpenPrice'] = np.where((df['o'] > df['h']) | (df['o'] < df['l']), 1, np.nan)
df['checkClosePrice'] = np.where((df['c'] > df['h']) | (df['c'] < df['l']), 1, np.nan)
dfTemp = df[['checkOpenPrice','checkClosePrice']]
print(dfTemp.sum())