"""Collect and print results returned by workers."""
import os
import pickle
import zmq
from common import Result

HOST = os.getenv("COLLECTOR_HOST", "*")
ENDPOINTS = [item.strip() for item in os.getenv("RESULT_ENDPOINTS", "127.0.0.1:9933,127.0.0.1:9932").split(",")]
EXPECTED_RESULTS = int(os.getenv("TASK_COUNT", "2"))

def main():
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    for endpoint in ENDPOINTS:
        receiver.connect(f"tcp://{endpoint}")
        print(f"[Collector] PULL connected to tcp://{endpoint}", flush=True)

    print(f"[Collector] Waiting for {EXPECTED_RESULTS} result(s)...", flush=True)
    results = []
    seen_ids = set()
    while len(results) < EXPECTED_RESULTS:
        payload = receiver.recv()
        result = pickle.loads(payload)
        if not isinstance(result, Result):
            print("[Collector] Ignored an unknown message type.", flush=True)
            continue
        if result.task_id in seen_ids:
            print(f"[Collector] Duplicate result for task #{result.task_id}; ignored.", flush=True)
            continue
        seen_ids.add(result.task_id)
        results.append(result)
        print(
            f"[Collector] RECEIVED task #{result.task_id} from {result.worker}: "
            f"{result.x} + {result.y} = {result.result}",
            flush=True
        )

    print("\\n[Collector] SUMMARY", flush=True)
    for item in sorted(results, key=lambda r: r.task_id):
        print(f"  Task #{item.task_id}: {item.x} + {item.y} = {item.result} "
              f"(processed by {item.worker})", flush=True)
    print("[Collector] All results collected. End.", flush=True)
    receiver.close()
    context.term()

if __name__ == "__main__":
    main()
