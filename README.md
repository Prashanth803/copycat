import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import random

# Function to generate simulated data
def generate_simulated_data(start_time, periods, freq='T'):
    times = pd.date_range(start_time, periods=periods, freq=freq)
    prices = [100 + random.gauss(0, 1) for _ in range(periods)]
    volumes = [random.randint(100, 1000) for _ in range(periods)]
    data = pd.DataFrame({'Datetime': times, 'Price': prices, 'Volume': volumes})
    data.set_index('Datetime', inplace=True)
    return data

# Function to calculate OBV
def calculate_obv(data):
    obv = [0]
    for i in range(1, len(data)):
        if data['Price'][i] > data['Price'][i-1]:
            obv.append(obv[-1] + data['Volume'][i])
        elif data['Price'][i] < data['Price'][i-1]:
            obv.append(obv[-1] - data['Volume'][i])
        else:
            obv.append(obv[-1])
    data['OBV'] = obv

# Function to generate buy or sell signals
def generate_signals(data):
    data['Signal'] = 0
    data['Signal'][1:] = [1 if data['OBV'][i] > data['OBV'][i-1] else -1 for i in range(1, len(data))]
    data['Position'] = data['Signal'].diff()

# Function to update the data with new simulated data
def update_data(data, new_data):
    return pd.concat([data, new_data])

# Function to plot data
def plot_data(data):
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)
    plt.plot(data['Price'], label='Price')
    plt.title('Price and OBV')
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(data['OBV'], label='OBV', color='orange')
    plt.scatter(data.index, data['Signal'], color='red', marker='o', label='Buy/Sell Signal')
    plt.legend()
    plt.show()

# Main function to run the simulation
def run_simulation():
    start_time = datetime.now()
    data = generate_simulated_data(start_time, periods=60)  # Initial 60 minutes of data

    while True:
        calculate_obv(data)
        generate_signals(data)
        plot_data(data)
        
        # Simulate getting new data every 5 minutes
        time.sleep(5 * 60)
        new_data = generate_simulated_data(start_time + timedelta(minutes=len(data)), periods=5)
        data = update_data(data, new_data)
        start_time += timedelta(minutes=5)

# Run the simulation
run_simulation()
