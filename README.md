A design document, often referred to as a design doc, is a comprehensive guide that outlines the architecture, components, and processes of a project. Here’s a general structure to help you get started:

1. **Title Page**
   - Project Title
   - Author(s)
   - Date
   - Version

2. **Table of Contents**
   - List of sections and subsections with page numbers

3. **Introduction**
   - **Purpose**: Explain the purpose of the document and the project.
   - **Scope**: Define the scope of the project.
   - **Audience**: Identify the intended audience for the document.
   - **Overview**: Provide a brief overview of what the document contains.

4. **Project Overview**
   - **Background**: Context and background information about the project.
   - **Objectives**: Clear and measurable objectives of the project.
   - **Stakeholders**: List of stakeholders involved in the project.

5. **Requirements**
   - **Functional Requirements**: Specific behaviors or functions of the system.
   - **Non-functional Requirements**: Performance, security, usability, etc.
   - **Constraints**: Any limitations or constraints affecting the design.

6. **System Architecture**
   - **High-Level Architecture**: Overview of the system architecture with diagrams.
   - **Components**: Description of major system components.
   - **Data Flow**: Data flow diagrams or descriptions.

7. **Detailed Design**
   - **Component Design**: Detailed design of each component.
   - **Interfaces**: Description of interfaces between components.
   - **Data Models**: Database schemas, data models, and related information.

8. **User Interface Design**
   - **Wireframes**: Sketches or wireframes of key screens.
   - **User Flows**: Descriptions or diagrams of user flows.

9. **Security Considerations**
   - **Threat Model**: Potential security threats and mitigation strategies.
   - **Security Measures**: Specific security measures implemented.

10. **Testing and Validation**
    - **Test Plan**: Plan for testing the system.
    - **Test Cases**: Specific test cases with expected outcomes.
    - **Validation**: How the system will be validated against requirements.

11. **Deployment Plan**
    - **Environment**: Description of the deployment environment.
    - **Deployment Steps**: Steps for deploying the system.
    - **Rollback Plan**: Plan for rolling back if deployment fails.

12. **Maintenance and Support**
    - **Maintenance Plan**: Plan for ongoing maintenance.
    - **Support**: Support processes and contacts.

13. **Appendices**
    - **Glossary**: Definitions of terms used in the document.
    - **References**: References to other documents or resources.

14. **Revision History**
    - **Change Log**: Record of changes made to the document.

When writing a design document, aim for clarity and conciseness. Use diagrams and visual aids to supplement the text and make complex information more accessible.






The error you're encountering, `SQLite objects created in a thread can only be used in that same thread`, occurs because SQLite connections are not thread-safe. When you try to use the same SQLite connection in multiple threads, it leads to this error. 

To prevent this, you need to ensure that each thread or async task gets its own database connection. Here are some ways to handle this:

1. **Connection Pooling**: Use a connection pool to manage SQLite connections. This ensures that each thread gets a fresh connection from the pool.

2. **Pass Connections to Threads**: Create a new connection in each thread or async task.

Here's an example of how you can modify your code to create a new SQLite connection for each async task:

### Modified Code

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import json
import pandas as pd
from process import Indicator
from engine import AnalysisEngine
from minordb.db_controller import DBController

# Database Controller Initialization
# Removed global dbController to prevent shared usage in threads

def get_db_controller():
    return DBController()

def fetch_data(topic, db_controller):
    prev_data = db_controller.findStockDataByCompanyId(topic)
    columns = ['companyId', 'frame', 'open', 'close', 'high', 'low', 'volume', 'timestamp', 'UpperBand', 'LowerBand', 
               'MACD', 'MACD_Signal', 'MACD_Hist', 'vwap', 'rsi', 'obv', 'ema_5', 'ema_13', 'ema_26', 'supertrend']
    new_stock = pd.DataFrame(columns=columns)
    
    if len(prev_data) == 0:
        return new_stock

    for _dict in prev_data:
        data = pd.DataFrame([_dict])
        data = data.reindex(columns=columns)  # Ensure columns are in the correct order and missing columns are added as NaN
        data.dropna(axis=1, how="all", inplace=True)
        new_stock = pd.concat([new_stock, data], ignore_index=True)

    return new_stock

def add_message_to_dataframe(topic, message, db_controller):
    new_stock = fetch_data(topic, db_controller)
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
    db_controller = get_db_controller()  # Create a new DB controller for this thread
    new_data = add_message_to_dataframe(topic, df_po, db_controller)
    new_data = new_data.to_frame().T

    stock = fetch_data(topic, db_controller)
    stock.dropna(axis=1, how="all", inplace=True)
    stock = pd.concat([stock, new_data], ignore_index=True)

    AnalysisEngine(stock)

    result_dict = (stock.iloc[-1]).to_dict()
    res = db_controller.insertStockData(result_dict)
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
    dbController = get_db_controller()  # Setup initial DB controller to create tables, etc.
    print(dbController.setup("./databases/stock.db", 35))
    asyncio.run(main())
```

### Key Changes:
1. **Removed Global DB Controller**: The `dbController` is not shared globally to avoid cross-thread issues.
2. **New DB Controller Per Task**: Added a function `get_db_controller()` to create a new `DBController` instance for each thread or async task.
3. **Reindexing DataFrame**: Ensured DataFrame has the correct columns and added as NaN if missing.
4. **Isolated Database Operations**: Database operations are now confined to the thread or task that initiated them, ensuring thread safety.

By making these changes, each thread or async task gets its own connection to the database, preventing the cross-thread SQLite usage issue.
