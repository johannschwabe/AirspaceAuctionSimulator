from typing import List, Dict

from .HistoryAgent import HistoryAgent
from ..Coordinate import Coordinate, TimeCoordinate
from ..Enum import Reason
from ..Simulator import Environment, Tick
from ..Agent import Agent
from ..Allocator import Allocator
from ..Owner import Owner


class History:
    def __init__(self, dims: Coordinate, allocator: Allocator, env: Environment, owners: List[Owner]):
        self.dims = dims
        self.agents: Dict[Agent, HistoryAgent] = {}
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.env: Environment = env


    def set_owners(self, owners: List[Owner]):
        self.owners = owners

    def add_new_agents(self, agents: List[Agent], time_step: Tick):
        for agent in agents:
            self.agents[agent] = HistoryAgent(agent, time_step)

    def update_allocations(self, new_allocations:  List["PathReallocation | SpaceReallocation"], time_step):
        for reallocation in new_allocations:
            history_agent = self.agents[reallocation.agent]
            history_agent.reallocation(reallocation.segments, reallocation.reason, time_step)
