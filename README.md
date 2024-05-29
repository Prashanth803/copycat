To add scrolling functionality to a graph in `matplotlib` so that previous plots are visible, you need to use a combination of a large `xlim` (x-axis limit) and `pan/zoom` functionality provided by `matplotlib`. You can also use an interactive backend like `TkAgg` which supports interactive zooming and panning. However, for smooth scrolling similar to a real-time chart, integrating with a GUI toolkit like `Tkinter` is often required.

Here’s an example demonstrating how to create a scrolling graph using `matplotlib` and `Tkinter` for a more interactive experience:

1. **Install the required libraries**:
   Make sure you have `matplotlib` and `tkinter` installed. You can install `matplotlib` using pip:
   ```sh
   pip install matplotlib
   ```

2. **Create a scrolling plot with `matplotlib` and `Tkinter`**:

```python
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk
from datetime import datetime, timedelta
import random
import pandas as pd

# Initialize lists to store time and RSI values
times = []
rsi_values = []

# Function to generate random RSI data
def generate_random_data():
    current_time = datetime.now().strftime('%H:%M:%S')
    rsi_value = random.uniform(0, 100)
    return current_time, rsi_value

# Function to update the plot
def update_plot(frame):
    current_time, rsi_value = generate_random_data()
    times.append(current_time)
    rsi_values.append(rsi_value)

    # Update plot limits to create a scrolling effect
    if len(times) > 20:
        ax.set_xlim(len(times) - 20, len(times))

    ax.clear()
    ax.plot(range(len(times)), rsi_values, label='RSI')
    ax.set_xticks(range(len(times)))
    ax.set_xticklabels(times, rotation=45, ha='right')
    ax.set_title('Real-Time RSI Plot')
    ax.set_ylabel('RSI')
    ax.set_xlabel('Time')
    ax.legend()
    fig.autofmt_xdate()

# Setup the main Tkinter window
root = Tk.Tk()
root.title("Real-Time RSI Plot")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

# Set up the animation
ani = animation.FuncAnimation(fig, update_plot, interval=3000)  # 3000 ms = 3 seconds

def _quit():
    root.quit()
    root.destroy()

button = Tk.Button(master=root, text="Quit", command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
```

### Explanation

1. **Generating Random Data**:
   - The `generate_random_data` function generates random RSI values along with current timestamps for demonstration purposes.

2. **Updating the Plot**:
   - The `update_plot` function appends new data points to `times` and `rsi_values`.
   - If the number of points exceeds 20, the x-axis limit is updated to show the last 20 points, creating a scrolling effect.
   - The plot is cleared and re-drawn each time `update_plot` is called to reflect the latest data.

3. **Tkinter Integration**:
   - The main Tkinter window is set up with a title and a canvas widget to display the `matplotlib` figure.
   - The `FigureCanvasTkAgg` class is used to embed the `matplotlib` figure in the Tkinter window.
   - A `Quit` button is added to allow the user to close the window gracefully.

4. **Animation**:
   - The `animation.FuncAnimation` function updates the plot every 3 seconds by calling `update_plot`.

### Key Points
The On-Balance Volume (OBV) indicator can be used to develop a trading strategy. A common approach is to generate buy and sell signals based on the direction of the OBV in relation to its moving average or based on its divergence with price. Below is an example of a simple trading strategy using OBV:

### Strategy Outline
1. **Buy Signal**: When OBV crosses above its moving average.
2. **Sell Signal**: When OBV crosses below its moving average.

### Implementation in Python

We'll first calculate the OBV, then compute a moving average of the OBV, and finally implement the buy/sell strategy.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_obv(df):
    """
    Calculate the On-Balance Volume (OBV) for a given DataFrame.
    """
    obv = [0]  # Initialize OBV with the initial volume

    # Loop through the DataFrame from the second row
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i - 1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i - 1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])

    df['OBV'] = pd.Series(obv, index=df.index)
    return df

