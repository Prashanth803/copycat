To handle the computation of indicators for 200 stocks with minimal lag, you should design your backend to efficiently manage data reception, indicator calculation, and data delivery. Here's a step-by-step approach to achieve this:

1. **Data Reception**:
   - Use a message queue or streaming service (e.g., Kafka, RabbitMQ) to receive stock data in real-time.
   - Implement a data ingestion service to listen to the queue and process incoming data.

2. **Data Storage**:
   - Temporarily store the incoming data in an in-memory data store (e.g., Redis) to ensure fast read/write access.
   - Organize the data by stock and time intervals for efficient retrieval.

3. **Indicator Calculation**:
   - Use concurrent processing to calculate indicators for multiple stocks simultaneously. Python's `concurrent.futures` with ThreadPoolExecutor or ProcessPoolExecutor can be helpful.
   - Each indicator calculation should be encapsulated in its class. Create instances of these classes as needed and pass the relevant data to them.

4. **Combining Indicator Calculations**:
   - Create a master function that retrieves data for each stock, initializes indicator classes, and computes the required indicators.
   - Aggregate the results and prepare them for delivery.

5. **Data Delivery**:
   - Use a fast communication protocol like WebSocket or gRPC to deliver the computed indicator values back to the client in real-time.

Here’s a basic outline of how you can structure your code:

### Data Reception Service

```python
import redis
import json

class DataReceiver:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def listen_to_queue(self, queue_name):
        while True:
            message = self.redis_client.blpop(queue_name)
            if message:
                stock_data = json.loads(message[1])
                self.store_data(stock_data)

    def store_data(self, stock_data):
        # Store the stock data in Redis
        stock_id = stock_data['stock_id']
        timestamp = stock_data['timestamp']
        self.redis_client.hset(f'stock:{stock_id}', timestamp, json.dumps(stock_data))
```

### Indicator Calculation

```python
from concurrent.futures import ThreadPoolExecutor
import redis

class IndicatorCalculator:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    def calculate_indicators(self, stock_id, indicators):
        stock_data = self.retrieve_data(stock_id)
        results = {}
        
        with ThreadPoolExecutor(max_workers=len(indicators)) as executor:
            future_to_indicator = {executor.submit(indicator.calculate, stock_data): indicator for indicator in indicators}
            for future in concurrent.futures.as_completed(future_to_indicator):
                indicator = future_to_indicator[future]
                results[indicator.name] = future.result()
        
        return results

    def retrieve_data(self, stock_id):
        data = self.redis_client.hgetall(f'stock:{stock_id}')
        return [json.loads(data[timestamp]) for timestamp in sorted(data.keys())]
```

### Indicator Classes

```python
class MovingAverage:
    def __init__(self, window):
        self.window = window
        self.name = 'moving_average'

    def calculate(self, data):
        # Implementation of moving average calculation
        return moving_average_value

class RSI:
    def __init__(self, period):
        self.period = period
        self.name = 'rsi'

    def calculate(self, data):
        # Implementation of RSI calculation
        return rsi_value

# Add more indicator classes as needed
```

### Data Delivery Service

```python
import asyncio
import websockets

class DataDelivery:
    async def send_data(self, websocket, path):
        stock_id = await websocket.recv()
        indicator_calculator = IndicatorCalculator()
        indicators = [MovingAverage(20), RSI(14)]  # Add other indicator instances
        results = indicator_calculator.calculate_indicators(stock_id, indicators)
        await websocket.send(json.dumps(results))

    def start_server(self):
        server = websockets.serve(self.send_data, 'localhost', 6789)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
```

### Putting It All Together

1. **Start the Data Reception Service**:
   ```python
   receiver = DataReceiver()
   receiver.listen_to_queue('stock_data_queue')
   ```

2. **Start the Data Delivery Service**:
   ```python
   delivery = DataDelivery()
   delivery.start_server()
   ```

This architecture allows you to receive stock data, store it efficiently, calculate multiple indicators concurrently, and deliver the results in real-time. Adjust the specifics based on your actual data structures, indicator algorithms, and deployment environment.
