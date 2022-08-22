from abc import ABC
from typing import List, Optional, TYPE_CHECKING

from Simulator.Agents.AgentType import AgentType
from .PathAgent import PathAgent

if TYPE_CHECKING:
    from Simulator.Coordinates.Coordinate4D import Coordinate4D
    from Simulator.Allocation.PathSegment import PathSegment
    from Simulator.Simulator import Simulator


class ABCAgent(PathAgent, ABC):
    agent_type: str = AgentType.ABC.value

    def __init__(self,
                 locations: List["Coordinate4D"],
                 stays: List[int],
                 simulator: "Simulator",
                 agent_id: Optional[int] = None,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 near_radius: Optional[int] = None):

        super().__init__(simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

        self.locations: List["Coordinate4D"] = locations
        self.stays: List[int] = stays

    def value_for_segments(self, paths: List["PathSegment"]) -> float:
        if len(paths) == 0:
            return 0.

        if len(paths) != len(self.locations) - 1:
            print("Invalid allocation!!")
            return 0.

        value = 1.
        time = 0
        for path, location in zip(paths, self.locations[1:]):
            destination = path[-1]
            if not destination.inter_temporal_equal(location):
                print("Invalid allocation!")
                return 0.

            time += destination.t - path[0].t
            value -= (destination.t - location.t) / 100

        if time > self.battery:
            return -1.

        return round(max(0., value), 2)
