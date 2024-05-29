import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta
import pandas as pd
import random

# Initialize lists to store time and RSI values
times = []
rsi_values = []
buy_signals = []
sell_signals = []

# Function to generate stock data for 30 days (assuming 1 data point per minute)
def generate_stock_data(symbol, start_price, num_minutes=30*24*60):
    stock_data = []
    current_price = start_price
    start_time = datetime.now() - timedelta(days=30)

    for i in range(num_minutes):  # 30 days of minute-by-minute data
        open_price = current_price
        high_price = open_price + random.uniform(0, 0.2)
        low_price = open_price - random.uniform(0, 0.2)
        close_price = random.uniform(low_price, high_price)
        volume = random.randint(1, 10)
        current_price = close_price

        timestamp = start_time + timedelta(minutes=i)

        stock_data.append({
            'timestamp': timestamp,
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })

    return stock_data

# Function to fetch RSI
def fetch_rsi(stock_data):
    data = pd.DataFrame(stock_data)
    data.set_index('timestamp', inplace=True)

    # Calculate RSI using pandas (example using close price)
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Return the latest RSI value and full RSI series
    return rsi.iloc[-1], rsi

# Generate initial stock data
initial_stock_data = generate_stock_data('AAPL', 150)

# Function to update the plot
def update_plot(frame):
    current_time = datetime.now().strftime('%H:%M:%S')
    try:
        # Simulate receiving new stock data point
        new_stock_data = generate_stock_data('AAPL', initial_stock_data[-1]['close'], num_minutes=1)
        initial_stock_data.extend(new_stock_data)
        
        latest_rsi, full_rsi = fetch_rsi(initial_stock_data)
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
