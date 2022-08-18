from time import time_ns
from typing import List, TYPE_CHECKING

from .History.History import History

if TYPE_CHECKING:
    from .Path.Allocation import Allocation
    from .Agents.Agent import Agent
    from .Environment.Environment import Environment
    from .Allocator.Allocator import Allocator
    from .Owners.Owner import Owner


class Simulator:
    def __init__(self,
                 owners: List["Owner"],
                 allocator: "Allocator",
                 environment: "Environment"):
        self.owners: List["Owner"] = owners
        self.allocator: "Allocator" = allocator
        self.environment: "Environment" = environment
        self.history: "History" = History(allocator, environment, owners)

        self.time_step = 0
        self._agent_id = 0

    def get_agent_id(self) -> int:
        agent_id = self._agent_id
        self._agent_id += 1
        return agent_id

    def tick(self) -> bool:
        newcomers: List["Agent"] = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self)

        if len(newcomers) > 0:
            print(f"STEP: {self.time_step}")
            start_time = time_ns()
            self.history.add_new_agents(newcomers, self.time_step)
            temp_env = self.environment.clone()
            cloned_agents_paths: List["Allocation"] = self.allocator.temp_allocation(
                newcomers,
                temp_env,
                self.time_step)
            agents_paths = self.environment.original_agents(cloned_agents_paths, newcomers)
            self.environment.allocate_segments_for_agents(agents_paths, self.time_step)
            self.history.update_allocations(agents_paths, self.time_step, (time_ns() - start_time) / 1e6)
        self.time_step += 1
        return True
