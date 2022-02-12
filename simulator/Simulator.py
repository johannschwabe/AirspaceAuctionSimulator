from typing import List

from simulator.owners.Owner import Owner
from simulator.allocators.Allocator import Allocator
from simulator.environments.Environment import Environment
from simulator.helpers.History import History


class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment,
                 history: History,
                 ):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: History = history
        self.time_step = 0

    def setup(self):
        pass

    def reset(self):
        pass

    def tick(self) -> bool:
        newcommers = []
        for owner in self.owners:
            newcommers += owner.generate_agents(self.time_step)
        for agent in newcommers:
            self.allocator.allocate_for_agent(agent)
        self.time_step+=1
        self.environment.visualize(self.time_step)
        if self.time_step > 100:
            return False
        return True