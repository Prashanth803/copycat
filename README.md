import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import json
import pandas as pd
from process import Indicator
from engine import AnalysisEngine
from minordb.db_controller import DBController

# Database Controller Initialization
dbController = DBController()

def fetch_data(topic):
    prev_data = dbController.findStockDataByCompanyId(topic)
    new_stock = pd.DataFrame(columns=['companyId', 'frame', 'open', 'close', 'high', 'low', 'volume', 'timestamp',
                                      'UpperBand', 'LowerBand', 'MACD', 'MACD_Signal', 'MACD_Hist', 'vwap', 'rsi',
                                      'obv', 'ema_5', 'ema_13', 'ema_26', 'supertrend'])
    if len(prev_data) == 0:
        return new_stock

    for _dict in prev_data:
        data = pd.DataFrame([_dict])
        data = data[['companyId', 'frame', 'open', 'close', 'high', 'low', 'volume', 'timestamp', 'UpperBand', 'LowerBand',
                     'MACD', 'MACD_Signal', 'MACD_Hist', 'vwap', 'rsi', 'obv', 'ema_5', 'ema_13', 'ema_26', 'supertrend']]
        data.dropna(axis=1, how="all", inplace=True)
        new_stock = pd.concat([new_stock, data], ignore_index=True)

    return new_stock

def add_message_to_dataframe(topic, message):
    new_stock = fetch_data(topic)
    new_stock.dropna(axis=1, how="all", inplace=True)
    new_stock = pd.concat([new_stock, message], ignore_index=True)

    indicator = Indicator(new_stock)
    results = indicator.process_data()

    new_data = new_stock.iloc[-1].copy()
    new_data['UpperBand'] = results[0][0]
    new_data['LowerBand'] = results[0][1]
    new_data['MACD'] = results[1][0]
    new_data['MACD_Signal'] = results[1][1]
    new_data['MACD_Hist'] = results[1][2]
    new_data['vwap'] = results[2]
    new_data['rsi'] = results[3]
    new_data['obv'] = results[4]
    new_data['ema_5'] = results[5][0]
    new_data['ema_13'] = results[5][1]
    new_data['ema_26'] = results[5][2]
    new_data['supertrend'] = results[6]

    return new_data

def process_message(msg, topic):
    topic = str(topic)
    df_po = pd.DataFrame([msg])
    new_data = add_message_to_dataframe(topic, df_po)
    new_data = new_data.to_frame().T

    stock = fetch_data(topic)
    stock.dropna(axis=1, how="all", inplace=True)
    stock = pd.concat([stock, new_data], ignore_index=True)

    AnalysisEngine(stock)

    result_dict = (stock.iloc[-1]).to_dict()
    res = dbController.insertStockData(result_dict)
    print(res)
    return stock.iloc[-1]

async def process_partition_messages(topic, message_queue, lock, executor):
    loop = asyncio.get_running_loop()
    while True:
        message = await message_queue.get()
        if message is None:
            break
        try:
            result = await loop.run_in_executor(executor, process_message, message, topic)
            message_queue.task_done()
            return result
        except asyncio.CancelledError:
            print("Task cancelled")
            break

class EngineServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.partition_locks = defaultdict(asyncio.Lock)
        self.partition_queues = defaultdict(asyncio.Queue)
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def handle_request(self, reader, writer):
        try:
            # Read data from client
            message = await reader.read(1024)
            data = message.decode()

            # Parse JSON data
            msg = json.loads(data)
            jon = pd.DataFrame([msg])

            part = str(jon['frame'].iloc[0])
            topic = str(jon['companyId'].iloc[0])

            lock = self.partition_locks[topic]
            queue = self.partition_queues[topic]

            await queue.put(msg)

            res = asyncio.create_task(process_partition_messages(topic, queue, lock, self.executor))
            result = await res

            result_json = result.to_json()
            result_str = str(result_json)

            print(result_str)
            writer.write(result_str.encode())
            await writer.drain()
        except Exception as e:
            response = f"Error: {str(e)}"
            writer.write(response.encode())
            await writer.drain()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_request, self.host, self.port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Server is running at {addrs}')
        async with server:
            await server.serve_forever()

async def main():
    server = EngineServer('localhost', 12345)
    await server.start_server()

if __name__ == "__main__":
    print(dbController.setup("./databases/stock.db", 35))
    asyncio.run(main())




const net = require('net');

// Create a TCP server
const server = net.createServer((socket) => {
    console.log('Client connected');

    // Handle incoming data from the client
    socket.on('data', (data) => {
        console.log(`Received data: ${data}`);
        
        // Send a response back to the client
        socket.write('Hello from the server!\n');
    });

    // Handle client disconnection
    socket.on('end', () => {
        console.log('Client disconnected');
    });

    // Handle errors
    socket.on('error', (err) => {
        console.error(`Socket error: ${err}`);
    });
});

// Make the server listen on port 1234
const PORT = 1234;
server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});




The round-robin partitioning strategy in Kafka affects producers, which determine how messages are distributed across partitions within a single topic. However, the presence of multiple consumers on different topics impacts the overall system differently. Here’s a detailed look at how the round-robin partitioner and multiple consumers on different topics interact and affect each other:

### Round-Robin Partitioning and Its Impact

1. **Balanced Load Distribution**:
   - **Producers**: When a producer uses the round-robin partitioner, it ensures that messages are evenly distributed across all partitions of a topic. This can help prevent any single partition from becoming a bottleneck.
   - **Impact on Consumers**: If consumers are reading from these partitions, they can benefit from a more evenly distributed load, assuming there is a consumer for each partition. This balance can improve overall throughput and latency.

2. **Consumer Group Dynamics**:
   - **Single Topic**: If all consumers are part of the same consumer group and subscribe to the same topic, Kafka ensures that each partition is consumed by only one consumer in the group. With round-robin partitioning, the work is evenly divided among the consumers, provided they are properly balanced.
   - **Multiple Topics**: When there are multiple consumers across different topics, each consumer group independently manages its own partitions. Round-robin partitioning on a producer side affects how messages are distributed within individual topics but does not directly affect other topics.

