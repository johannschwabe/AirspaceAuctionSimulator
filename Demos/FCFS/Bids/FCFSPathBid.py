import json
from typing import List, Dict

from Simulator import Bid, PathAgent, Coordinate4D


class FCFSPathBid(Bid):
    def __init__(self, agent: "PathAgent", locations: List["Coordinate4D"], stays: List[int], battery: int):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "PathAgent" = agent
        # locations this agent still wants to visit
        self.locations: List["Coordinate4D"] = locations
        # stay durations for the locations
        self.stays: List[int] = stays
        # remaining battery (in ticks)
        self.battery: int = battery

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def to_dict(self) -> Dict[str, str | int | float]:
        return {
            "locations": json.dumps([[location.x, location.y, location.z, location.t] for location in self.locations]),
            "stays": self.stays,
            "battery": self.battery
        }
