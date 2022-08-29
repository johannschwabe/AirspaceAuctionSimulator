from typing import List, TYPE_CHECKING

from .Owner import Owner
from ..Agents.SpaceAgent import SpaceAgent

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
                 value_function: "ValueFunction"
                 ):
        super().__init__(owner_id, bidding_strategy, value_function, name, color)
        self.stops = stops
        self.creation_ticks = creation_ticks
        self.size: "Coordinate4D" = size

    @staticmethod
    def generate_stop_coordinates(stop: "GridLocation", env: "Environment", t: int) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + 1)
        return coord

    def initialize_agent(self, blocks: List[List["Coordinate4D"]]) -> "SpaceAgent":
        agent_id: str = self.get_agent_id()
        return SpaceAgent(agent_id, self.bidding_strategy, self.value_function, blocks)

    def generate_agents(self, t: int, environment: "Environment") -> List["SpaceAgent"]:
        res = []
        for _ in range(self.creation_ticks.count(t)):
            blocks = []
            for stop in self.stops:
                center = self.generate_stop_coordinates(stop, environment, t)
                bottom_left = center.clone()
                bottom_left.x -= round(self.size.x / 2)
                bottom_left.z -= round(self.size.z / 2)
                top_right = bottom_left + self.size
                blocks.append([bottom_left, top_right])
            agent = self.initialize_agent(blocks)
            res.append(agent)
            print(f"{agent} {', '.join([str(block) for block in blocks])}")

        self.agents += res
        return res
