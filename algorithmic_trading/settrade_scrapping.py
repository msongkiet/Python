# importing the libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
# import math
from datetime import datetime

def getFinancialData(symbol):
    
    if symbol.find('&'):
        s = symbol.replace('&','%26')
    else:
        s = symbol
    
    df = pd.DataFrame()
    # Step 1: Sending a HTTP request to a URL
    url = f'https://classic.set.or.th/set/companyhighlight.do?symbol={s}&ssoPageId=5&language=en&country=US'
    
    try:
        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(url).text

        # Step 2: Parse the html content
        soup = BeautifulSoup(html_content, 'lxml')
        # print(soup.prettify()) # print the parsed data of html

        # Step 3: Analyze the HTML tag, where your content lives    
        # Get the table having the class table table-hover table-info
        gdp_table = soup.find('table',attrs={'class':'table table-hover table-info'})

        t_headers = []
        for th in gdp_table.find_all('th'): #[:5]: # Loop only first 5 headers
            # remove any symbol and extra spaces from left and right
            if th.text.startswith('Y'):
                t_headers.append(th.text.replace('/','').replace(' ','_').replace("'",'').strip()[:5])
            else:
                t_headers.append(th.text.strip())
                # t_headers.append(th.text.strip().split()[0])

        # Get all the rows of table
        table_data = []
        for tr in gdp_table.tbody.find_all('tr'): # find all tr's from table's tbody
            t_row = {}

            # find all td in tr and zip it with t_header
            for td, th in zip(tr.find_all('td'), t_headers): 
                t_row[th] = td.text.replace(',', '').strip()
            table_data.append(t_row)

        df = pd.DataFrame.from_dict(table_data)
        # df.drop(df.columns[[len(df.columns)-1,]], axis=1, inplace=True)
       
        for col in df.columns:
            if(col.startswith('Y')): # Keep Year end data
                df[col] = pd.to_numeric(df[col],errors='coerce')
            elif(col.startswith('Q')): # Drop Quarterly data
                df.drop(columns=col,inplace=True)
            elif(col == ''):
                df.drop(columns=[""],inplace=True) # Drop no header data
        # 
        df.drop({0,9,13,16},inplace=True)
        # df.dropna(inplace=True) # Drop all n/a
        # df.reset_index(drop=True,inplace=True)
        df.rename(columns = {'Period  as of':'FinStmt'}, inplace = True)
        df = df.replace({'Paid-up Capital':'PaidCapital','Profit (Loss) from Other Activities':'ProfitfromOtherActivities','Net Profit':'NetProfit','EPS (Baht)':'EPS','ROA(%)':'ROA','ROE(%)':'ROE','Net Profit Margin(%)':'NPM','Last Price(Baht)':'LastPrice','Market Cap.':'MarketCap','P/E':'PE','P/BV':'PBV','P/NAV':'PNAV','Book Value per share (Baht)':'BVPS','Dvd. Yield(%)':'DividendYield'})

        df['Symbol'] = symbol
        df.set_index(['Symbol', 'FinStmt'],inplace=True)

    except Exception as e:

        print(f'{symbol}: {e}')

    # print(df)
    return df

# read excel file
sheetName = "SET"
stockTicker = pd.read_excel("G:\\My Drive\\coding\\python\\_algorithmic_trading\\tickers.xlsx", header=0, sheet_name=sheetName)
stockTicker = stockTicker["Symbol"].values.tolist()

df = pd.DataFrame()
for s in stockTicker:
    try:
        df = pd.concat([df, getFinancialData(symbol=s.split('.')[0])])
        print(f'{s.split(".")[0]} completed')

    except Exception as e:
        print(f'{s.split(".")[0]} {e}')

dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
df.to_excel(f'{sheetName}_{dt_string}.xlsx')