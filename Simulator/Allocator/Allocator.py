from abc import ABC, abstractmethod
from typing import List

from ..Path import TravelPath
from ..Field import Field
from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Environment import Environment
from ..helpers.PathFinding import astar


class Allocator(ABC):
    def __init__(self):
        self.env = None

    def register(self, env: Environment):
        self.env = env

    def get_shortest_path(self, start: TimeCoordinate, target: TimeCoordinate):
        assert self.env is not None
        return astar(start, target, self.env)

    @abstractmethod
    def allocate_for_agent(self, agent: Agent):
        pass

    def allocate(self, fields: List[Field], agent: Agent, path: List[TimeCoordinate]):
        assert self.env is not None
        for field in fields:
            field.allocated_to = agent

        self.env.add_agent(agent)
        agent.allocated_path = TravelPath(path)
