from typing import List, Dict

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Enum import Reason
from ..Time import Tick


class HistoryAgent:
    def __init__(self, agent: Agent, registered: int):
        self.id = agent.id
        self.registered: int = registered
        self.past_allocations: Dict[int, Dict[str, List[List[TimeCoordinate]] | Reason]] = {}

    def reallocation(self, new_path: List[List[TimeCoordinate]], reason: Reason, time_step: Tick):
        self.past_allocations[time_step] = {"path": new_path, "reason": reason}
