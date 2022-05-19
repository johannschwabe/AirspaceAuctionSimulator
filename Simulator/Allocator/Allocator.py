from abc import ABC, abstractmethod
from typing import List, Dict, TYPE_CHECKING

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment

if TYPE_CHECKING:
    from .. import Tick


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self, agents: List[Agent], env: Environment, tick: "Tick") -> Dict[Agent, List[List[TimeCoordinate]]]:
        pass

    def temp_allocation(self, agents: List[Agent], env: Environment, tick: "Tick") -> Dict[Agent, List[List[TimeCoordinate]]]:
        cloned_agents = [agent.clone() for agent in agents]
        allocations = self.allocate_for_agents(cloned_agents, env, tick)
        res = {}
        for cloned_agent, paths in allocations.items():
            index = [_agent.__repr__() for _agent in agents].index(cloned_agent.__repr__())
            agent = agents[index]
            res[agent] = paths
        return res

