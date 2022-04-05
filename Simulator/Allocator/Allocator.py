from abc import ABC, abstractmethod
from typing import List, Dict

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment, TempEnvironment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self, agents: List[Agent], env: Environment) -> Dict[Agent, List[List[TimeCoordinate]]]:
        pass

    def temp_allocation(self, agents: List[Agent], env: TempEnvironment) -> Dict[Agent, List[List[TimeCoordinate]]]:
        cloned_agents = [agent.clone() for agent in agents]
        allocations = self.allocate_for_agents(cloned_agents, env)
        #remap allocation to correct agents
