from typing import List, Dict
from time import time_ns

from .Time import Tick
from .Agent import Agent
from .Coordinate import TimeCoordinate
from .Environment import Environment
from .Allocator import Allocator
from .History2 import History2
from .Owner import Owner

class Simulator:
    def __init__(self,
                 owners: List[Owner],
                 allocator: Allocator,
                 environment: Environment,
                 history: History2):
        self.owners: List[Owner] = owners
        self.allocator: Allocator = allocator
        self.environment: Environment = environment
        self.history: History2 = history
        self.agents: List[Agent] = []
        self.time_step = Tick(0)

    def tick(self) -> bool:
        t1 = time_ns()
        newcomers: List[Agent] = []
        for owner in self.owners:
            newcomers += owner.generate_agents(self.time_step, self.environment)
        self.history.add_new_agents(newcomers, self.time_step)
        t2 = time_ns()
        temp_env = self.environment.clone()
        t3 = time_ns()
        agents_paths: Dict[Agent, List[List[TimeCoordinate]]] = self.allocator.temp_allocation(newcomers, temp_env)
        t4 = time_ns()
        self.environment.allocate_paths_for_agents(agents_paths, self.time_step)
        t5 = time_ns()
        self.history.update_allocations(agents_paths, self.time_step)
        self.time_step += 1
        t6 = time_ns()
        # print(f"1-2: {(t2-t1)/1e9}, 2-3: {(t3-t2)/1e9}, 3-4: {(t4-t3)/1e9}, 4-5: {(t5-t4)/1e9}, 5-6: {(t6-t5)/1e9}")
        return True
