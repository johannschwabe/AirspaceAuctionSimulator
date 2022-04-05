from typing import List, Dict

from .HistoryAgent import HistoryAgent
from ..Coordinate import Coordinate, TimeCoordinate
from ..Simulator import Environment, Tick
from ..Agent import Agent
from ..Allocator import Allocator
from ..History.Owner import Owner
class History2:
    def __init__(self, dims: Coordinate, allocator: Allocator, env: Environment):
        self.dims = dims
        self.agents: Dict[Agent, HistoryAgent] = {}
        self.owners: List[Owner] = []
        self.allocator: Allocator = allocator
        self.env: Environment = env

    def set_owners(self, owners: List[Owner]):
        self.owners = owners

    def add_new_agents(self, agents: List[Agent], time_step: Tick):
        for agent in agents:
            self.agents[agent] = HistoryAgent(agent.id, time_step)

    def update_allocations(self, new_allocations: Dict[Agent, List[List[TimeCoordinate]]], time_step):
        for agent, paths in new_allocations.items():
            history_agent = self.agents[agent]
            history_agent.reallocation(paths, time_step)


