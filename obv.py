import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np

# Function to generate simulated stock data
def generate_stock_data(symbol, start_price, num_minutes=30*24*60):
    start_time = datetime.now() - timedelta(days=30)
    current_price = start_price
    stock_data = []

    for i in range(num_minutes):
        open_price = current_price
        high_price = open_price + random.uniform(0, 0.2)
        low_price = open_price - random.uniform(0, 0.2)
        close_price = random.uniform(low_price, high_price)
        volume = random.randint(1, 10)
        current_price = close_price
        timestamp = start_time + timedelta(minutes=i)
        stock_data.append({
            "timestamp": timestamp,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume
        })
    
    return stock_data

# Function to calculate OBV
def calculate_obv(df):
    obv = [0]

    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i-1]:
            obv.append(obv[-1] + df['volume'].iloc[i])
        elif df['close'].iloc[i] < df['close'].iloc[i-1]:
            obv.append(obv[-1] - df['volume'].iloc[i])
        else:
            obv.append(obv[-1])
    
    df['OBV'] = pd.Series(obv, index=df.index)
    return df

# Function to calculate OBV strategy
def calculate_obv_strategy(df, obv_ma_period=20):
    avg = df['OBV'].ewm(span=20).mean()
    df['Buy_signal'] = np.nan
    df['Sell_signal'] = np.nan

    for i in range(1, len(df)):
        if df['OBV'].iloc[i] > avg.iloc[i] and df['OBV'].iloc[i-1] <= avg.iloc[i-1]:
            df.loc[df.index[i], 'Buy_signal'] = df['close'].iloc[i]
        elif df['OBV'].iloc[i] < avg.iloc[i] and df['OBV'].iloc[i-1] >= avg.iloc[i-1]:
            df.loc[df.index[i], 'Sell_signal'] = df['close'].iloc[i]
    
    return df

# Function to update the plot
def update_plot(frame):
    global df, times
    current_time = datetime.now().strftime('%H:%M:%S')
    final = df['close'].iloc[-1]
    new_stock_data = generate_stock_data('AAPL', final, num_minutes=1)
    new_stock_data = pd.DataFrame(new_stock_data)[['timestamp', 'close', 'volume']].set_index('timestamp')

    df = pd.concat([df, new_stock_data])
    df = calculate_obv(df)
    df = calculate_obv_strategy(df)
    
    if len(times) >= 60:
        times = times[-59:] + [current_time]
    else:
        times.append(current_time)
    
    obv = df['OBV'][-60:].to_numpy()

    ax.clear()
    ax.plot(times, obv, label='OBV')
    ax.set_xticklabels(times, rotation=45, ha='right')
    ax.set_title("Real-Time OBV Plot")
    ax.set_ylabel("OBV")
    ax.set_xlabel("Time")
    ax.legend()

    buy = df['Buy_signal'].iloc[-1]
    sell = df['Sell_signal'].iloc[-1]

    if not pd.isna(buy):
        ax.annotate('Buy', (times[-1], obv[-1]), textcoords="offset points", xytext=(0,10), ha='center', color='green')
    
    if not pd.isna(sell):
        ax.annotate('Sell', (times[-1], obv[-1]), textcoords="offset points", xytext=(0,10), ha='center', color='red')

# Initial data generation
stocks = generate_stock_data("AAPL", 200)
df = pd.DataFrame(stocks).set_index('timestamp')
df = calculate_obv(df)
df = calculate_obv_strategy(df)

# Plot setup
fig, ax = plt.subplots()
times = list(df.index.strftime('%H:%M:%S'))

# Animation setup
ani = FuncAnimation(fig, update_plot, interval=1000, cache_frame_data=False)

plt.show()