### Multiple Consumers on Different Topics

When you have multiple consumers subscribed to different topics, several factors come into play:

1. **Resource Utilization**:
   - **CPU and Memory**: Each consumer consumes resources on the Kafka brokers and on the consumers’ own machines. If these consumers are spread across different topics, they might contend for CPU, memory, and network bandwidth.
   - **Disk I/O**: Kafka brokers manage logs for different topics. If multiple topics are heavily accessed, this can lead to increased disk I/O, potentially impacting performance.

2. **Network Throughput**: With multiple consumers, the network throughput can become a limiting factor. Consumers pulling data from different topics need sufficient network bandwidth to ensure timely processing of messages.

3. **Consumer Lag**:
   - **Balancing Consumers**: With well-balanced partitions and consumer groups, consumer lag can be minimized. However, if some partitions receive more messages due to round-robin distribution, while other topics are less busy, it can lead to imbalances in consumer processing rates.

### Optimizing Performance

To optimize performance and ensure efficient handling of multiple consumers on different topics, consider the following strategies:

1. **Monitor and Balance Load**:
   - Regularly monitor the load on each partition and consumer group. Ensure that partitions are evenly distributed among consumers to prevent lag.
   - Use Kafka’s metrics to keep track of consumer lag, throughput, and other important performance indicators.

2. **Increase Partitions and Consumers**:
   - If some consumers are under heavy load, consider increasing the number of partitions for those topics. This allows the load to be distributed across more consumers.
   - Add more consumers to consumer groups to handle increased load efficiently.

3. **Resource Allocation**:
   - Allocate sufficient resources (CPU, memory, network bandwidth) to your Kafka brokers and consumer machines to handle the expected load.
   - Use dedicated machines or clusters for Kafka brokers to avoid resource contention with other applications.

4. **Consumer Configuration**:
   - Tune consumer configurations such as `fetch.min.bytes`, `fetch.max.wait.ms`, and `max.partition.fetch.bytes` to optimize how consumers pull data from Kafka.
   - Ensure that consumers can process messages quickly to keep up with the rate at which producers are sending them.

### Conclusion

The round-robin partitioner ensures balanced message distribution within a topic, which generally helps in evenly spreading the load across partitions. When there are multiple consumers on different topics, the key is to monitor resource utilization, ensure balanced consumer groups, and allocate sufficient resources. Proper configuration and scaling of partitions and consumers can help maintain optimal performance in a Kafka cluster with multiple topics and consumer groups.



Polling messages in `AIOKafkaConsumer` can be achieved using the `getmany` method, which allows you to fetch multiple messages from different partitions in a single call. This can be more efficient than processing messages one by one, especially when dealing with high-throughput scenarios.

Here is how you can modify the code to use `getmany` for polling messages:

### Updated Code to Poll Messages

```python
import asyncio
from aiokafka import AIOKafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from process import Indicator
from engine import Analysisengine

# Configuration for the Kafka consumer
KAFKA_BOOTSTRAP_SERVERS = 'your_bootstrap_servers'
KAFKA_TOPICS = ['your_topic1', 'your_topic2']  # List your topics here
KAFKA_GROUP_ID = 'your_group_id'
POLL_TIMEOUT_MS = 1000  # Poll timeout in milliseconds

def process_message(message):
    print(f"Partition {message.partition}, Topic {message.topic}: {message.value.decode('utf-8')}")
    # You can use Indicator, Analysisengine, or any other processing logic here

async def process_partition_messages(partition, message_queue, executor):
    loop = asyncio.get_event_loop()
    while True:
        message = await message_queue.get()
        if message is None:  # Shutdown signal
            break
        await loop.run_in_executor(executor, process_message, message)
        message_queue.task_done()

async def start_consumer():
    consumer = AIOKafkaConsumer(
        *KAFKA_TOPICS,  # Unpack the list of topics
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        enable_auto_commit=False
    )

    await consumer.start()
    try:
        partition_queues = defaultdict(asyncio.Queue)
        partition_tasks = {}
        executor = ThreadPoolExecutor(max_workers=10)  # Adjust the number of workers as needed

        while True:
            # Poll messages from Kafka
            messages = await consumer.getmany(timeout_ms=POLL_TIMEOUT_MS)
            for tp, msgs in messages.items():
                partition = tp.partition
                if partition not in partition_tasks:
                    queue = partition_queues[partition]
                    task = asyncio.create_task(process_partition_messages(partition, queue, executor))
                    partition_tasks[partition] = task

                for msg in msgs:
                    await partition_queues[partition].put(msg)
    finally:
        for partition, task in partition_tasks.items():
            await partition_queues[partition].put(None)
            await task

        await consumer.stop()
        executor.shutdown(wait=True)

if __name__ == '__main__':
    asyncio.run(start_consumer())
```

### Key Changes for Polling Messages:

1. **POLL_TIMEOUT_MS**:
   - Added a `POLL_TIMEOUT_MS` constant to define the timeout for polling messages.

2. **Using `getmany`**:
   - Replaced the `async for msg in consumer` loop with a `while True` loop that calls `consumer.getmany(timeout_ms=POLL_TIMEOUT_MS)`.
   - `getmany` returns a dictionary where the keys are `TopicPartition` objects and the values are lists of messages. This allows you to handle messages from multiple partitions efficiently.

3. **Processing Polled Messages**:
   - Loop through the dictionary returned by `getmany` and process messages from each partition.
   - Ensure each message is put into the corresponding partition queue.

### Explanation:

