Using microservices to merge different Python files, each containing an indicator calculation, is a modern approach to designing modular and scalable applications. You don't necessarily have to create a class for each indicator, but doing so can encapsulate the functionality and make your code more organized and maintainable. Here’s a step-by-step guide on how you can achieve this:

### Step 1: Structure Your Python Files

Assume you have separate Python files for each indicator, e.g., `rsi.py`, `ema.py`, and `obv.py`. Each file should ideally contain a function or a class to calculate the respective indicator.

#### Example: `rsi.py`
```python
class RSI:
    def __init__(self, period=14):
        self.period = period

    def calculate(self, prices):
        # RSI calculation logic
        pass
```

#### Example: `ema.py`
```python
class EMA:
    def __init__(self, period=14):
        self.period = period

    def calculate(self, prices):
        # EMA calculation logic
        pass
```

#### Example: `obv.py`
```python
class OBV:
    def __init__(self):
        pass

    def calculate(self, prices, volumes):
        # OBV calculation logic
        pass
```

### Step 2: Create a Microservice for Each Indicator

Using a web framework like Flask, you can create microservices for each indicator. Here’s an example for each:

#### Example: `rsi_service.py`
```python
from flask import Flask, request, jsonify
from rsi import RSI

app = Flask(__name__)
rsi = RSI()

@app.route('/rsi', methods=['POST'])
def calculate_rsi():
    data = request.get_json()
    prices = data['prices']
    period = data.get('period', 14)
    rsi.period = period
    result = rsi.calculate(prices)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5001)
```

#### Example: `ema_service.py`
```python
from flask import Flask, request, jsonify
from ema import EMA

app = Flask(__name__)
ema = EMA()

@app.route('/ema', methods=['POST'])
def calculate_ema():
    data = request.get_json()
    prices = data['prices']
    period = data.get('period', 14)
    ema.period = period
    result = ema.calculate(prices)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5002)
```

#### Example: `obv_service.py`
```python
from flask import Flask, request, jsonify
from obv import OBV

app = Flask(__name__)
obv = OBV()

@app.route('/obv', methods=['POST'])
def calculate_obv():
    data = request.get_json()
    prices = data['prices']
    volumes = data['volumes']
    result = obv.calculate(prices, volumes)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5003)
```

### Step 3: Create a Gateway to Merge Results

Create another Flask service that acts as a gateway to call these microservices and merge the results.

#### Example: `gateway.py`
```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/indicators', methods=['POST'])
def calculate_indicators():
    data = request.get_json()
    prices = data['prices']
    volumes = data.get('volumes', [])

    rsi_response = requests.post('http://localhost:5001/rsi', json={'prices': prices})
    ema_response = requests.post('http://localhost:5002/ema', json={'prices': prices})
    obv_response = requests.post('http://localhost:5003/obv', json={'prices': prices, 'volumes': volumes})

    result = {
        'rsi': rsi_response.json(),
        'ema': ema_response.json(),
        'obv': obv_response.json()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
```

### Running the Services

1. Start each microservice by running:
   - `python rsi_service.py`
   - `python ema_service.py`
   - `python obv_service.py`
2. Start the gateway service by running:
   - `python gateway.py`

### Summary

- **Classes for Each Indicator**: While not strictly necessary, using classes encapsulates the functionality and makes the code cleaner.
- **Microservices**: Each indicator is exposed via a microservice using Flask.
- **Gateway Service**: A central service calls each microservice and merges the results.

This setup ensures that each indicator is modular, scalable, and easy to maintain.




import requests
import json

# Define the base URL of your API
base_url = 'http://localhost:3000/api'

# Function to create a new document
def create_document(data):
    url = f"{base_url}/documents"
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Document created successfully:", response.json())
    else:
        print("Failed to create document:", response.text)

# Function to read documents
def read_documents():
    url = f"{base_url}/documents"
    response = requests.get(url)
    if response.status_code == 200:
        print("Documents retrieved successfully:", response.json())
    else:
        print("Failed to retrieve documents:", response.text)

# Function to update a document by ID
def update_document(document_id, data):
    url = f"{base_url}/documents/{document_id}"
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print("Document updated successfully:", response.json())
    else:
        print("Failed to update document:", response.text)

# Function to delete a document by ID
def delete_document(document_id):
    url = f"{base_url}/documents/{document_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Document deleted successfully:", response.json())
    else:
        print("Failed to delete document:", response.text)

# Example usage
if __name__ == "__main__":
    # Create a new document
    new_data = {
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    create_document(new_data)

    # Read documents
    read_documents()

    # Update a document
    update_data = {
        "name": "Jane Doe"
    }
    document_id = 'some_document_id'  # Replace with actual document ID
    update_document(document_id, update_data)

    # Delete a document
    delete_document(document_id)
    // server.js

const express = require('express');
const bodyParser = require('body-parser');
const Datastore = require('nedb');

const app = express();
const port = 3000;

app.use(bodyParser.json());

const db = new Datastore({ filename: 'database.db', autoload: true });

// Create a new document
app.post('/api/documents', (req, res) => {
    const doc = req.body;
    db.insert(doc, (err, newDoc) => {
        if (err) {
            res.status(500).send(err);
        } else {
            res.status(201).send(newDoc);
        }
    });
});

// Read all documents
app.get('/api/documents', (req, res) => {
    db.find({}, (err, docs) => {
        if (err) {
            res.status(500).send(err);
        } else {
            res.status(200).send(docs);
        }
    });
});

// Update a document by ID
app.put('/api/documents/:id', (req, res) => {
    const { id } = req.params;
    const updatedDoc = req.body;
    db.update({ _id: id }, { $set: updatedDoc }, {}, (err, numReplaced) => {
        if (err) {
            res.status(500).send(err);
        } else {
            res.status(200).send({ updated: numReplaced });
        }
    });
});

// Delete a document by ID
app.delete('/api/documents/:id', (req, res) => {
    const { id } = req.params;
    db.remove({ _id: id }, {}, (err, numRemoved) => {
        if (err) {
            res.status(500).send(err);
        } else {
            res.status(200).send({ removed: numRemoved });
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
OBV:

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
