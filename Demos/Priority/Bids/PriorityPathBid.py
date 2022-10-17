from typing import Any, Dict, List

from Simulator import Bid, Coordinate4D, PathAgent


class PriorityPathBid(Bid):
    def __init__(self, agent: "PathAgent", locations: List["Coordinate4D"], stays: List[int], battery: int,
                 priority: float, index: int, flying: bool):
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
        # the index of the first path segment requested in this bid
        self.index = index
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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": {
                "locations": [[location.x, location.y, location.z, location.t] for location in self.locations],
                "stays": self.stays,
                "battery": self.battery,
                "priority": self.priority,
                "index": self.index,
                "flying": self.flying
            },
            "display": {
                "path": " -> ".join(
                    f"{int(location.x)}, {int(location.y)}, {int(location.z)}, {int(location.t)}" for location in
                    self.locations),
                "battery": self.battery,
                "priority": self.priority
            }

        }
