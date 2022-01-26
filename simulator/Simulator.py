from typing import List

from simulator.blocker.Blocker import Blocker
from simulator.owners.Owner import Owner
from simulator.allocators.Allocator import Allocator
from simulator.environments.Environment import Environment
from simulator.helpers.History import History
from simulator.statistics.Statistics import Statistics


class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment,
                 history: History,
                 blocker: List[Blocker],
                 statistics: Statistics):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: History = history
        self.blocker: List[Blocker] = blocker
        self.statistics: Statistics = statistics
        self.time_step = 0

    def setup(self):
        pass

    def reset(self):
        pass

    def tick(self) -> bool:
        pass
