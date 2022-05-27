from abc import ABC, abstractmethod
from typing import List, Dict, TYPE_CHECKING

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment
from ..Path import PathSegment

if TYPE_CHECKING:
    from .. import Tick


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self, agents: List[Agent], env: Environment, tick: "Tick") -> Dict[Agent, List[PathSegment]]:
        pass

    def temp_allocation(self, agents: List[Agent], env: Environment, tick: "Tick") -> Dict[Agent, List[PathSegment]]:
        cloned_agents = [agent.clone() for agent in agents]
        return self.allocate_for_agents(cloned_agents, env, tick)


