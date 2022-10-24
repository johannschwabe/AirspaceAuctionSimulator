from typing import List, Dict, Any

from Simulator import Bid, PathAgent, Coordinate4D


class CBSPathBid(Bid):
    def __init__(self, agent: "PathAgent", locations: List["Coordinate4D"], stays: List[int], battery: int,
                 flying=False):
        super().__init__(agent)
        # overwrite agent for typing
        self.agent: "PathAgent" = agent
        # locations this agent still wants to visit
        self.locations: List["Coordinate4D"] = locations
        # stay durations for the locations
        self.stays: List[int] = stays
        # remaining battery (in ticks)
        self.battery: int = battery

        self.flying: bool = False

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __le__(self, other):
        return True

    def __eq__(self, other):
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": {
                "locations": [[location.x, location.y, location.z, location.t] for location in self.locations],
                "stays": self.stays,
                "battery": self.battery,
            },
            "display": {
                "path": " -> ".join(
                    f"{int(location.x)}, {int(location.y)}, {int(location.z)}, {int(location.t)}" for location in
                    self.locations),
                "battery": self.battery

            }

        }
