from typing import List, Optional, TYPE_CHECKING

from Simulator.Owner.ABAOwner import ABAOwner
from Simulator.Owner.ABCOwner import ABCOwner
from Simulator.Owner.ABOwner import ABOwner
from Simulator.Owner.StationaryOwner import StationaryOwner
from .EnvironmentGen import EnvironmentGen
from ..Allocator import FCFSAllocator
from ..History2 import History2
from .History import History
from ..Simulator import Simulator

if TYPE_CHECKING:
    from ..Allocator import Allocator
    from ..Owner import Owner
    from ..Environment import Environment
    from ..Coordinate import TimeCoordinate


class Generator:
    def __init__(
        self,
        name: str,
        description: str,
        owners,
        dimensions: "TimeCoordinate",
    ):
        self.name: str = name
        self.description: str = description
        self.ownerTypes = owners
        self.dimensions: "TimeCoordinate" = dimensions
        self.owners: List["Owner"] = []
        self.allocator: "Allocator" = FCFSAllocator()
        self.environment: "Environment" = EnvironmentGen(self.dimensions).generate(10)
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History2"] = None

    def simulate(self):
        for ownerType in self.ownerTypes:
            if ownerType.type == "a-to-b":
                self.owners.append(ABOwner([i for i in range(ownerType.agents)]))
            if ownerType.type == "a-to-b-to-a":
                self.owners.append(ABAOwner([i for i in range(ownerType.agents)]))
            if ownerType.type == "stationary":
                self.owners.append(StationaryOwner([i for i in range(ownerType.agents)]))
            if ownerType.type == "a-to-b-to-c":
                self.owners.append(ABCOwner([i for i in range(ownerType.agents)]))
        self.history = History2(self.dimensions, self.allocator, self.environment, self.owners)
        self.simulator = Simulator(
            self.owners,
            self.allocator,
            self.environment,
            self.history
        )
        while self.simulator.time_step <= self.dimensions.t:
            print(f"STEP: {self.simulator.time_step}")
            self.simulator.tick()
        return History(self.name, self.description, self.simulator)