def calculate_obv_strategy(df, obv_ma_period=20):
    """
    Implement a simple OBV strategy: Buy when OBV crosses above its moving average,
    and sell when OBV crosses below its moving average.
    
    Parameters:
    df (pd.DataFrame): DataFrame with 'Close', 'Volume', and 'OBV' columns.
    obv_ma_period (int): The period for the OBV moving average.
    
    Returns:
    pd.DataFrame: DataFrame with 'Buy_Signal' and 'Sell_Signal' columns added.
    """
    # Calculate the OBV moving average
    df['OBV_MA'] = df['OBV'].rolling(window=obv_ma_period).mean()
    
    # Initialize signal columns
    df['Buy_Signal'] = np.nan
    df['Sell_Signal'] = np.nan
    
    # Generate Buy/Sell signals
    for i in range(1, len(df)):
        if df['OBV'].iloc[i] > df['OBV_MA'].iloc[i] and df['OBV'].iloc[i - 1] <= df['OBV_MA'].iloc[i - 1]:
            df['Buy_Signal'].iloc[i] = df['Close'].iloc[i]
        elif df['OBV'].iloc[i] < df['OBV_MA'].iloc[i] and df['OBV'].iloc[i - 1] >= df['OBV_MA'].iloc[i - 1]:
            df['Sell_Signal'].iloc[i] = df['Close'].iloc[i]
    
    return df

# Example usage
data = {
    'Close': [10, 11, 12, 11, 10, 11, 12, 13, 12, 11, 10, 9, 8, 9, 10, 11, 12, 11, 10, 9],
    'Volume': [1000, 1200, 1100, 1500, 1300, 1600, 1700, 1800, 1400, 1500, 1600, 1300, 1200, 1100, 1000, 900, 800, 700, 600, 500]
}
df = pd.DataFrame(data)

# Calculate OBV
df = calculate_obv(df)

# Apply OBV strategy
df = calculate_obv_strategy(df)

# Plot the results
plt.figure(figsize=(12, 8))

# Plot Close price and buy/sell signals
plt.subplot(2, 1, 1)
plt.plot(df['Close'], label='Close Price', color='black')
plt.scatter(df.index, df['Buy_Signal'], label='Buy Signal', marker='^', color='green', alpha=1)
plt.scatter(df.index, df['Sell_Signal'], label='Sell Signal', marker='v', color='red', alpha=1)
plt.title('Close Price and Buy/Sell Signals')
plt.legend()

# Plot OBV and its moving average
plt.subplot(2, 1, 2)
plt.plot(df['OBV'], label='OBV', color='blue')
plt.plot(df['OBV_MA'], label='OBV Moving Average', color='orange')
plt.title('OBV and OBV Moving Average')
plt.legend()

plt.tight_layout()
plt.show()
```

### Explanation

1. **Calculate OBV**: The `calculate_obv` function calculates the On-Balance Volume for each row in the DataFrame.

2. **Calculate OBV Strategy**:
   - `calculate_obv_strategy` function calculates the moving average of the OBV.
   - It generates buy signals when the OBV crosses above its moving average.
   - It generates sell signals when the OBV crosses below its moving average.

3. **Plotting the Results**:
   - The first subplot shows the closing prices with buy (green arrows) and sell (red arrows) signals.
   - The second subplot shows the OBV and its moving average.

### Adjusting Parameters

- **OBV Moving Average Period**: You can adjust the `obv_ma_period` parameter in the `calculate_obv_strategy` function to change the sensitivity of the strategy.
- **Buy/Sell Logic**: The logic for buy and sell signals can be adjusted to fit specific trading strategies or conditions.

This implementation demonstrates how to use the OBV indicator for a simple trading strategy and visualize the results with `matplotlib`. Adjusting the parameters and logic can help fine-tune the strategy to better match the characteristics of the stock being analyzed.
- **Interactive Plotting**: Using `Tkinter` and `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`, you can create an interactive plotting environment that supports scrolling.
- **Dynamic Limits**: By dynamically adjusting the x-axis limits (`ax.set_xlim`), the plot can give the appearance of scrolling as new data points are added.
- **Real-Time Updates**: The `animation.FuncAnimation` function allows for real-time updates, making it ideal for live data plotting.

This approach combines the power of `matplotlib` for plotting with `Tkinter` for creating an interactive user interface, allowing for a seamless scrolling experience in a real-time plot.
