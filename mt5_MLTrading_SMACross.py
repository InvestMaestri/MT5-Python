# Script to get started in Machine Learning with a SMA Cross strategy.
# By Eduardo Bogosian 2023
import pytz

import numpy as np
import pandas as pd
import pandas_ta as ta
import MetaTrader5 as mt5
import matplotlib.pyplot as plt

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from datetime import datetime

mt5.initialize()
timezone = pytz.timezone("Etc/UTC")
from_date = datetime.now()
look_back = 25000
historical_data = mt5.copy_rates_from("AAPL", mt5.TIMEFRAME_H1, from_date, look_back)
df = pd.DataFrame(historical_data)
df['time'] = pd.to_datetime(df['time'], unit='s')

del df['tick_volume']
del df['real_volume']
del df['spread']

print(f'Historical Data:\n{df}')

Fast_Period = 12
Slow_Period = 24
df['Fast_MA'] = ta.sma(df['close'], Fast_Period)
df['Slow_MA'] = ta.sma(df['close'], Slow_Period)
df = df.dropna()
df.reset_index(drop=True, inplace=True)

print(df)

df['Cross_Over'] = ta.cross(df['Fast_MA'], df['Slow_MA'], True)
df['Cross_Under'] = ta.cross(df['Fast_MA'], df['Slow_MA'], False)
del df['time']
del df['open']
del df['high']
del df['low']
del df['close']
del df['Fast_MA']
del df['Slow_MA']
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# cross_count = df['Cross_Over'].sum() + df['Cross_Under'].sum()
# print(f'Total Crosses: {cross_count}')

df['Long'] = np.where(df['Cross_Over'] == 1, 1, 0)
df['Short'] = np.where(df['Cross_Under'] == 1, 1, 0)
# Remove bad first row
df = df.iloc[1:]  # Slice it? Better start calling me... Butcher!
df.reset_index(drop=True, inplace=True)

# Little sanity check on our actions
long_cross_min = df['Long'].min()
long_cross_max = df['Long'].max()
long_cross_average = df['Long'].mean()
long_cross_sum = df['Long'].sum()
print(f'Long List Check:\nMin Value: {long_cross_min}\nMax Value:{long_cross_max}\nAverage Value: {long_cross_average}\nTotal Longs:{long_cross_sum}\n')

short_cross_min = df['Short'].min()
short_cross_max = df['Short'].max()
short_cross_average = df['Short'].mean()
short_cross_sum = df['Short'].sum()
print(f'Short List Check:\nMin Value: {short_cross_min}\nMax Value:{short_cross_max}\nAverage Value: {short_cross_average}\nTotal Shorts:{short_cross_sum}\n')
print(df)

# Training data
X_train = df.drop(['Long', 'Short'], axis=1)  # Only copy inputs
y_train = df[['Long', 'Short']]  # Only copy the outputs
print(f'Training:\n{X_train}\nLabels:\n{y_train}')

# Setup Neural Network
model = Sequential()
model.add(Dense(2, activation='sigmoid',
                input_shape=(X_train.shape[1], 2)))  # Output (Sigmoid for two-class classification)

# Compile the model
optimizer = Adam(learning_rate=0.001)
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.summary()

# Train
history = model.fit(X_train, y_train,
                    epochs=1000,
                    batch_size=32,
                    validation_split=0.1)

# Plot training & validation loss values
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Plot training & validation accuracy values
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()
