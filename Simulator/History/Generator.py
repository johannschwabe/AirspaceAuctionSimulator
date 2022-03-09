from typing import List, Optional

from owners.ABOwner import ABOwner
from .EnvironmentGen import EnvironmentGen
from ..Allocator import FCFSAllocator, Allocator
from ..Owner import Owner
from .History import History
from ..Simulator import Simulator
from ..Environment import Environment
from ..Coordinate import TimeCoordinate


class Generator:
    def __init__(
        self,
        name: str,
        description: str,
        agents: int,
        owners: int,
        dimensions: TimeCoordinate,
        avg_flight_time: int
    ):
        self.name: str = name
        self.description: str = description
        self.n_agents: int = agents
        self.n_owners: int = owners
        self.dimensions: TimeCoordinate = dimensions
        self.avg_flight_time: int = avg_flight_time
        self.owners: List[Owner] = []
        self.allocator: Allocator = FCFSAllocator()
        self.environment: Environment = EnvironmentGen(self.dimensions).generate(10)
        self.simulator: Optional[Simulator] = None

    def simulate(self):
        for owner in range(self.n_owners):
            self.owners.append(ABOwner(list(range(round(self.n_agents / self.n_owners)))))
        self.simulator = Simulator(
            self.owners,
            self.allocator,
            self.environment,
        )
        while self.simulator.time_step <= self.dimensions.t:
            print(f"\r{self.simulator.time_step}", end="")
            self.simulator.tick()
        return History(self.name, self.description, self.simulator)

