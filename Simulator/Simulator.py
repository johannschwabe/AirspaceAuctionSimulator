from typing import List
from .Path import PathReallocation, SpaceReallocation
from .Agent import Agent
from .Environment import Environment
from .Allocator import Allocator
from .Owner import Owner
from .History.History import History


class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: History = History(allocator, environment, owners)

        self.time_step = 0

    def tick(self) -> bool:
        newcomers: List[Agent] = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self.environment)

        if len(newcomers) > 0:
            self.history.add_new_agents(newcomers, self.time_step)
            temp_env = self.environment.clone()
            cloned_agents_paths: List[PathReallocation | SpaceReallocation] = self.allocator.temp_allocation(newcomers, temp_env, self.time_step)
            agents_paths = self.environment.original_agents(cloned_agents_paths, newcomers)
            self.environment.allocate_segments_for_agents(agents_paths, self.time_step)
            self.history.update_allocations(agents_paths, self.time_step)
        self.time_step += 1
        return True
