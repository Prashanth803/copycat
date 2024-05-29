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

- **Interactive Plotting**: Using `Tkinter` and `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg`, you can create an interactive plotting environment that supports scrolling.
- **Dynamic Limits**: By dynamically adjusting the x-axis limits (`ax.set_xlim`), the plot can give the appearance of scrolling as new data points are added.
- **Real-Time Updates**: The `animation.FuncAnimation` function allows for real-time updates, making it ideal for live data plotting.

This approach combines the power of `matplotlib` for plotting with `Tkinter` for creating an interactive user interface, allowing for a seamless scrolling experience in a real-time plot.
