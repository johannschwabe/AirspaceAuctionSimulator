from typing import List, Dict, Any, Optional
from Simulator import GridLocation, Coordinate4D, BiddingStrategy, ValueFunction, Environment, SpaceSegment, SpaceAgent, \
    SpaceOwner


class APISpaceOwner(SpaceOwner):
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
        super().__init__(owner_id, name, color, stops, creation_ticks, size, bidding_strategy, value_function, meta)

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
