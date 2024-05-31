from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np
import schedule
import os

def append_to_csv(df, file_path):
    mode = 'w' if not os.path.isfile(file_path) else 'a'
    df.to_csv(file_path, mode=mode, header=mode=='w', index=False)
    print("Data appended successfully to", file_path)

def generate_stock_data(symbol, start_price, num_minutes=30*24*60):
    stock_data = []
    current_price = start_price
    start_time = datetime.now()

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


def round_float(value, precision):
    return round(value, precision)

def detect_precision(value):
    # This function is a placeholder to match the precision detection in Go.
    # You may need to adjust this based on how you want to determine precision.
    if isinstance(value, float):
        decimal_part = str(value).split('.')[1]
        return len(decimal_part)
    return 0

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
    
    k = 2 / (1 + period)
    for p in prices[period:]:       #formula=EMA = (current or close price * multiplier) + [EMA previous * (1- multiplier)]    Multiplier = 2/(N-1)
        previous_ema = emas[-1]
        ema = (p * k) + (previous_ema * (1 - k))
        emas.append(round_float(ema, round_precision))
    
    return emas

def group(frame,close):
    new_stock_data = generate_stock_data("Mishra", close, frame)
    new_stock_data=pd.DataFrame(new_stock_data)
    stocks=pd.concat([stocks,new_stock_data],ignore_index=False)
    ema=calculate_ema(stocks,frame)
    if(ema>len(new_stock_data)):
        new_stock_data['EMA']=[0.0]*(len(new_stock_data)-len(ema))+ema[-len(new_stock_data):]
        append_to_csv(new_stock_data, 'ema.csv')
    else:
        print("No data appended")
# Initialize close price
global close
close = 200
# Create an empty DataFrame to hold stock data
stocks = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Schedule the group function
schedule.every(1).minutes.do(group, 5, close)

# Run scheduled tasks until future_time is reached
current_time = datetime.now()
future_time = current_time + timedelta(hours=24)
while datetime.now() < future_time:
    schedule.run_pending()