- **Polling Messages**: The `consumer.getmany(timeout_ms=POLL_TIMEOUT_MS)` method is used to poll messages. It fetches messages from multiple partitions and returns them as a dictionary.
- **Handling Polled Messages**: The loop iterates over the dictionary, retrieves messages for each partition, and puts them into the appropriate partition queue for processing.
- **Efficient Processing**: This approach ensures that messages are processed efficiently, even when dealing with high-throughput scenarios, as it reduces the overhead of individual message fetching.

By using `getmany`, you can poll multiple messages in a single call, which can significantly improve the performance and efficiency of your Kafka consumer.



Using `asyncio` instead of threading can still be beneficial even when the primary task isn't I/O-bound. Here are some reasons why `asyncio` might be preferable over threading:

1. **Lower Overhead**:
   - **Thread Creation**: Creating and managing threads has a higher overhead compared to creating coroutines with `asyncio`.
   - **Context Switching**: Threads require context switching by the operating system, which is more costly than the context switching between coroutines managed by `asyncio`.

2. **Scalability**:
   - **Resource Management**: `asyncio` can manage thousands of tasks more efficiently than threading can manage the same number of threads.
   - **Memory Usage**: Coroutines use less memory compared to threads, which is particularly beneficial for applications that need to handle a large number of concurrent tasks.

3. **Concurrency Model**:
   - **Simpler Concurrency**: `asyncio` provides a single-threaded concurrency model, which can be easier to reason about compared to multi-threading, especially for avoiding race conditions and deadlocks.
   - **Deterministic Execution**: The event loop in `asyncio` ensures that coroutines are executed deterministically, which can simplify debugging and testing.

4. **Integrated Features**:
   - **Built-in Libraries**: `asyncio` integrates well with modern Python features and libraries, providing a rich set of tools for managing concurrency.
   - **Standard Library**: Being part of the standard library, `asyncio` is well-maintained and supported by the Python community.

### Example Using `asyncio` for Non-I/O-Bound Task Processing

Even if your Kafka message processing tasks are CPU-bound, you can still use `asyncio` effectively. However, you may need to combine it with `concurrent.futures.ThreadPoolExecutor` for truly CPU-bound tasks to prevent blocking the event loop.

Here's an example:

```python
import asyncio
from aiokafka import AIOKafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# Configuration for the Kafka consumer
KAFKA_BOOTSTRAP_SERVERS = 'your_bootstrap_servers'
KAFKA_TOPIC = 'your_topic'
KAFKA_GROUP_ID = 'your_group_id'

# Function to process messages from a specific partition
def process_message(message):
    # Simulate CPU-bound processing
    print(f"Partition {message.partition}: {message.value.decode('utf-8')}")

# Function to process messages asynchronously
async def process_partition_messages(partition, message_queue, executor):
    loop = asyncio.get_event_loop()
    while True:
        message = await message_queue.get()
        if message is None:  # Shutdown signal
            break
        # Run CPU-bound task in a thread pool
        await loop.run_in_executor(executor, process_message, message)
        message_queue.task_done()

# Main function to consume messages
async def consume():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        enable_auto_commit=False
    )

    await consumer.start()
    try:
        partition_queues = defaultdict(asyncio.Queue)
        partition_tasks = {}
        executor = ThreadPoolExecutor(max_workers=10)  # Adjust the number of workers as needed

        async for msg in consumer:
            partition = msg.partition
            if partition not in partition_tasks:
                queue = partition_queues[partition]
                task = asyncio.create_task(process_partition_messages(partition, queue, executor))
                partition_tasks[partition] = task

            # Put the message into the corresponding partition queue
            await partition_queues[partition].put(msg)
    finally:
        # Shutdown handling
        for partition, task in partition_tasks.items():
            await partition_queues[partition].put(None)
            await task

        await consumer.stop()
        executor.shutdown(wait=True)

# Entry point
if __name__ == '__main__':
    asyncio.run(consume())
```

### Explanation:

1. **ThreadPoolExecutor**: Used to offload CPU-bound tasks to a pool of threads to avoid blocking the event loop.
2. **`run_in_executor`**: Allows running the CPU-bound `process_message` function in the thread pool.
3. **Efficient Queue Management**: Each partition has its own queue, and messages are processed concurrently by the event loop.

By combining `asyncio` with a thread pool for CPU-bound tasks, you can achieve a highly efficient and scalable solution that leverages the benefits of both asynchronous and multi-threaded programming models. This approach ensures that your application remains responsive and can handle a high volume of concurrent tasks effectively.



, message_queue):
       while True:
           message = message_queue.get()
           if message is None:  # Shutdown signal
               break
           # Process the message
           print(f"Partition {partition}: {message.value().decode('utf-8')}")
           consumer.commit(message)  # Commit the message

   # Dictionary to hold the queues and threads for each partition
   partition_threads = {}

   # Function to assign partitions to the consumer
   def on_assign(consumer, partitions):
       for partition in partitions:
           partition = partition.partition
           if partition not in partition_threads:
               message_queue = queue.Queue()
               thread = threading.Thread(target=process_partition_messages, args=(partition, message_queue))
               partition_threads[partition] = {'queue': message_queue, 'thread': thread}
               thread.start()
       consumer.assign(partitions)

   # Function to revoke partitions from the consumer
   def on_revoke(consumer, partitions):
       for partition in partitions:
           partition = partition.partition
           if partition in partition_threads:
               # Signal the thread to shut down
               partition_threads[partition]['queue'].put(None)
               partition_threads[partition]['thread'].join()
               del partition_threads[partition]
       consumer.unassign()

   consumer.subscribe(['your_topic'], on_assign=on_assign, on_revoke=on_revoke)

   # Poll for messages
   try:
       while True:
           msg = consumer.poll(1.0)
           if msg is None:
               continue
           if msg.error():
               if msg.error().code() == KafkaError._PARTITION_EOF:
                   continue
               elif msg.error():
                   raise KafkaException(msg.error())
           # Put the message in the respective partition's queue
           partition = msg.partition()
           partition_threads[partition]['queue'].put(msg)
   except KeyboardInterrupt:
       pass
   finally:
       consumer.close()

       # Ensure all threads are properly shut down
       for partition in partition_threads:
           partition_threads[partition]['queue'].put(None)
           partition_threads[partition]['thread'].join()
   ```

3. **Explanation:**
   - **Kafka Consumer Configuration:** Configures the Kafka consumer.
   - **`process_partition_messages` function:** This function runs in a separate thread for each partition and processes messages from a queue.
   - **`on_assign` and `on_revoke` functions:** Handle partition assignment and revocation, creating and stopping threads as needed.
   - **Main loop:** Polls for messages and puts them in the appropriate queue based on the partition.

This implementation ensures that each partition has its own dedicated thread for processing messages, and new messages for the same partition are queued for processing by the same thread. This approach helps in maintaining order within each partition while enabling concurrent processing across different partitions.





Certainly! Here’s a revised version of your script to handle incoming Kafka messages using threads. When a topic is received, it triggers a new thread for processing. Further data for the same topic will wait until the thread for that topic is complete before starting a new one.

```python
import threading
import queue
from confluent_kafka import Consumer, KafkaException, KafkaError
import pandas as pd
import json

