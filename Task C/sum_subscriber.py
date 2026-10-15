import main_constants as mc
from data_worker import DataToWorker
import pickle
import zmq

### Here's the step by step
### Create your context 
### Create a socket using the subscriber socket type
### Connect the socket to the publisher'socket 
### Set socket topic
context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:9991")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, mc.SUM)

index: int = 0
print("Waiting for a new message to arrive... ")

def show_content(result):
    result_obj: DataToWorker = pickle.loads(result)
    print(f"Input Numbers: {result_obj.num1} & {result_obj.num2}")
    print(f"Main Operation: {result_obj.op}")
    print(f"Result: {result_obj.result}")
    print(f"Message: {result_obj.message}")
    print(f"EXECUTOR: {result_obj.exe}")

while True:
    ### Receive the data in multi part
    ### Call the show_content
    topic, payload = sub_socket.recv_multipart()
    print("Received a new message: with topic's name", str(topic.decode("utf-8")))
    show_content(payload)

    index += 1

    if index >= 5:
        print("\033c", end="")
        index = 0
    print("\nRepeating ...\n")