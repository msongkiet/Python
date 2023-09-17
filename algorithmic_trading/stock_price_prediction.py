# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#import the library
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# %%
#Get the stock price
df = web.DataReader('CPALL.BK', data_source='yahoo', start='2011-01-01', end='2021-06-15')

#Show data
df


# %%
#Visualize the close price history
plt.figure(figsize=(16,8))
plt.title('Close Price History ')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price (THB)', fontsize=18)
plt.show()


# %%
#Create a new dataframe with only the 'Close' column
data = df.filter(['Close'])
#Convert the dataframe to numpy array
dataset = data.values
#Get the number of rows to train the model 
training_data_len = math.ceil(len(dataset) * .8)

training_data_len


# %%
#Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data


# %%
#Create the training data set
#Create the scaled training data set
train_data = scaled_data[0:training_data_len, :]

#Split the data into x_train and y_train data set
x_train = []
y_train = []

for i in range(60, len(train_data)):
  x_train.append(train_data[i-60:i, 0])
  y_train.append(train_data[i, 0])
  if i <= 61:
    print(x_train)
    print(y_train)


# %%
#Convert the x_train and y_train to numpy array
x_train, y_train = np.array(x_train), np.array(y_train)


# %%
#Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_train.shape


# %%
#Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))


# %%
#Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')


# %%
#Train the model
model.fit(x_train, y_train, batch_size=1, epochs=1)


# %%
#Create the testing data set
#Create a new array contianing scaled values from index 1981 to 2041
test_data = scaled_data[training_data_len - 60: , :]
#Create the data sete x_test and y_test
x_test = []
y_test = dataset[training_data_len: , :]

for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i, 0])


# %%
#Convert the data to numpy array
x_test = np.array(x_test)


# %%
#Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))


# %%
#Get the models pridicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)


# %%
#Get the root mean squared error (RMSE)
rmse = np.sqrt(np.mean(((predictions- y_test)**2)))
rmse


# %%
#Plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#Visualize the data
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price THB', fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close', 'Predictions']])
plt.legend(['Train', 'Val', 'Prediction'], loc='lower_right')
plt.show()


# %%
#Show the valid and predicted prices
valid


# %%
#Get the quote
cpall_quote = web.DataReader('CPALL.BK', data_source='yahoo', start='2011-01-01', end='2021-06-19')
#Create new dataframe
new_df = cpall_quote.filter(['Close'])
#Get last 60 days closing price values and convert to numpy array
last_60_days = new_df[-60:].values
#Scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
#Create emtry list
X_test = []
#Append the padt 60 days
X_test.append(last_60_days_scaled)
#Convert X_test dataset to numpy array
X_test = np.array(X_test)
#Reshape the data
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1],1))
#Get the predicticed scaled price
pred_price = model.predict(X_test)
#undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)


# %%



# %%
#Get the quote
cpall_quote2 = web.DataReader('CPALL.BK', data_source='yahoo', start='2021-06-19', end='2021-06-19')
print(cpall_quote2['Close'])


# %%



