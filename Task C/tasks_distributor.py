from data_worker import DataToWorker
import main_constants as mc
import zmq
import time
import random
import pickle

### Here's the step by step
### Create your context 
### Create 1 socket using the PUSH socket type
### Bind your PUSH socket to your desired endpoint.
context = zmq.Context()
socket = context.socket(zmq.PUSH)
endpoint = "tcp://*:9921"
socket.bind(endpoint)

print(f"Tasks distributor is running on {endpoint}")
print("Sending tasks to workers")
print("There are 3 available tasks")
print("Sum; Multiply; Division")

while True:
    ### Generate 2 random numbers
    ### set the appropriate value for the given variables
    ## send the data
    time.sleep(5)
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    task_code = random.choice([mc.SUM, mc.MUT, mc.DIV])
    task_data = DataToWorker(num1, num2, task_code)
    sent_task = pickle.dumps(task_data)
    print(f"Sending task --- {task_code} ({num1} & {num2}) waiting for available worker to handle")
    socket.send(sent_task)
    print("--- Sent --- ")