"""Receive one targeted task, calculate x + y, and return the result."""
import os, pickle, time, zmq
from common import Task, Result

WORKER_NAME = os.getenv("WORKER_NAME", "Worker")
TASK_HOST = os.getenv("TASK_HOST", "127.0.0.1")
TASK_PORT = int(os.getenv("TASK_PORT", "9921"))
RESULT_PORT = int(os.getenv("RESULT_PORT", "9933"))

def main():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    receiver.connect(f"tcp://{TASK_HOST}:{TASK_PORT}")
    sender = context.socket(zmq.PUSH)
    sender.bind(f"tcp://*:{RESULT_PORT}")
    print(f"[{WORKER_NAME}] PULL connected to tcp://{TASK_HOST}:{TASK_PORT}", flush=True)
    print(f"[{WORKER_NAME}] PUSH result socket bound to tcp://*:{RESULT_PORT}", flush=True)
    payload = receiver.recv()
    task = pickle.loads(payload)
    if not isinstance(task, Task):
        raise TypeError("Received message is not a Task object")
    answer = int(task.x) + int(task.y)
    result = Result(task.task_id, task.x, task.y, task.operation, answer, WORKER_NAME)
    print(f"[{WORKER_NAME}] RECEIVED task #{task.task_id}: {task.x} + {task.y}", flush=True)
    print(f"[{WORKER_NAME}] CALCULATED result: {answer}", flush=True)
    sender.send(pickle.dumps(result))
    print(f"[{WORKER_NAME}] SENT result for task #{task.task_id} to port {RESULT_PORT}", flush=True)
    time.sleep(0.5)
    receiver.close(); sender.close(); context.term()

if __name__ == "__main__":
    main()
