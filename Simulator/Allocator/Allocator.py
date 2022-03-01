from abc import ABC, abstractmethod
from typing import List

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment


class Allocator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def allocate_for_agent(self, agent: Agent, env: Environment) -> List[List[TimeCoordinate]]:
        pass
