import requests
import pandas as pd
import time

# Replace with your Alpha Vantage API key
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
STOCK_SYMBOL = 'AAPL'
INTERVAL = '5min'

def fetch_data(symbol, interval, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def parse_data(data):
    time_series = data[f'Time Series ({INTERVAL})']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df = df.astype(float)
    df = df.rename(columns={"4. close": "close"})
    return df

data = fetch_data(STOCK_SYMBOL, INTERVAL, API_KEY)
stocks = parse_data(data)
print(stocks.head())


def calculate_sma(prices, period):
    if len(prices) < period:
        raise ValueError("Not enough data points to calculate SMA")
    sma = sum(prices) / period
    return [sma]

def calculate_ema(prices, period):
    if len(prices) < 2 * period:
        raise ValueError("Prices length must be at least twice the period")
    
    emas = []
    round_precision = detect_precision(prices[0])
    
    # First EMA value = SMA value
    sma = calculate_sma(prices[:period], period)
    previous_ema = sma[0]
    emas.append(round_float(previous_ema, round_precision))
    
    # Smoothing factor
    alpha = 2 / (1 + period)
    for p in prices[period:]:
        previous_ema = emas[-1]
        ema = (p * alpha) + (previous_ema * (1 - alpha))
        emas.append(round_float(ema, round_precision))
    
    return emas

def generate_signals(prices, short_period, long_period):
    short_ema = calculate_ema(prices, short_period)
    long_ema = calculate_ema(prices, long_period)
    
    signals = []
    
    for i in range(len(long_ema)):
        if i == 0:
            signals.append(0)  # No signal on the first day
        else:
            if short_ema[i] > long_ema[i] and short_ema[i-1] <= long_ema[i-1]:
                signals.append(1)  # Buy signal
            elif short_ema[i] < long_ema[i] and short_ema[i-1] >= long_ema[i-1]:
                signals.append(-1)  # Sell signal
            else:
                signals.append(0)  # No signal
    
    return signals

def detect_precision(value):
    if isinstance(value, float):
        decimal_part = str(value).split('.')[1]
        return len(decimal_part)
    return 0

def round_float(value, precision):
    return round(value, precision)

# Get closing prices
prices = stocks['close'].to_numpy()
short_period = 12
long_period = 26

# Generate signals
signals = generate_signals(prices, short_period, long_period)

# Append signals to the DataFrame
stocks['short_ema'] = calculate_ema(prices, short_period)[len(prices) - len(signals):]
stocks['long_ema'] = calculate_ema(prices, long_period)
stocks['signal'] = signals

print(stocks)

import alpaca_trade_api as tradeapi

# Replace with your Alpaca API key and secret
APCA_API_KEY_ID = 'YOUR_ALPACA_API_KEY_ID'
APCA_API_SECRET_KEY = 'YOUR_ALPACA_API_SECRET_KEY'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

def execute_trade(signal, symbol):
    if signal == 1:  # Buy signal
        api.submit_order(
            symbol=symbol,
            qty=1,  # Number of shares to buy
            side='buy',
            type='market',
            time_in_force='gtc'
        )
    elif signal == -1:  # Sell signal
        api.submit_order(
            symbol=symbol,
            qty=1,  # Number of shares to sell
            side='sell',
            type='market',
            time_in_force='gtc'
        )

# Iterate through signals and execute trades
for i in range(len(stocks)):
    if stocks['signal'][i] == 1 or stocks['signal'][i] == -1:
        execute_trade(stocks['signal'][i], STOCK_SYMBOL)
        time.sleep(1)  # To avoid hitting the rate limit


# Setup initial variables
short_period = 12  # 12 intervals of 5 minutes each (60 minutes)
long_period = 26   # 26 intervals of 5 minutes each (130 minutes)

# Create the figure and axes
fig, ax = plt.subplots()

# Function to update the plot
def update(frame):
    global stocks, API_KEY, STOCK_SYMBOL, INTERVAL
    data = fetch_data(STOCK_SYMBOL, INTERVAL, API_KEY)
    stocks = parse_data(data)
    prices = stocks['close'].to_numpy()

    # Calculate EMAs and generate signals
    short_ema, long_ema, signals = generate_signals(prices, short_period, long_period)

    # Clear the previous plot
    ax.clear()

    # Plot the closing prices
    ax.plot(stocks.index, stocks['close'], label='Close Price', color='blue')

    # Plot the EMAs
    ax.plot(stocks.index[len(stocks) - len(short_ema):], short_ema, label=f'Short EMA ({short_period})', color='green')
    ax.plot(stocks.index[len(stocks) - len(long_ema):], long_ema, label=f'Long EMA ({long_period})', color='red')

    # Plot buy/sell signals
    for i, signal in enumerate(signals):
        if signal == 1:
            ax.plot(stocks.index[len(stocks) - len(signals) + i], prices[len(prices) - len(signals) + i], marker='^', color='green', markersize=10, label='Buy Signal' if i == 0 else "")
        elif signal == -1:
            ax.plot(stocks.index[len(stocks) - len(signals) + i], prices[len(prices) - len(signals) + i], marker='v', color='red', markersize=10, label='Sell Signal' if i == 0 else "")

    # Set titles and labels
    ax.set_title('Stock Price and EMA Buy/Sell Signals')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.legend()

# Create the animation
ani = animation.FuncAnimation(fig, update, interval=300000)  # Update every 5 minutes (300000 ms)

# Display the plot
plt.show()

