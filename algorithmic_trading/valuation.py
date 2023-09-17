import pandas as pd

df = pd.read_excel("G:\\My Drive\\Coding\\trading\\SET_20220406_185710.xlsx", index_col=[0,1])
# pd.to_numeric(df)
symbols = df.index.get_level_values('Symbol').drop_duplicates().to_list()
finStatment = df.index.get_level_values('FinStmt').drop_duplicates().to_list()

for symbol in symbols:
    temp = df[df.index.get_level_values('Symbol').isin([symbol])]
    # Check NaN columns
    for col in temp.columns:
        if(temp[col].isnull().any()):
            temp.drop(columns=col,inplace=True)
    eps = temp[temp.index.get_level_values('FinStmt') == 'EPS'].values
    price = temp[temp.index.get_level_values('FinStmt') == 'LastPrice'].values
    dvdYield = temp[temp.index.get_level_values('FinStmt') == 'DividendYield'].values
    payoutRatio = (dvdYield * price / eps) / 100
