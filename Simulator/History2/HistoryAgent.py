from typing import List, Dict

from Simulator import Tick
from Simulator.Coordinate import TimeCoordinate


class HistoryAgent:
    def __init__(self, uid, registered: Tick):
        self.id = uid
        self.registered = registered
        self.traveled_path: List[TimeCoordinate] = []
        self.passed_allocations: Dict[Tick, List[List[TimeCoordinate]]] = {}

    def reallocation(self, new_path: List[List[TimeCoordinate]], time_step: Tick):
        self.passed_allocations[time_step] = new_path
