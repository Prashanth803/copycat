import random
import datetime


def generate_stock_data(symbol, start_price):
    stock_data = []
    current_price = start_price
    start_time = datetime.datetime.now()

    for i in range(5 * 60):
        open_price = current_price
        high_price = open_price + random.uniform(0, 0.2)
        low_price = open_price - random.uniform(0, 0.2)
        close_price = random.uniform(low_price, high_price)
        volume = random.randint(1, 10)
        current_price = close_price 

        timestamp = start_time + datetime.timedelta(seconds=i)
        
        stock_data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': symbol,
            'open': round(open_price, 2),
            'close': round(close_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'volume': volume
        })

    return stock_data


stock_symbol = 'XYZ'
starting_price = 100  

data = generate_stock_data(stock_symbol, starting_price)



# for entry in data:
#     timestamp = entry['timestamp']
#     symbol = entry['symbol']
#     open_price = entry['open']
#     close_price = entry['close']
#     high_price = entry['high']
#     low_price = entry['low']
#     volume = entry['volume']
    
# how cam simulator be helpful in backtesting to know our accuracy
   
#     print(f"Timestamp: {timestamp}, Symbol: {symbol}, Open: {open_price}, Close: {close_price}, High: {high_price}, Low: {low_price}, Volume: {volume}")
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch historical data
def fetch_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data['Date'] = stock_data.index
    return stock_data

# Define the SMA crossover strategy
def sma_crossover_strategy(data, short_window, long_window):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    # Short moving average
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    # Long moving average
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Create signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()

    return signals

# Backtesting the strategy
def backtest_strategy(data, signals):
    initial_capital = float(100000.0)
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    portfolio = pd.DataFrame(index=signals.index).fillna(0.0)

    positions['stock'] = signals['signal'] * 100  # Assume buying 100 shares per signal
    portfolio['positions'] = (positions.multiply(data['Close'], axis=0))
    portfolio['cash'] = initial_capital - (positions.diff().multiply(data['Close'], axis=0)).cumsum()
    portfolio['total'] = portfolio['positions'] + portfolio['cash']

    return portfolio

# Fetch the data for AAPL from Jan 1, 2020 to Dec 31, 2023
stock_data = fetch_data('AAPL', '2020-01-01', '2023-12-31')

# Apply the strategy
signals = sma_crossover_strategy(stock_data, short_window=40, long_window=100)

# Backtest the strategy
portfolio = backtest_strategy(stock_data, signals)

# Output results
print(portfolio.tail())

# Plot the results
plt.figure(figsize=(14, 7))
plt.plot(portfolio['total'], label='Portfolio value')
plt.title('Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.show()


# RSI and plot the graph continuosly and no refreshing is done and the data is recieved every 5 minutes and the RSI must be plotted

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import time
from datetime import datetime

# Replace with your API endpoint and parameters
API_URL = 'https://api.example.com/rsi'
API_KEY = 'your_api_key'  # If needed

# Initialize lists to store time and RSI values
times = []
rsi_values = []

# Function to fetch RSI data from the API
def fetch_rsi():
    response = requests.get(API_URL, headers={'Authorization': f'Bearer {API_KEY}'})
    data = response.json()
    # Extract the RSI value from the API response (adjust according to your API's response structure)
    rsi = data['rsi']
    return rsi

# Function to update the plot
def update_plot(frame):
    current_time = datetime.now().strftime('%H:%M:%S')
    try:
        rsi = fetch_rsi()
        times.append(current_time)
        rsi_values.append(rsi)
        print(f"Fetched RSI: {rsi} at {current_time}")

        # Keep the last 60 data points for better visualization
        if len(times) > 60:
            times.pop(0)
            rsi_values.pop(0)

        # Clear and re-plot
        ax.clear()
        ax.plot(times, rsi_values, label='RSI')
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Real-Time RSI Plot')
        plt.ylabel('RSI')
        plt.xlabel('Time')
        plt.legend()
    except Exception as e:
        print(f"Error fetching or plotting data: {e}")

# Set up the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_plot, interval=300000)  # 300000 ms = 5 minutes

plt.show()




# To integrate buy or sell signals based on RSI into the graph, we need to:
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import quandl
from datetime import datetime, timedelta
import pandas as pd

# Replace with your Quandl API key
QUANDL_API_KEY = 'your_quandl_api_key'
quandl.ApiConfig.api_key = QUANDL_API_KEY

# Function to fetch RSI data from Quandl
def fetch_rsi():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Fetch last 30 days of data for RSI calculation
    data = quandl.get("CHRIS/CME_CL1", start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))
    
    # Calculate RSI using pandas (example using close price)
    delta = data['Last'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Return the latest RSI value and full RSI series
    return rsi.iloc[-1], rsi

# Initialize lists to store time and RSI values
times = []
rsi_values = []
buy_signals = []
sell_signals = []

# Function to update the plot
def update_plot(frame):
    current_time = datetime.now().strftime('%H:%M:%S')
    try:
        latest_rsi, full_rsi = fetch_rsi()
        times.append(current_time)
        rsi_values.append(latest_rsi)
        print(f"Fetched RSI: {latest_rsi} at {current_time}")

        # Determine buy/sell signals
        if latest_rsi < 30:
            buy_signals.append((current_time, latest_rsi))
            sell_signals.append((None, None))  # No signal
            signal = 'Buy'
        elif latest_rsi > 70:
            sell_signals.append((current_time, latest_rsi))
            buy_signals.append((None, None))  # No signal
            signal = 'Sell'
        else:
            buy_signals.append((None, None))  # No signal
            sell_signals.append((None, None))  # No signal
            signal = None

        # Keep the last 60 data points for better visualization
        if len(times) > 60:
            times.pop(0)
            rsi_values.pop(0)
            buy_signals.pop(0)
            sell_signals.pop(0)

        # Clear and re-plot
        ax.clear()
        ax.plot(times, rsi_values, label='RSI')
        for i, (time, rsi) in enumerate(buy_signals):
            if time is not None:
                ax.annotate('Buy', (time, rsi), textcoords="offset points", xytext=(0,10), ha='center', color='green')
        for i, (time, rsi) in enumerate(sell_signals):
            if time is not None:
                ax.annotate('Sell', (time, rsi), textcoords="offset points", xytext=(0,10), ha='center', color='red')

        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Real-Time RSI Plot')
        plt.ylabel('RSI')
        plt.xlabel('Time')
        plt.legend()

        # Display the current signal message
        if signal:
            ax.text(0.5, 0.9, f'{signal} Signal', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, color='blue', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
    except Exception as e:
        print(f"Error fetching or plotting data: {e}")

# Set up the plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update_plot, interval=300000)  # 300000 ms = 5 minutes

plt.show()

