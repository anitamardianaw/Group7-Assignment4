"""Generate two random integer tasks and route one directly to each worker."""
import os, pickle, random, time, zmq
from common import Task

PORT1 = int(os.getenv("WORKER1_TASK_PORT", "9921"))
PORT2 = int(os.getenv("WORKER2_TASK_PORT", "9922"))
LOW = int(os.getenv("RANDOM_MIN", "1"))
HIGH = int(os.getenv("RANDOM_MAX", "100"))

def main():
    context = zmq.Context()
    sockets = []
    for port in (PORT1, PORT2):
        sock = context.socket(zmq.PUSH)
        sock.bind(f"tcp://*:{port}")
        sockets.append(sock)
        print(f"[Distributor] PUSH socket bound to tcp://*:{port}", flush=True)
    time.sleep(float(os.getenv("STARTUP_DELAY", "2")))
    for task_id, sock in enumerate(sockets, start=1):
        task = Task(task_id, random.randint(LOW, HIGH), random.randint(LOW, HIGH))
        sock.send(pickle.dumps(task))
        print(f"[Distributor] SENT task #{task.task_id} to Worker {task_id}: {task.x} + {task.y}", flush=True)
    print("[Distributor] Both tasks sent.", flush=True)
    time.sleep(1)
    for sock in sockets:
        sock.close()
    context.term()

if __name__ == "__main__":
    main()
