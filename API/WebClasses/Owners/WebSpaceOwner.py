import random
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from Simulator import SpaceAgent, SpaceOwner, SpaceSegment
from .WebOwnerMixin import WebOwnerMixin

if TYPE_CHECKING:
    from Simulator import Coordinate4D, BiddingStrategy, ValueFunction, Environment
    from ...GridLocation.GridLocation import GridLocation


class WebSpaceOwner(WebOwnerMixin, SpaceOwner):
    def __init__(self,
                 owner_id,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 size: "Coordinate4D",
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 config: Optional[Dict[str, Any]] = None):
        super().__init__(name, color, creation_ticks, owner_id, bidding_strategy, value_function, config=config)
        self.stops = stops
        self.size: "Coordinate4D" = size

    def initialize_agent(self, blocks: List["SpaceSegment"]) -> "SpaceAgent":
        agent_id: str = self.get_agent_id()
        return SpaceAgent(agent_id, self.bidding_strategy, self.value_function, blocks, config=self.config)

    @staticmethod
    def generate_stop_coordinates(stop: "GridLocation", env: "Environment", t: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + random.randint(15, 30))
        return coord

    def generate_agents(self, t: int, environment: "Environment") -> List["SpaceAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks: List["SpaceSegment"] = []
            for idx, stop in enumerate(self.stops):
                center = self.generate_stop_coordinates(stop, environment, t)
                bottom_left = center.clone()
                bottom_left.x -= round(self.size.x / 2)
                bottom_left.z -= round(self.size.z / 2)
                top_right = bottom_left + self.size
                blocks.append(SpaceSegment(bottom_left, top_right, idx))
            agent = self.initialize_agent(blocks)
            res.append(agent)
            print(f"{agent} {', '.join([str(block) for block in blocks])}")

        self.agents += res
        return res
