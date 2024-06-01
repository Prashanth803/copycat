import socket
import pickle

class DataSender:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_data(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            # Pickle the data
            pickled_data = pickle.dumps(data)
            s.sendall(pickled_data)
            response = s.recv(4096)
            # Unpickle the response
            response = pickle.loads(response)
            return response

if __name__ == "__main__":
    sender = DataSender("localhost", 5001)  # Connect to the receiving server
    data = "Data to be processed"
    result = sender.send_data(data)
    
    # Assuming the response is a dictionary with 'result_a' and 'result_b' as keys
    result_a = pickle.loads(result['result_a'])
    result_b = pickle.loads(result['result_b'])
    
    print("Received results:")
    print(result_a)
    print(result_b)
