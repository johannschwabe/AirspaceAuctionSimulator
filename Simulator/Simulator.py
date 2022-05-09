from typing import List, Dict, TYPE_CHECKING

from .Time import Tick
from .Agent import Agent
from .Coordinate import TimeCoordinate
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
        newcomers: List[Agent] = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self.environment)

        if len(newcomers) > 0:
            self.history.add_new_agents(newcomers, self.time_step)
            temp_env = self.environment.clone()
            agents_paths: Dict[Agent, List[List[TimeCoordinate]]] = self.allocator.temp_allocation(newcomers, temp_env)
            self.environment.allocate_paths_for_agents(agents_paths, self.time_step)
            self.history.update_allocations(agents_paths, self.time_step)

        self.time_step += 1
        return True

