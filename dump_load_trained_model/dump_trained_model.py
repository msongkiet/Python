import pandas as pd
import numpy as np
from sklearn import linear_model

df = pd.DataFrame(columns=['area', 'price'],
                 data = [[2600,550000],
                        [3000,565000],
                        [3200,610000],
                        [3600,680000],
                        [4000,725000]])

print(df)

model = linear_model.LinearRegression()
model.fit(df[['area']], df.price)

print(f'Coefficient : {model.coef_}')
print(f'Intercept : {model.intercept_}')

print(model.predict([[5000]]))

# dump trained model
from joblib import dump
dump(model,'model_joblib')