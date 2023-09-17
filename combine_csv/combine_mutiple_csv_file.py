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
csv_files = glob.glob(path + "/*.csv")


# %%
len(csv_files)


# %%
# for filename in csv_files:
#     # Get stock name from filename
#     name_csv = filename.split('\\')[-1]
# #     name = name_csv.split('.')[0]
#     name = name_csv.split(' ')[0]
# #     print(name)
    
#     # Read in data
#     df = pd.read_csv(filename, header = [2])
# # pd.set_option('display.max_rows', df.shape[0]+1)
# # print(df['Unnamed: 0'])


# %%
all_stock_df = pd.DataFrame()
revenue_df = pd.DataFrame()
gpm_df = pd.DataFrame()
eps_df = pd.DataFrame()
dividend_df = pd.DataFrame()
pbv_df = pd.DataFrame()
sga_df = pd.DataFrame()
npm_df = pd.DataFrame()
roe_df = pd.DataFrame()
de_df = pd.DataFrame()


for filename in csv_files:
    # Get stock name from filename
    name_csv = filename.split('\\')[-1]
#     name = name_csv.split('.')[0]
    name = name_csv.split(' ')[0]
    print(name)
    
    # Read in data
    df = pd.read_csv(filename, header = [2])
    
    # Split column name
    for i in range(1, 11):
        col_name = df.columns[i].split('-')[0]
        df.rename(columns = {df.columns[i] : col_name}, inplace = True)
        
    # Renaming and add stock name
    df.rename(columns = {'Unnamed: 0' : 'Item'}, inplace = True)
#     df.rename(columns = {'Unnamed: 0' : 'Item', df.columns[1] : '2011', df.columns[2] : '2012', df.columns[3] : '2013',df.columns[4] : '2014', df.columns[5] : '2015', df.columns[6] : '2016', df.columns[7] : '2017', df.columns[8] : '2018', df.columns[9] : '2019', df.columns[10] : '2020'}, inplace = True)
#     print(df.columns[1].split('-')[0])
    df['Stock Name'] = name
    df.drop(columns = 'TTM', inplace = True)
    
#     df.set_index('Item', inplace=True)
    
#     for col in df.columns:
#         print(col)
    
    # Split section
#     section1 = df[0:15] 
#     section2 = df[17:26]
#     section3 = df[27:35]
#     section4 = df[37:57]
#     section5 = df[59:64] 
#     section6 = df[66:86] 
#     section7 = df[88:92] 
#     section8 = df[93:101]
    
    revenue = df[0:1]
#     gpm = df[1:2]
    eps = df[5:6]
    dividend = df[6:7]
    pbv = df[9:10]
#     sga = df[20:21]
#     npm = df[28:29]
#     roe = df[32:33]
#     de = df[90:91]

#     revenue = df.loc['Revenue THB Mil']
#     gpm = df.loc['Gross Margin %']
#     eps = df.loc['Earnings Per Share THB']
#     dividend = df.loc['Dividends THB']
#     pbv = df.loc['Book Value Per Share * THB']
#     sga = df.loc['SG&A']
#     npm = df.loc['Net Margin %']
#     roe = df.loc['Return on Equity %']
#     de = df.loc['Debt/Equity']
    
    
#     df_temp1 = section1.append(section2.append(section3).append(section4))
#     df_temp2 = section5.append(section6.append(section7.append(section8)))
    
#     df_total = df_temp1.append(df_temp2)
#     all_stock_df = all_stock_df.append(df_total)

    revenue_df = revenue_df.append(revenue)
#     gpm_df = gpm_df.append(gpm)
    eps_df = eps_df.append(eps)
    dividend_df = dividend_df.append(dividend)
    pbv_df = pbv_df.append(pbv)
#     sga_df = sga_df.append(sga)
#     npm_df = npm_df.append(npm)
#     roe_df = roe_df.append(roe)
#     de_df = de_df.append(de)
    
    print('Done')
    print('#'*30)

# print(df.head(30))


# %%
#colnaming = pd.read_excel('col_name.xlsx' )
#all_stock_df.columns = colnaming.columns


# %%
# all_stock_df.to_excel('total_stock_index2.xlsx')
revenue_df.to_excel('SET REVENUE.xlsx')
# gpm_df.to_excel('SET GPM.xlsx')
eps_df.to_excel('SET EPS.xlsx')
dividend_df.to_excel('SET DIVIDEND.xlsx')
pbv_df.to_excel('SET PBV.xlsx')
# sga_df.to_excel('SET SGA.xlsx')
# npm_df.to_excel('SET NPM.xlsx')
# roe_df.to_excel('SET ROE.xlsx')
# de_df.to_excel('SET DE.xlsx')


# %%



