from typing import List

from .Agent import Agent
from .Environment import Environment
from .Allocator import Allocator
from .Owner import Owner
from .helpers.History import History


class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment,
                 history: History):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: History = history
        self.agents: List[Agent] = []
        self.time_step = 0

    def setup(self):
        pass

    def reset(self):
        pass

    def tick(self) -> bool:
        newcomers = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self.environment)
        allocated = False
        while not allocated:
            allocated = True
            for agent in newcomers:
                self.allocator.allocate_for_agent(agent)
        self.time_step += 1
        return True
