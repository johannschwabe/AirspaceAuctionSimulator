from typing import List, Dict

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Time import Tick


class HistoryAgent:
    def __init__(self, agent: Agent, registered: int, speed: int):
        self.id = agent.id
        self.registered: int = registered
        self.past_allocations: Dict[int, List[List[TimeCoordinate]]] = {}
        self.speed = speed

    def reallocation(self, new_path: List[List[TimeCoordinate]], time_step: Tick):
        self.past_allocations[time_step] = new_path
