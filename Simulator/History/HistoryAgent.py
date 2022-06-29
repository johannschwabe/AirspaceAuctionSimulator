from typing import List, Dict

from ..Agent import Agent
from ..Coordinate import Coordinate4D


class HistoryAgent:
    def __init__(self, agent: Agent, registered: int, speed: int):
        self.id = agent.id
        self.registered: int = registered
        self.traveled_paths = []
        self.past_allocations: Dict[int, List[List[Coordinate4D]]] = {}
        self.speed = speed

    def reallocation(self, new_path: List[List[Coordinate4D]], time_step: int):
        self.past_allocations[time_step] = new_path
