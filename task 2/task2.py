# -*- coding: utf-8 -*-
"""task2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yNF_p61EFyC8hKyFrt265cDz3b58nXIV
"""

import pandas as pd
file_path = 'aapl.csv'
df = pd.read_csv(file_path)
df.head()

# Step 2: Preprocess the data
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


data = df[['Close']].values


scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Function to create a dataset suitable for LSTM
def create_dataset(data, time_step=60):
    X, Y = [], []
    for i in range(len(data) - time_step - 1):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

# Prepare the dataset
time_step = 60
X, Y = create_dataset(scaled_data, time_step)

# Reshape X to be [samples, time_steps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("Shape of X_train:", X_train.shape)
print("Shape of X_test:", X_test.shape)
print("Shape of Y_train:", Y_train.shape)
print("Shape of Y_test:", Y_test.shape)

# Step 3: Create and train the LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(Dropout(0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train, Y_train, epochs=20, batch_size=64, validation_data=(X_test, Y_test), verbose=1)

# Step 4: Make predictions and evaluate the model
import matplotlib.pyplot as plt

# Make predictions
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Inverse transform the predictions and actual values to get the real values
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
Y_train_actual = scaler.inverse_transform([Y_train])
Y_test_actual = scaler.inverse_transform([Y_test])

# Plot the results
plt.figure(figsize=(14, 5))
plt.plot(df.index, scaler.inverse_transform(scaled_data), label='Actual Price')
plt.plot(df.index[time_step:len(train_predict) + time_step], train_predict, label='Train Predictions')
plt.plot(df.index[len(train_predict) + (time_step*2) + 1: len(scaled_data) - 1], test_predict, label='Test Predictions')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()