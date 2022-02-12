from typing import List

from .Agent import Agent
from .Blocker import Blocker
from .Environment import Environment
from .Allocator import Allocator
from .Owner import Owner
from .helpers.History import History


class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment,
                 history: History,
                 blocker: List[Blocker]):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: History = history
        self.blocker: List[Blocker] = blocker
        self.agents: List[Agent] = []
        self.time_step = 0

    def setup(self):
        pass

    def reset(self):
        pass

    def tick(self) -> bool:
        newcomers = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step)
        for agent in newcomers:
            self.allocator.allocate_for_agent(agent)
        self.time_step += 1
        self.environment.visualize(self.time_step)
        if self.time_step > 100:
            return False
        return True
