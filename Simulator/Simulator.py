from typing import List

from .Agent import Agent
from .Coordinate import TimeCoordinate
from .Environment import Environment
from .Allocator import Allocator
from .Owner import Owner


class Simulator:
    def __init__(
        self,
        owners: List[Owner],
        allocator: Allocator,
        environment: Environment,
    ):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.agents: List[Agent] = []
        self.time_step = 0

    def tick(self) -> bool:
        newcomers: List[Agent] = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self.environment)
        for agent in newcomers:
            agent_paths: List[List[TimeCoordinate]] = self.allocator.allocate_for_agent(agent, self.environment)
            self.environment.allocate_paths(agent, agent_paths)
        self.time_step += 1
        return True