# Dictionary to hold thread locks for each topic
topic_locks = {}
# Queue to handle messages
message_queue = queue.Queue()

# Function to process messages
def process_messages():
    while True:
        topic, msg = message_queue.get()
        with topic_locks[topic]:
            try:
                message_value = msg.value()
                print(message_value)

                df = json.loads(message_value)
                print(df)

                df_po = pd.DataFrame([df])
                partition = msg.partition()
                topic = msg.topic()

                new_data = add_message_to_dataframe(topic, df_po, partition)
                new_data = new_data.to_frame().T

                ans[topic][partition] = pd.concat([ans[topic][partition], new_data], ignore_index=True)
                print(">")
                
                last_row = ans[topic][partition].iloc[-1]
                print(last_row)
                print(">")

                if len(ans[topic][partition]) > 35:
                    ans.drop(e)
                if len(ans[topic][partition]) == 35:
                    AnalysisEngine(ans)

                last_row = ans.iloc[-1]
                send_data(last_row)
            except Exception as e:
                print(f"Error processing message: {e}")
            finally:
                message_queue.task_done()

# Function to add message to the dataframe
def add_message_to_dataframe(topic, df, partition):
    # Implement your logic here
    return df

# Function to send data
def send_data(data):
    # Implement your logic here
    pass

# Function to analyze the data
def AnalysisEngine(ans):
    # Implement your logic here
    pass

# Kafka Consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_config)
consumer.subscribe(['mytopic'])

# Create and start the worker threads
num_worker_threads = 4
for i in range(num_worker_threads):
    threading.Thread(target=process_messages, daemon=True).start()

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError.PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        
        topic = msg.topic()
        if topic not in topic_locks:
            topic_locks[topic] = threading.Lock()
        
        message_queue.put((topic, msg))
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

### Explanation
1. **Thread Management**: Uses a `queue.Queue` to manage incoming messages and `threading.Lock` to ensure that messages for the same topic are processed sequentially.
2. **Worker Threads**: A fixed number of worker threads (`num_worker_threads`) are created to process the messages from the queue.
3. **Locking Mechanism**: Each topic has its own lock (`topic_locks[topic]`) to ensure that only one thread processes messages for a given topic at a time.
4. **Message Processing**: The `process_messages` function processes each message in the queue, updating the dataframe and performing necessary operations.

This setup ensures that messages for the same topic are processed sequentially, and you can scale the number of worker threads as needed.


To set up a Kafka environment with 10 topics, each with 4 partitions, and a producer that sends data to these topics, followed by consumers that consume data based on topic and partition, you can follow this comprehensive template. We'll use `kafka-python` for interacting with Kafka.

### Steps

1. **Install Kafka and kafka-python**
2. **Create Kafka Topics with Partitions**
3. **Producer Code to Send Data**
4. **Consumer Code to Consume Data Based on Topic and Partition**

### Step 1: Install kafka-python

Ensure you have `kafka-python` installed. If not, install it using:

```bash
pip install kafka-python
```

### Step 2: Create Kafka Topics with Partitions

Here's the script to create 10 topics, each with 4 partitions:

```python
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

# Kafka broker address
kafka_broker = 'localhost:9092'

# Create an admin client
admin_client = KafkaAdminClient(
    bootstrap_servers=kafka_broker,
    client_id='example_admin'
)

# Create 10 topics each with 4 partitions
topics = [NewTopic(name=f'my_topic_{i}', num_partitions=4, replication_factor=1) for i in range(10)]

try:
    admin_client.create_topics(new_topics=topics, validate_only=False)
    print("Topics created successfully.")
except TopicAlreadyExistsError:
    print("Some topics already exist.")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the admin client
admin_client.close()
```

### Step 3: Producer Code to Send Data

Here's a producer script to send data to these topics. The producer will randomly send messages to different partitions of different topics:

```python
from kafka import KafkaProducer
import json
import random

# Kafka broker address
kafka_broker = 'localhost:9092'

# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to send messages
def send_messages():
    topics = [f'my_topic_{i}' for i in range(10)]
    for _ in range(100):  # Send 100 messages as an example
        topic = random.choice(topics)
        partition = random.randint(0, 3)
        message = {
            'topic': topic,
            'partition': partition,
            'data': random.randint(0, 100)
        }
        producer.send(topic, value=message, partition=partition)
        print(f"Sent to {topic} partition {partition}: {message}")

    producer.flush()

# Send messages
send_messages()

# Close the producer
producer.close()
```

### Step 4: Consumer Code to Consume Data Based on Topic and Partition

Here's a consumer script that consumes messages from specific partitions of specific topics:

