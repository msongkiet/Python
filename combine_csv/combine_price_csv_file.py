# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# Data Manipulation Library
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from datetime import timedelta
import random
import os
import glob


# %%
path = os.getcwd()
csv_files = glob.glob(path + "/price_yearly/*.csv")


# %%
len(csv_files)


# %%
price_df = pd.DataFrame()

for filename in csv_files:
    # Get stock name from filename
    name_csv = filename.split('\\')[-1]
    name = name_csv.split(' ')[0]
#     print(name)

    # Read in data
    df = pd.read_csv(filename, header = [1])
    
    # Change string to date format 
#     df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y')
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m')
    
    # Delete columns
    df.drop(columns = 'Volume', inplace = True)
    df.drop(columns = 'Open', inplace = True)
    df.drop(columns = 'High', inplace = True)
    df.drop(columns = 'Low', inplace = True)

    df = df.T
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:2] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    df['Stock Name'] = name

    price = df.loc['Close']
    price_df = price_df.append(price)

price_df = price_df.where(pd.notnull(price_df), "")
print(price_df)


# %%
price_df.to_excel('SET PRICE.xlsx')


# %%



