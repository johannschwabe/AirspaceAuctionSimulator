from typing import List, Dict

from ..Agent import Agent
from ..Coordinate import Coordinate4D
from ..Enum import Reason


class HistoryAgent:
    def __init__(self, agent: Agent, registered: int):
        self.id = agent.id
        self.registered: int = registered
        self.past_allocations: Dict[int, Dict[str, List[List[Coordinate4D]] | Reason | float]] = {}
        self.allocation_time: Dict[int, int]

    def reallocation(self, new_path: List[List[Coordinate4D]], reason: Reason, time_step: int, compute_time: float):
        self.past_allocations[time_step] = {"path": new_path, "reason": reason, "time": compute_time}