```python
from kafka import KafkaConsumer
import json

# Kafka broker address
kafka_broker = 'localhost:9092'

# Create a Kafka consumer
consumer = KafkaConsumer(
    bootstrap_servers=kafka_broker,
    auto_offset_reset='earliest',
    group_id='my_group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Subscribe to the topics
topics = [f'my_topic_{i}' for i in range(10)]
consumer.subscribe(topics)

# Process messages based on the partition they come from
for message in consumer:
    topic = message.topic
    partition = message.partition
    value = message.value

    # Print or process the message based on topic and partition
    print(f"Received from {topic} partition {partition}: {value}")

# Remember to close the consumer when done
consumer.close()
```

### Explanation

1. **Creating Topics:**
   - The admin client script creates 10 topics (`my_topic_0` to `my_topic_9`), each with 4 partitions.
   
2. **Producer:**
   - The producer sends 100 random messages to different partitions of different topics. You can adjust the number of messages and content as needed.
   
3. **Consumer:**
   - The consumer subscribes to all the topics and processes messages based on the partition they come from. This script will print the topic, partition, and message content.

### Running the Code

1. **Start Kafka Server:**
   - Ensure your Kafka server is running.
   
2. **Run the Admin Script:**
   - Run the script to create the topics and partitions.
   
3. **Run the Producer Script:**
   - Execute the producer script to send messages to the topics.
   
4. **Run the Consumer Script:**
   - Start the consumer script to begin consuming messages.

This setup allows you to simulate a Kafka environment with multiple topics and partitions, enabling producers to send and consumers to process messages accordingly. Adjust the scripts as needed to fit your specific use case and environment.


import socket
import json
import pandas as pd

def receive_json(socket):
    buffer = ""
    data_list = []

    while True:
        # Receive data in chunks
        data = socket.recv(1024).decode('utf-8')  # Adjust buffer size as needed
        if not data:
            break
        
        buffer += data

        while True:
            try:
                # Try to parse a complete JSON object from the buffer
                json_obj, end = json.JSONDecoder().raw_decode(buffer)
                buffer = buffer[end:].lstrip()  # Remove the parsed object from the buffer
                data_list.append(json_obj)  # Append the JSON object to the list
                print(json_obj)
            except json.JSONDecodeError:
                # If there is a decoding error, we need to wait for more data
                break

    return data_list

def main():
    # Example socket setup
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 12345))  # Replace with your server's address and port
    
    try:
        data_list = receive_json(s)
    finally:
        s.close()

    # Create DataFrame from the list of JSON objects
    df = pd.DataFrame(data_list)
    print(df)

if __name__ == "__main__":
    main()


To send a row of a dataframe where one column specifies the topic to which it belongs, you need to parse the message accordingly in your consumer. You can achieve this by modifying the message handling logic to access and use the topic information from the message itself.

Let's assume the dataframe row is serialized as a JSON string, and one of the keys in the JSON object is `topic`, which indicates the topic to which the message belongs.

Here's how you can modify your consumer to handle such messages:

1. **Install `pandas`** if you haven't already:

   ```bash
   pip install pandas
   ```

2. **Modify the consumer script** to parse the incoming messages and extract the topic information.

Here's the modified consumer script:

```python
from confluent_kafka import Consumer, KafkaException, KafkaError
import pandas as pd
import json

# Configuration for Kafka Consumer
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
}

# Create the Kafka Consumer
consumer = Consumer(conf)

# Initialize empty DataFrames for each topic
dataframes = {
    'topic1': pd.DataFrame(columns=['timestamp', 'value', 'topic']),
    'topic2': pd.DataFrame(columns=['timestamp', 'value', 'topic'])
}

def add_message_to_dataframe(topic, message):
    """Add a message to the appropriate dataframe based on topic."""
    try:
        message_data = json.loads(message)
        timestamp = message_data.get('timestamp')
        value = message_data.get('value')
        
        # Append the data to the corresponding dataframe
        new_row = pd.DataFrame({'timestamp': [timestamp], 'value': [value], 'topic': [topic]})
        global dataframes
        if topic in dataframes:
            dataframes[topic] = pd.concat([dataframes[topic], new_row], ignore_index=True)
        else:
            print(f"Unknown topic: {topic}")
    except json.JSONDecodeError:
        print(f"Failed to decode JSON message: {message}")

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                message_value = msg.value().decode('utf-8')
                try:
                    message_json = json.loads(message_value)
                    message_topic = message_json['topic']
                    print(f"Received message: {message_value} from topic: {message_topic}")
                    add_message_to_dataframe(message_topic, message_value)
                except KeyError:
                    print(f"Message does not contain 'topic' key: {message_value}")
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON message: {message_value}")

    finally:
        consumer.close()

# List of topics to subscribe to
topics = ['topic1', 'topic2']
basic_consume_loop(consumer, topics)

# Save dataframes to CSV files after consuming messages
dataframes['topic1'].to_csv('topic1_data.csv', index=False)
dataframes['topic2'].to_csv('topic2_data.csv', index=False)
```

### Explanation

1. **Consumer Configuration and Initialization**:
   - The `conf` dictionary specifies the Kafka consumer configuration.
   - The `consumer` object is created with this configuration.

2. **Initialize DataFrames**:
   - Two empty dataframes are initialized, one for each topic (`topic1` and `topic2`), with columns for `timestamp`, `value`, and `topic`.

3. **Function to Add Messages to DataFrame**:
   - The `add_message_to_dataframe` function takes a topic and a message as input.
   - It parses the message (assumed to be a JSON string) to extract `timestamp`, `value`, and `topic`.
   - It creates a new row with this data and appends it to the appropriate dataframe.

4. **Message Handling Loop**:
   - The `basic_consume_loop` function subscribes to the specified topics and enters an infinite loop to poll for messages.
   - For each received message, it checks for errors and, if there are none, decodes the message and topic.
   - It then calls `add_message_to_dataframe` to add the message to the appropriate dataframe.

5. **Error Handling**:
   - The code handles potential errors, such as missing `topic` keys in the message or JSON decoding errors.

