from typing import List, TYPE_CHECKING, Dict, Any, Optional

from .Owner import Owner
from ..Agents.SpaceAgent import SpaceAgent
from ..Segments.SpaceSegment import SpaceSegment

if TYPE_CHECKING:
    from ..Location.GridLocation import GridLocation
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class SpaceOwner(Owner):
    def __init__(self,
                 owner_id: str,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 size: "Coordinate4D",
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 meta: Optional[Dict[str, Any]] = None):
        super().__init__(owner_id, bidding_strategy, value_function, creation_ticks, name, color, meta if meta else {})
        self.stops = stops
        self.size: "Coordinate4D" = size

    @staticmethod
    def generate_stop_coordinates(stop: "GridLocation", env: "Environment", t: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + 1)
        return coord

    def initialize_agent(self, blocks: List["SpaceSegment"]) -> "SpaceAgent":
        agent_id: str = self.get_agent_id()
        return SpaceAgent(agent_id, self.bidding_strategy, self.value_function, blocks, config=self.config)

    def generate_agents(self, t: int, environment: "Environment") -> List["SpaceAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks: List["SpaceSegment"] = []
            for stop in self.stops:
                center = self.generate_stop_coordinates(stop, environment, t)
                bottom_left = center.clone()
                bottom_left.x -= round(self.size.x / 2)
                bottom_left.z -= round(self.size.z / 2)
                top_right = bottom_left + self.size
                blocks.append(SpaceSegment(bottom_left, top_right))
            agent = self.initialize_agent(blocks)
            res.append(agent)
            print(f"{agent} {', '.join([str(block) for block in blocks])}")

        self.agents += res
        return res
