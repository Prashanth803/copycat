To implement a microservice architecture where you receive data from a server and pass it to different indicator classes without requiring traditional API routes, you can use an event-driven approach. This can be achieved using a message broker to facilitate communication between services. 

Here is a step-by-step guide to implementing this:

### 1. Set Up the Environment

1. **Install RabbitMQ**: Ensure RabbitMQ is installed and running.
2. **Install Necessary Libraries**: Use `pika` for RabbitMQ and any other libraries you need for your indicator classes.

```bash
pip install pika
```

### 2. Define Your Indicator Classes

Let's assume you have several indicator classes that process data and return some results. Each class should have a method that takes data as input and returns some processed result.

```python
class IndicatorA:
    def process(self, data):
        # Process the data
        return f"IndicatorA processed {data}"

class IndicatorB:
    def process(self, data):
        # Process the data
        return f"IndicatorB processed {data}"
```

### 3. Microservice to Receive Data and Distribute

This microservice will receive data from the server and publish it to a RabbitMQ queue.

```python
import socket
import pika

def start_socket_client():
    host = 'your_server_ip'  # Server IP address
    port = 12345  # Server port

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")
        distribute_data(data)

    s.close()

def distribute_data(data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='data_queue')
        channel.basic_publish(exchange='', routing_key='data_queue', body=data)
        print(f"Data sent to queue: {data.decode('utf-8')}")
    except pika.exceptions.AMQPError as err:
        print(f"Error occurred: {err}")
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    start_socket_client()
```

### 4. Microservices to Process Data

Each microservice will consume data from the RabbitMQ queue, process it using the indicator classes, and potentially return the result to another queue or directly back to the client if needed.

**Microservice for IndicatorA:**

```python
import pika

class IndicatorA:
    def process(self, data):
        return f"IndicatorA processed {data}"

def callback(ch, method, properties, body):
    data = body.decode('utf-8')
    indicator = IndicatorA()
    result = indicator.process(data)
    print(f"Processed result: {result}")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='data_queue')
    channel.basic_consume(queue='data_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
```

**Microservice for IndicatorB:**

```python
import pika

class IndicatorB:
    def process(self, data):
        return f"IndicatorB processed {data}"

def callback(ch, method, properties, body):
    data = body.decode('utf-8')
    indicator = IndicatorB()
    result = indicator.process(data)
    print(f"Processed result: {result}")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='data_queue')
    channel.basic_consume(queue='data_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
```

### Summary

1. **Socket Client**: Connects to the server and receives data, then sends it to a RabbitMQ queue.
2. **Message Broker (RabbitMQ)**: Facilitates communication between the data-receiving service and the indicator processing services.
3. **Indicator Microservices**: Each microservice listens to the RabbitMQ queue, processes the data using its indicator class, and outputs the result.

This setup ensures a decoupled, scalable, and event-driven architecture, where each microservice can independently process incoming data without requiring direct API routes.