6. **Saving DataFrames**:
   - After the consumer loop ends, the dataframes are saved to CSV files.

This setup allows you to dynamically handle messages from different topics and store them in separate dataframes, which can later be saved to files or used for further processing.



To subscribe to a Kafka producer in Node.js using a Python consumer, you need to set up Kafka producers and consumers in each respective language. Here's a step-by-step guide to help you achieve this:

### Step 1: Set Up Kafka

Ensure you have Kafka installed and running on your machine. You can download Kafka from the [Apache Kafka website](https://kafka.apache.org/quickstart) and follow the installation instructions for your operating system.

### Step 2: Create a Kafka Producer in Node.js

Install the `kafka-node` library:

```bash
npm install kafka-node
```

Create a producer script (`producer.js`):

```javascript
const kafka = require('kafka-node');
const Producer = kafka.Producer;
const client = new kafka.KafkaClient({ kafkaHost: 'localhost:9092' });
const producer = new Producer(client);

const topicsToCreate = [
    {
        topic: 'topic1',
        partitions: 1,
        replicationFactor: 1
    },
    {
        topic: 'topic2',
        partitions: 1,
        replicationFactor: 1
    }
];

client.createTopics(topicsToCreate, (error, result) => {
    if (error) {
        console.error('Error creating topics', error);
    } else {
        console.log('Topics created', result);
    }
});

producer.on('ready', () => {
    console.log('Producer is ready');
    setInterval(() => {
        const payloads = [
            { topic: 'topic1', messages: 'Hello from topic1' },
            { topic: 'topic2', messages: 'Hello from topic2' }
        ];
        producer.send(payloads, (err, data) => {
            if (err) {
                console.error('Error sending data', err);
            } else {
                console.log('Data sent', data);
            }
        });
    }, 5000);
});

producer.on('error', (err) => {
    console.error('Error in producer', err);
});
```

Run the producer:

```bash
node producer.js
```

### Step 3: Create a Kafka Consumer in Python

Install the `confluent-kafka` library:

```bash
pip install confluent-kafka
```

Create a consumer script (`consumer.py`):

```python
from confluent_kafka import Consumer, KafkaException, KafkaError

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(f'Received message: {msg.value().decode("utf-8")} from topic: {msg.topic()}')

    finally:
        consumer.close()

topics = ['topic1', 'topic2']
basic_consume_loop(consumer, topics)
```

Run the consumer:

```bash
python consumer.py
```

### Explanation

1. **Kafka Producer in Node.js**:
    - The `kafka-node` library is used to create a producer.
    - The producer creates two topics (`topic1` and `topic2`).
    - It sends messages to these topics every 5 seconds.

2. **Kafka Consumer in Python**:
    - The `confluent-kafka` library is used to create a consumer.
    - The consumer subscribes to both `topic1` and `topic2`.
    - It polls for messages from these topics and prints them to the console.

By following these steps, you can set up a Node.js producer to send messages to different topics and a Python consumer to subscribe to these topics and consume messages.
To connect to a Kafka server using its server link, IP address, and port from Python, you can use the `confluent-kafka` library, which is a Python wrapper around the high-performance C/C++ Kafka client library `librdkafka`.

### Installation

First, install the `confluent-kafka` library:

```sh
pip install confluent-kafka
```

### Connecting to Kafka

Here is a basic example of how to connect to a Kafka server using the `confluent-kafka` library, produce messages to a topic, and consume messages from a topic.

#### Producer Example

```python
from confluent_kafka import Producer

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Kafka server details
kafka_server = '192.168.1.100:9092'  # Replace with your Kafka server's IP and port

# Producer configuration
conf = {
    'bootstrap.servers': kafka_server,
    'client.id': 'python-producer'
}

# Create Producer instance
producer = Producer(conf)

# Produce a message
topic = 'your-topic'
message = 'Hello, Kafka!'

producer.produce(topic, value=message, callback=delivery_report)
producer.poll(1)  # Wait for delivery report
producer.flush()  # Wait for any outstanding messages to be delivered

print("Message sent to Kafka")
```

#### Consumer Example

```python
from confluent_kafka import Consumer, KafkaError

# Kafka server details
kafka_server = '192.168.1.100:9092'  # Replace with your Kafka server's IP and port

# Consumer configuration
conf = {
    'bootstrap.servers': kafka_server,
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to topic
topic = 'your-topic'
consumer.subscribe([topic])

# Poll for new messages
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # Proper message
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    pass

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
```

### Explanation

1. **Producer Configuration**:
    - `bootstrap.servers`: This is where you specify the Kafka server's address and port.
    - `client.id`: An optional identifier for the client instance.

2. **Consumer Configuration**:
    - `bootstrap.servers`: This is where you specify the Kafka server's address and port.
    - `group.id`: The consumer group id.
    - `auto.offset.reset`: What to do when there is no initial offset in Kafka or if the current offset does not exist any more on the server (e.g., because that data has been deleted). The `earliest` setting will automatically reset the offset to the earliest offset.

3. **Delivery Report Callback**:
    - The `delivery_report` function is called for each message produced to indicate the delivery result.

4. **Polling for Messages**:
    - The consumer polls for new messages from Kafka. If a message is received, it is processed. If an error occurs, it is handled accordingly.

### Important Notes

- Ensure that your Kafka server is running and accessible from the machine where your Python script is running.
- Replace `192.168.1.100:9092` with the actual IP address and port of your Kafka server.
- Replace `your-topic` with the actual topic name you are working with.
- Ensure that the `confluent-kafka` library is installed in your Python environment.
from confluent_kafka import Producer

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Kafka server details
kafka_server = '192.168.1.100:9092'  # Replace with your Kafka server's IP and port

# Producer configuration
conf = {
    'bootstrap.servers': kafka_server,
    'client.id': 'python-producer'
}

# Create Producer instance
producer = Producer(conf)

# Produce a message
topic = 'your-topic'
message = 'Hello, Kafka!'

producer.produce(topic, value=message, callback=delivery_report)
producer.poll(1)  # Wait for delivery report
producer.flush()  # Wait for any outstanding messages to be delivered

print("Message sent to Kafka")
import pandas as pd

def calculate_obv(df):
    df['OBV'] = 0  # Initialize the OBV column with 0

    # Calculate the daily price change direction
    df['Direction'] = 0
    df.loc[df['close'] > df['close'].shift(1), 'Direction'] = 1
    df.loc[df['close'] < df['close'].shift(1), 'Direction'] = -1

    # Calculate OBV
    df['OBV'] = (df['Direction'] * df['volume']).cumsum()

    # Drop the auxiliary column
    df.drop(columns=['Direction'], inplace=True)
    
    return df
Given your setup where you have KafkaJS installed for Node.js and Python classes for calculating indicators, you can establish a workflow where Node.js handles the Kafka communication and Python performs the indicator calculations. Here's how you can structure this:

1. **KafkaJS in Node.js**: Use KafkaJS to consume data from Kafka topics.
2. **Inter-process Communication**: Send the data from Node.js to Python for processing.
3. **Python for Processing**: Calculate the indicators using your Python classes.
4. **Returning Results**: Send the processed results back to Node.js and produce the results to Kafka or another service.

### Step-by-Step Implementation

#### 1. KafkaJS Consumer in Node.js

Create a Kafka consumer in Node.js that reads messages from Kafka topics.

```javascript
const { Kafka } = require('kafkajs');
const { spawn } = require('child_process');

const kafka = new Kafka({
  clientId: 'my-app',
  brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'indicator-group' });

const run = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'company-data', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const data = message.value.toString();
      console.log(`Received message: ${data}`);

      // Call Python script for processing
      const pythonProcess = spawn('python3', ['process_data.py', data]);

      pythonProcess.stdout.on('data', (data) => {
        console.log(`Processed data: ${data.toString()}`);
        // Here you can send the processed data back to Kafka or another service
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data.toString()}`);
      });
    },
  });
};

