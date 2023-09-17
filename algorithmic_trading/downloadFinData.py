### Download financial statment (yahoo finance)

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import math
import os
import glob

def getEndPeriodPrice(ticker,dateIndex):
    try:
        price = yf.download(f'{ticker}',period = "5y",interval = "1d")
        # print(price)
    except Exception as e:
        print(f'{ticker} - download price error - {e}')
        
    dfPrice = pd.DataFrame()
    lstPrice = []
    for i in range(len(dateIndex)):
        # print(type(dateIndex[i]))
        # print(type(price.index[0]))
        try:
            if dateIndex[i] >= price.index[0] and dateIndex[i] <= price.index[-1] :
                idx = price.index[price.index.get_loc(dateIndex[i], method='pad')]
                # idx = price.index.get_indexer(dateIndex[i], method='pad')
                # idx = price.get_indexer(dateIndex[i], method='pad')
                lstPrice.append(price.Close[idx])
                # lstPrice = pd.concat([lstPrice,price.Close[idx]])
            else:
                lstPrice.append(np.nan)
                # lstPrice = pd.concat([lstPrice,np.nan])
                print(f'{ticker} - out of range')
        except Exception as e:
                print(f'{ticker} - index error {e}')
                
    dfPrice["Price"] = pd.DataFrame(lstPrice, dateIndex)
    print(dfPrice.T)
    return dfPrice.T

def combineDF(filePaths):
    dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
    fileName = filePaths[0].split('\\')[-1]
    fileName = f'{fileName.split("_")[0]}_{fileName.split("_")[1]}'
    
    df1 = pd.DataFrame()
    
    for filename in filePaths:
        df = pd.read_pickle(filename)
        # df1 = df1.append(df)
        df1 = pd.concat([df1,df])

    df1.drop_duplicates
    df1.to_pickle(f'{fileName}_{dt_string}.pkl')

# read excel file
sheetName = "SET"
stockTicker = pd.read_excel("tickers.xlsx", header=0, sheet_name=sheetName)
stockTicker = stockTicker["Symbol"].values.tolist()

###########################
m = len(stockTicker)
n = 10
p = math.ceil(m/n)

for i in range(0,p):
    df = pd.DataFrame()
    dfInfo = pd.DataFrame()
    dfBalanceSheet = pd.DataFrame()
    dfCashFlow = pd.DataFrame()
    dfEarnings = pd.DataFrame()
    dfFinancials = pd.DataFrame()
    
    for j in range(0,n):
        q = i*n + j
        
        if q < m:
            try:
                # set ticker symbol
                ticker = yf.Ticker(f'{stockTicker[q]}')

                # download info
                info = ticker.info
                # price = ticker.history(period="max")
                df = df.from_dict(info, orient='index')
                # dfInfo = dfInfo.append(df.T, ignore_index=True)
                dfInfo = pd.concat([dfInfo,df.T],ignore_index=True)

                # download balance sheet and price for calculation
                balanceSheet = ticker.balance_sheet
                dfPrice = getEndPeriodPrice(f'{stockTicker[q]}',balanceSheet.columns)
                # balanceSheet = balanceSheet.append(dfPrice).T
                balanceSheet = pd.concat([balanceSheet,dfPrice]).T
                balanceSheet["Symbol"] = stockTicker[q]
                # dfBalanceSheet = dfBalanceSheet.append(balanceSheet)
                dfBalanceSheet = pd.concat([dfBalanceSheet,balanceSheet])

                # download cashflow
                cashFlow = ticker.cashflow
                cashFlow = cashFlow.T
                cashFlow["Symbol"] = stockTicker[q]
                # dfCashFlow = dfCashFlow.append(cashFlow)
                dfCashFlow = pd.concat([dfCashFlow,cashFlow])

                # download earning
                earnings = ticker.earnings
                earnings["Symbol"] = stockTicker[q]
                # dfEarnings = dfEarnings.append(earnings)
                dfEarnings = pd.concat([dfEarnings,earnings])

                # download financials data
                financials = ticker.financials
                financials = financials.T
                financials["Symbol"] = stockTicker[q]
                # dfFinancials = dfFinancials.append(financials)
                dfFinancials = pd.concat([dfFinancials,financials])
        
                print(f'{i} {q} {stockTicker[q]} completed')
        
            except Exception as e:
                print(f'{i} {q} {stockTicker[q]} {e}')
        else:
            break
    
    # save df to pkl
    dfInfo.to_pickle(f'pkl/{sheetName}_Info_{i}.pkl')
    dfBalanceSheet.to_pickle(f'pkl/{sheetName}_BalanceSheet_{i}.pkl')
    dfCashFlow.to_pickle(f'pkl/{sheetName}_CashFlow_{i}.pkl')
    dfEarnings.to_pickle(f'pkl/{sheetName}_Earnings_{i}.pkl')
    dfFinancials.to_pickle(f'pkl/{sheetName}_Financials_{i}.pkl')

# combine pkl (DF) to single file
# get path directory
path = os.getcwd()

# read all files in each folder
pkl_Info_files = glob.glob(path + f'/pkl/{sheetName}_Info*.pkl')
pkl_BalanceSheet_files = glob.glob(path + f'/pkl/{sheetName}_BalanceSheet*.pkl')
pkl_CashFlow_files = glob.glob(path + f'/pkl/{sheetName}_CashFlow*.pkl')
pkl_Earnings_files = glob.glob(path + f'/pkl/{sheetName}_Earnings*.pkl')
pkl_Financials_files = glob.glob(path + f'/pkl/{sheetName}_Financials*.pkl')

combineDF(pkl_Info_files)
combineDF(pkl_BalanceSheet_files)
combineDF(pkl_CashFlow_files)
combineDF(pkl_Earnings_files)
combineDF(pkl_Financials_files)