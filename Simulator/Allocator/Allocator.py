from typing import List

from ..Agent import Agent
from ..Path import TravelPath
from ..Environment import Environment
from ..Coordinate import TimeCoordinate
from ..Field import EnrichedField


class Allocator:
    def __init__(self):
        pass

    def allocate_for_agent(self, agent: Agent, env: Environment):
        pass

    def get_welfare(self, t1: int, t2: int) -> float:
        pass

    def get_field_at(self, coords: TimeCoordinate) -> EnrichedField:
        pass

    def get_cost_of_path(self, path: TravelPath) -> float:
        pass

    def allocate_path_to_agent(self, path: TravelPath, agent: Agent) -> bool:
        pass

    def get_all_active_agents(self) -> List[Agent]:
        pass

    def get_agents_with_collision(self, path: TravelPath) -> List[Agent]:
        pass

    def ask_agents_for_bids(self, agents: List[Agent]):
        pass