run().catch(console.error);
```

#### 2. Python Script (`process_data.py`)

Create a Python script to process the incoming data and calculate the indicators.

```python
import sys
import json
from your_indicator_module import calculate_indicators  # Replace with your actual module and function

def main():
    # Receive data from Node.js
    data = sys.argv[1]
    company_data = json.loads(data)

    # Process the data
    results = calculate_indicators(company_data)

    # Output the results
    print(json.dumps(results))

if __name__ == "__main__":
    main()
```

#### 3. Python Indicator Calculation (Placeholder)

Implement the `calculate_indicators` function in your Python module. This function should perform the necessary calculations.

```python
# your_indicator_module.py

def calculate_indicators(company_data):
    # Implement your indicator calculation logic here
    results = {}
    # Example processing
    for company, data in company_data.items():
        results[company] = some_indicator_function(data)  # Replace with actual logic
    return results

def some_indicator_function(data):
    # Placeholder for actual indicator calculation
    return sum(data) / len(data)  # Example calculation
```

#### 4. Node.js Producer for Processed Results (Optional)

If you want to send the processed results back to Kafka, you can add a producer in your Node.js script.

```javascript
const producer = kafka.producer();

const sendProcessedData = async (processedData) => {
  await producer.connect();
  await producer.send({
    topic: 'processed-data',
    messages: [{ value: processedData }],
  });
  await producer.disconnect();
};

// Inside the consumer eachMessage function
pythonProcess.stdout.on('data', async (data) => {
  const processedData = data.toString();
  console.log(`Processed data: ${processedData}`);
  await sendProcessedData(processedData);
});
```

### Summary

1. **KafkaJS Consumer**: Reads data from Kafka and sends it to the Python script.
2. **Python Script**: Processes the data using indicator classes and returns the results.
3. **KafkaJS Producer (Optional)**: Sends the processed results back to Kafka or another service.

This setup allows you to leverage KafkaJS for Kafka communication in Node.js and Python for complex data processing and indicator calculations. Adjust the specific processing logic in your Python code as needed.






import pandas as pd
import numpy as np
import os

class EMA:
    def __init__(self):
        pass

    def append_to_csv(self, df, file_path):
        mode = 'w' if not os.path.isfile(file_path) else 'a'
        df.to_csv(file_path, mode=mode, header=(mode == 'w'), index=False)
        print("Data appended successfully to", file_path)

    def round_float(self, value, precision):
        return round(value, precision)

    def detect_precision(self, value):
        value_str = str(value)
        if '.' in value_str:
            decimal_part = value_str.split('.')[1]
            return len(decimal_part)
        else:
            return 0

    def calculate_sma(self, prices, period):
        if len(prices) < period:
            raise ValueError("Not enough data points to calculate SMA")
        sma = sum(prices) / period
        return [sma]

    def calculate_ema(self, prices, period):
        if len(prices) < 2 * period:
            return []
        
        emas = []
        round_precision = 2

        # First EMA value using SMA
        sma = self.calculate_sma(prices[:period], period)
        previous_ema = sma[0]
        emas.append(self.round_float(previous_ema, round_precision))

        k = 2 / (1 + period)

        for p in prices[period:]:
            ema = (p * k) + (previous_ema * (1 - k))
            previous_ema = ema
            emas.append(self.round_float(ema, round_precision))

        return emas

    def generate_signals(self, prices, short_period, long_period):
        if len(prices) < 2 * long_period:
            print(len(prices))
            return [], []

        short_ema = self.calculate_ema(prices, short_period)
        long_ema = self.calculate_ema(prices, long_period)

        b_signal = []
        s_signal = []

        for i in range(len(long_ema)):
            if i == 0:
                b_signal.append(0)
                s_signal.append(0)
            else:
                if short_ema[i] > long_ema[i] and short_ema[i-1] <= long_ema[i-1]:
                    b_signal.append(1)
                    s_signal.append(0)
                elif short_ema[i] < long_ema[i] and short_ema[i-1] >= long_ema[i-1]:
                    s_signal.append(1)
                    b_signal.append(0)
                else:
                    b_signal.append(0)
                    s_signal.append(0)

        return b_signal, s_signal

    def group(self, frame, new_stock_data):
        global df
        df = pd.concat([df, new_stock_data], ignore_index=True)
        close_price = df['close'].to_numpy()

        ema = self.calculate_ema(close_price, frame)
        s_signal, b_signal = self.generate_signals(close_price, 5, 10)

        df['EMA'] = [0.0] * (len(df) - len(ema)) + ema
        df['buy'] = [0.0] * (len(df) - len(b_signal)) + b_signal
        df['sell'] = [0.0] * (len(df) - len(s_signal)) + s_signal

        self.append_to_csv(df, 'ema.csv')

# Create an empty DataFrame to hold stock data
stocks = pd.read_csv(r"C:\Users\K131249\pythondemo\indicators\intrada.csv")
stocks = pd.DataFrame(stocks)

# Initialize the EMA calculator
ema_calculator = EMA()

# Define the global DataFrame with required columns
df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'rsi', 'ema_5','ema_13','ema_16', 'vwap', 'atr', 'super_upperband', 'super_lowerband', 'MACD', 'MACD_Signal'])

# Schedule the group function
ema_calculator.group(5, stocks)




To efficiently receive data, calculate indicators, and return the results using Kafka and Python, you can structure your backend system in a modular and concurrent manner. Here’s a step-by-step guide to achieve this:

### Step 1: Set Up Kafka

Ensure Kafka is correctly installed and running. You can refer to the previous instructions for installation. 

### Step 2: Define Your Indicators

Assume you have your indicator classes defined as follows:

```python
class MovingAverage:
    def __init__(self, window):
        self.window = window

    def calculate(self, data):
        return sum(data[-self.window:]) / self.window

