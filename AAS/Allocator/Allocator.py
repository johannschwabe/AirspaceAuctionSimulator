from abc import ABC, abstractmethod
from typing import List, Dict, TYPE_CHECKING

from ..Agent import Agent
from ..Environment import Environment
from ..Path import PathSegment
from ..Path import PathAllocation
from ..Path import SpaceAllocation

class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self,
                            agents: List[Agent],
                            env: Environment,
                            tick: int) -> List[PathAllocation | SpaceAllocation]:
        pass

    def temp_allocation(self,
                        agents: List[Agent],
                        env: Environment,
                        tick: int) -> List[PathAllocation | SpaceAllocation]:
        cloned_agents = [agent.clone() for agent in agents]
        return self.allocate_for_agents(cloned_agents, env, tick)

    @staticmethod
    def compatible_owner():
        pass

