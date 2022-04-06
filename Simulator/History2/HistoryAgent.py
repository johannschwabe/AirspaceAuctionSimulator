from typing import List, Dict

from ..Coordinate import TimeCoordinate
from ..Time import Tick


class HistoryAgent:
    def __init__(self, uid, registered: Tick):
        self.id = uid
        self.registered = registered
        self.traveled_path: List[TimeCoordinate] = []
        self.past_allocations: Dict[Tick, List[List[TimeCoordinate]]] = {}

    def reallocation(self, new_path: List[List[TimeCoordinate]], time_step: Tick):
        self.past_allocations[time_step] = new_path
