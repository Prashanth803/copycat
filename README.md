Import matplotlib.pyplot

Import matplotlib.ant

from natplotlib.backeновский

fron datetime Import daterter,

Import pandas as pd

Import randon

Inport tkinter as 1

Import numpy as np

for i in range(num minutes): 30 days of minute-by-minute data

py

times-[]

11 obv[]

12 buy signals-()

sell signals-[]

15 stock data[] 14

def generate stock data(symbol, start price, nus minutes-30*24*60):

16

17

start time datetime.now() timedelta(days-39)

current price start price

16

19

20

21

23

21

24

25

26

27

28

29

38

TE

32

33

14

35

16

37

30

30

open_price current_price

high price open_price random.uniform(0, 0.2)

low price open price random.uniform(0, 0.2)

close price random.uniform(low_price, high price)

volume random.randint(1, 10)

current price close_price

timestamp - start time tinedelta(minutes-1)

stock_data.append

timestamp": timestamp,

"open" round(open_price, 2),

'high': round (high_price, 2),

'low': round(low_price, 2).

'close': round(close_price, 2),

volume: volume

return stock data

40 def calculate_obv(df):

41

42

41

45

46

47

40

49

Calculate the on-Balance Volume (OBV) for a given DataFrame.

obv.append(0)

#Loop through the DataFrame from the second row

for i in range(1, len(df)):

if df['close'].iloc[1] > df ['close'].iloc[11]:

obv.append(obv[-1] + df['volume'].iloc[i])

elif dff close 1.Ilocfil < dff close 1.1locfi - 11:
]

cbv.append(obv-3)

else: cbv.append(obv(-1))

df[V] pd.Series(abv, index-of. Index)

return of

47

49

52

14

50

17 def calculate_obv_strategy(df, obv_na_period-20):

60

Implement a simple 0BV strategy: Buy when OBV crosses above its moving average. and sell when CEV crosses below its moving average.

Parameters:

df (pd.DataFrame): DataFrane with "Close", "Volume', and '08V' columns. obv_ma_period (Int): The period for the OBV moving average.

Returns:

pd.DataFrame: DataFrase with 'Buy Signal' and 'Sell Signal columns added.

Calculate the CBV moving average

avgdf['cev'].rolling(window-obv_ma_period).mean()

df[ Buy Signal"]-np.nan

df["Sell Signal"]-rp.nan

Generate Buy/Sell signals

for i in range(1, len(df)):

if df[08V].iloc[1]> avg.iloc[1] and df['0BV"].iloc[11] df.loc[df.index[1], 'Buy_signal"]-df['close'].iloc[1] avg.iloc[1]:

elif df[ev'].iloc[i] < avg.iloc[1] and df['OBV'].iloc[11] df.loc[df.index[1], 'Sell_Signal'] df['close'].iloc[1] avg.iloc[1]:

return of

def update plot(frame):

current time datetime.now().strftime('SH:35')

final-df[-1]['close']

new stock data generate stock_data(AAPL, final,mum minutes-1)

new_stock_data-new_stock_data[['close', 'volume"]]

df-calculate_obv(df)

df-calculate_obv_strategy(df)

abv-df[08V'].to_numpy()

times.append(current_time)

If len(times) > 60:

ax.setxlin(len(times)-20, len(tines))
ax.clear() ax.plot(times,obv, label-RS!)

ax.set xticklabels(times, rotation-as, ha-'right')

ax.set sticks (range(len(times)))

ax.set title("Real-Time OBV Plot)

ax.set ylabel(OBV)

ax. set xlabel(Time')

ax.legend()

buy-dff Buy Signal'].1loc(-1)

sell-df Sell Signal ].iloc(-1)

ax. annotate(luy, (times(-1),obu[-1]), textcoords="offset points", xytext-(6,10), ha- center", color-'green')

if selle:

1f buyer

ax.annotate(Sell, (times[-1],obv[-1]), rextcoords="offset points", xytext-(0,10), ha='center', color="green")

simulate receiving new stock date paint

#except Exception as

print("Error fetching or plotting datar (e)")

stocks-generate stock_data("Mishra",200)

2 global of

df-pd.DataFrame (stocks)

df.set Index('timestamp', inplace-True)

df-calculate obv (df)

df-calculate_obv_strategy (df)

fig, axplt.subplots()

and unimation, FuncAnimation(fig, update plot, interval-1000)

plt.show()

