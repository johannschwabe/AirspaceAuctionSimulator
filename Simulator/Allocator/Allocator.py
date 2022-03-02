from abc import ABC, abstractmethod
from typing import List, Dict

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agents(self, agents: List[Agent], env: Environment) -> Dict[Agent, List[List[TimeCoordinate]]]:
        pass