class RSI:
    def __init__(self, period):
        self.period = period

    def calculate(self, data):
        gains = [data[i] - data[i - 1] for i in range(1, len(data)) if data[i] > data[i - 1]]
        losses = [-data[i] + data[i - 1] for i in range(1, len(data)) if data[i] < data[i - 1]]
        avg_gain = sum(gains) / self.period
        avg_loss = sum(losses) / self.period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        return rsi

# Add other indicators similarly
```

### Step 3: Kafka Producer (Data Reception Service)

This service will receive stock data and send it to a Kafka topic:

```python
from kafka import KafkaProducer
import json

class DataProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_data(self, topic, stock_data):
        self.producer.send(topic, stock_data)
        self.producer.flush()

# Example usage
producer = DataProducer()
stock_data = {
    'stock_id': 'AAPL',
    'timestamp': '2024-06-02T12:34:56Z',
    'price': 150.25,
    'volume': 1000
}
producer.send_data('stock_data', stock_data)
```

### Step 4: Kafka Consumer (Indicator Calculation Service)

This service will consume stock data from the Kafka topic, calculate indicators, and send the results to another topic:

```python
from kafka import KafkaConsumer, KafkaProducer
import json
from concurrent.futures import ThreadPoolExecutor

class DataConsumer:
    def __init__(self, bootstrap_servers='localhost:9092', group_id='indicator_calculator'):
        self.consumer = KafkaConsumer(
            'stock_data',
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def consume_data(self):
        for message in self.consumer:
            stock_data = message.value
            self.process_data(stock_data)

    def process_data(self, stock_data):
        indicators = [MovingAverage(20), RSI(14)]  # Add other indicator instances
        indicator_calculator = IndicatorCalculator()
        results = indicator_calculator.calculate_indicators(stock_data, indicators)
        self.producer.send('indicator_results', {'stock_id': stock_data['stock_id'], 'results': results})
        self.producer.flush()

class IndicatorCalculator:
    def calculate_indicators(self, stock_data, indicators):
        results = {}
        
        with ThreadPoolExecutor(max_workers=len(indicators)) as executor:
            future_to_indicator = {executor.submit(indicator.calculate, stock_data['price']): indicator for indicator in indicators}
            for future in concurrent.futures.as_completed(future_to_indicator):
                indicator = future_to_indicator[future]
                results[indicator.__class__.__name__] = future.result()
        
        return results

# Example usage
consumer = DataConsumer()
consumer.consume_data()
```

### Step 5: Data Delivery Service

Use WebSocket to deliver the calculated indicator values to clients in real-time:

```python
import asyncio
import websockets
import json
from kafka import KafkaConsumer

class DataDelivery:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.consumer = KafkaConsumer(
            'indicator_results',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    async def send_data(self, websocket, path):
        for message in self.consumer:
            indicator_data = message.value
            await websocket.send(json.dumps(indicator_data))

    def start_server(self):
        server = websockets.serve(self.send_data, 'localhost', 6789)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

# Example usage
delivery = DataDelivery()
delivery.start_server()
```

### Step 6: Running the System

1. **Start the Kafka Broker**:
   Ensure Kafka is running.

2. **Start the Data Producer**:
   ```python
   producer = DataProducer()
   stock_data = {
       'stock_id': 'AAPL',
       'timestamp': '2024-06-02T12:34:56Z',
       'price': 150.25,
       'volume': 1000
   }
   producer.send_data('stock_data', stock_data)
   ```

3. **Start the Data Consumer**:
   ```python
   consumer = DataConsumer()
   consumer.consume_data()
   ```

4. **Start the Data Delivery Service**:
   ```python
   delivery = DataDelivery()
   delivery.start_server()
   ```

### Summary

By integrating Kafka with your Python application, you can efficiently receive stock data, calculate multiple indicators concurrently, and deliver the results in real-time. The system is designed to handle high throughput and ensure low latency, making it suitable for trading applications. Adjust the configuration and implementation details to match your specific requirements and environment.



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
