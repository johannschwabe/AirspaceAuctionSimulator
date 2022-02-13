from abc import ABC, abstractmethod

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment
from ..helpers.PathFinding import astar


class Allocator(ABC):
    def __init__(self, env: Environment):
        self.env = env

    def get_shortest_path(self, start: TimeCoordinate, target: TimeCoordinate):
        return astar(start,
                     target,
                     self.env)

    @abstractmethod
    def allocate_for_agent(self, agent: Agent, env: Environment):
        pass
