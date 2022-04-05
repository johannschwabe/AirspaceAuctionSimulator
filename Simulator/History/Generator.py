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
        owners,
        dimensions: TimeCoordinate,
        avg_flight_time: int
    ):
        self.name: str = name
        self.description: str = description
        self.ownerTypes = owners
        self.dimensions: TimeCoordinate = dimensions
        self.avg_flight_time: int = avg_flight_time
        self.owners: List[Owner] = []
        self.allocator: Allocator = FCFSAllocator()
        self.environment: Environment = EnvironmentGen(self.dimensions).generate(10)
        self.simulator: Optional[Simulator] = None

    def simulate(self):
        for ownerType in self.ownerTypes:
            if ownerType.type == "a-to-b":
                self.owners.append(ABOwner([i for i in range(ownerType.agents)]))

        self.simulator = Simulator(
            self.owners,
            self.allocator,
            self.environment,
        )
        while self.simulator.time_step <= self.dimensions.t:
            print(f"STEP: {self.simulator.time_step}")
            self.simulator.tick()
        return History(self.name, self.description, self.simulator)

