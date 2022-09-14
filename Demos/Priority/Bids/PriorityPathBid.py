import json
from typing import List, Dict

from Simulator import Bid, PathAgent, Coordinate4D


class PriorityPathBid(Bid):
    def __init__(self, agent: "PathAgent", locations: List["Coordinate4D"], stays: List[int], battery: int,
                 priority: float, flying: bool):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "PathAgent" = agent
        # locations this agent still wants to visit
        self.locations: List["Coordinate4D"] = locations
        # stay durations for the locations
        self.stays: List[int] = stays
        # remaining battery (in ticks)
        self.battery: int = battery
        # priority in collisions
        self.priority: float = priority
        # if the agent is currently in the air
        self.flying: bool = flying

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def to_dict(self) -> Dict[str, str | int | float]:
        return {
            "locations": json.dumps([[location.x, location.y, location.z, location.t] for location in self.locations]),
            "stays": self.stays,
            "battery": self.battery,
            "priority": self.priority,
            "flying": self.flying,
        }
