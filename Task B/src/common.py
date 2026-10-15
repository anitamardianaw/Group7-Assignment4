"""Shared message classes for the ZeroMQ sum example."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    task_id: int
    x: int
    y: int
    operation: str = "sum"

@dataclass
class Result:
    task_id: int
    x: int
    y: int
    operation: str
    result: int
    worker: str
