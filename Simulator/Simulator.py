from typing import List, TYPE_CHECKING
from time import time
from .Path import PathReallocation, SpaceReallocation
from .Time import Tick
from .Agent import Agent
from .Environment import Environment
from .Allocator import Allocator
from .Owner import Owner

if TYPE_CHECKING:
    from .History import History


class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment,
                 history: "History"):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: "History" = history
        # self.agents: List[Agent] = []
        self.time_step = Tick(0)

    def tick(self) -> bool:
        start_t = time() * 1000
        newcomers: List[Agent] = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self.environment)
        agents_created_t = time() * 1000

        if len(newcomers) > 0:
            self.history.add_new_agents(newcomers, self.time_step)
            history_updated_t = time() * 1000
            temp_env = self.environment.clone()
            temp_env_created_t = time() * 1000
            cloned_agents_paths: List[PathReallocation | SpaceReallocation] = self.allocator.temp_allocation(newcomers, temp_env, self.time_step)
            temp_allocations_t = time() * 1000
            agents_paths = self.environment.original_agents(cloned_agents_paths, newcomers)
            path_translated_t = time() * 1000
            self.environment.allocate_segments_for_agents(agents_paths, self.time_step)
            real_env_updated_t = time() * 1000
            self.history.update_allocations(agents_paths, self.time_step)
            history_updated_2_t = time() * 1000
        self.time_step += 1
        return True
