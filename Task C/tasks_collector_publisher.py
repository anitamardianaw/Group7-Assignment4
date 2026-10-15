import zmq
import pickle
from data_worker import DataToWorker
import main_constants as mc

### Here's the step by step
### Create your context 
### Create 2 sockets using the pull socket type
### Connect each pull socket variable to the worker's socket end point.

### Create a socket using the pub socket type to publish the message
### Bind your publisher socket to your desired endpoint.

context = zmq.Context()
pull_worker_1 = context.socket(zmq.PULL)
pull_worker_2 = context.socket(zmq.PULL)
pull_worker_1.connect("tcp://localhost:9933")
pull_worker_2.connect("tcp://localhost:9932")

poller = zmq.Poller()
poller.register(pull_worker_1, zmq.POLLIN)
poller.register(pull_worker_2, zmq.POLLIN)

pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:9991")

def set_data_message(data: DataToWorker, message: str):
    data.set_message(message)
    return data

message_sum: str = "The summation process has been executed sucessfully"
message_multiply: str = "The multiplication process has been executed sucessfully"
message_div: str = "The div process has been executed sucessfully"

print("Tasks Collector & Publisher is running...")

while True:
    ##  Receive tasks from the workers
    ### Loads the data 
    ### set the message property appropriately for the given operation 
    ### send the multipart data.
    socks = dict(poller.poll())

    if pull_worker_1 in socks:
        raw_data = pull_worker_1.recv()
    elif pull_worker_2 in socks:
        raw_data = pull_worker_2.recv()
    else:
        continue

    print("Task is received")

    result: DataToWorker = pickle.loads(raw_data)

    if mc.SUM == result.op:
        result = set_data_message(result, message_sum)
    elif mc.MUT == result.op:
        result = set_data_message(result, message_multiply)
    elif mc.DIV == result.op:
        result = set_data_message(result, message_div)

    print("Sending the results to subscribers...")
    pub_socket.send_multipart([result.op.encode("utf-8"), pickle.dumps(result)])
    print("--- Sent ---")