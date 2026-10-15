# ZeroMQ Distributed Sum (Python)

A small distributed-processing assignment using **Python + ZeroMQ (pyzmq)**. The distributor generates two random integer tasks. Two workers share the distributor's PUSH/PULL queue; each worker adds `x + y` for every task it receives and sends a pickled `Result` to the collector. The collector gathers two unique task results and prints them.

## Components and ports

| Component | Socket | Address / port | Purpose |
|---|---|---|---|
| Distributor | PUSH / bind | `tcp://*:9921` and `tcp://*:9922` | Sends one targeted `Task` to each worker |
| Worker 1 | PULL / connect | `tcp://127.0.0.1:9921` | Receives tasks |
| Worker 2 | PULL / connect | `tcp://127.0.0.1:9922` | Receives its task |
| Worker 1 | PUSH / bind | `tcp://*:9933` | Sends results |
| Worker 2 | PUSH / bind | `tcp://*:9932` | Sends results |
| Collector | PULL / connect | ports `9933`, `9932` | Collects results |

To make the screenshot requirement reproducible, this implementation uses **one task PUSH socket per worker**. The distributor sends task #1 to Worker 1 on port 9921 and task #2 to Worker 2 on port 9922. Each worker therefore receives one task in every normal run.

## Run locally (recommended for screenshots)

Requires Python 3.11 and `pyzmq`.

### Option A: Conda
```bash
conda env create -f environment.yml
conda activate zmq-sum-assignment
```

### Option B: venv
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
python -m pip install pyzmq==26.2.1
```

Open **four terminals** in the project folder. Run these in order:

Terminal 1:
```bash
python src/collector.py
```
Terminal 2:
```bash
WORKER_NAME="Worker 1" TASK_PORT=9921 RESULT_PORT=9933 python src/worker.py
```
Terminal 3:
```bash
WORKER_NAME="Worker 2" TASK_PORT=9922 RESULT_PORT=9932 python src/worker.py
```
Terminal 4:
```bash
python src/distributor.py
```

On Windows Command Prompt, set environment variables using `set` first, or use PowerShell:
```powershell
$env:WORKER_NAME="Worker 1"; $env:RESULT_PORT="9933"; python src/worker.py
```
Repeat for Worker 2 with port 9932. Start collector and both workers before starting the distributor. The distributor waits two seconds before sending.

## Run with Docker Compose
```bash
docker compose up --build
```
Stop with `Ctrl+C`. The Compose setup starts the collector, both workers, and distributor in one coordinated network.

## Message classes and serialization
`src/common.py` defines:
- `Task(task_id, x, y, operation="sum")`
- `Result(task_id, x, y, operation, result, worker)`

The sender serializes objects using `pickle.dumps(...)`; the receiver restores them using `pickle.loads(...)`. **Only unpickle data from trusted senders** because pickle is not safe for untrusted input.

## Important implementation note
This version deliberately uses separate task ports so each worker receives a task deterministically. That is slightly different from a shared load-balanced queue, but it directly satisfies the requirement that both worker terminals show a received message.

## Suggested screenshot checklist
1. Distributor terminal showing both `SENT task` messages.
2. Worker 1 terminal showing `RECEIVED` and `SENT result`.
3. Worker 2 terminal showing `RECEIVED` and `SENT result`.
4. Collector terminal showing both results and the summary.
5. If using Docker, `docker compose up --build` shows logs for all services; use `docker compose logs -f distributor worker1 worker2 collector` if needed.
