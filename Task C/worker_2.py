import pickle
import main_constants as mc
from data_worker import DataToWorker
import zmq
import random
import time

## Create context
## Create pull and push socket
## Bind the push socket
## Connect the pull socket
context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
push_socket = context.socket(zmq.PUSH)
push_socket.bind("tcp://*:9932")
pull_socket.connect("tcp://localhost:9921")

def task_1_sum(num1: float, num2: float) -> float:
    print(f"[x] {num1} + {num2} ")
    return float(num1 + num2)

def task_2_multiply(num1: float, num2: float) -> float:
    print(f"[x] {num1} x {num2} ")
    return float(num1 * num2)

def task_3_division(num1: float, num2: float) -> float:
    print(f"[x] {num1} / {num2} ")
    return float(num1 / num2) if num2 != 0 else 0.0

print("Successfully connected with the server ...")
print("Waiting for tasks ... ")

while True:
    ### receive the task using the pull socket
    ### load the task 
    ### Get the numbers
    ### do the operation based upon the operation of DataToWorker object
    ### set the result property of your DataToWorker object
    ### set the executor
    ### Push the updated object
    work_time = random.uniform(0.5, 1)
    time.sleep(work_time)

    raw_data = pull_socket.recv()
    task_data: DataToWorker = pickle.loads(raw_data)
    print("WORKER-2: Handling the task")
    result: float = 0.0

    if task_data.op == mc.SUM:
        result = task_1_sum(task_data.num1, task_data.num2)
    elif task_data.op == mc.MUT:
        result = task_2_multiply(task_data.num1, task_data.num2)
    elif task_data.op == mc.DIV:
        result = task_3_division(task_data.num1, task_data.num2)

    task_data.set_result(result)
    task_data.set_executor(mc.WORKER_2)
    push_socket.send(pickle.dumps(task_data))

    print("Data has been processed, sending them to the collector ...\n")