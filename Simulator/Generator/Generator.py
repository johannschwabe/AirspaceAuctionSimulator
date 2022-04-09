from typing import List, Optional, Tuple, TYPE_CHECKING

from ..Owner.ABAOwner import ABAOwner
from ..Owner.ABCOwner import ABCOwner
from ..Owner.ABOwner import ABOwner
from .EnvironmentGen import EnvironmentGen
from ..Owner.StationaryOwner import StationaryOwner
from ..Statistics.Statistics import Statistics
from ..Allocator import FCFSAllocator
from ..History import History
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
        self.history: Optional["History"] = None
        self.statistics: Optional[Statistics] = None
        self.simulator: Optional[Simulator] = None

    def simulate(self) -> Statistics:
        for ownerType in self.ownerTypes:
            if ownerType.type == "ab":
                self.owners.append(ABOwner(ownerType.name, ownerType.color, [i for i in range(ownerType.agents)]))
            if ownerType.type == "aba":
                self.owners.append(ABAOwner(ownerType.name, ownerType.color, [i for i in range(ownerType.agents)]))
            if ownerType.type == "stat":
                self.owners.append(
                    StationaryOwner(ownerType.name, ownerType.color, [i for i in range(ownerType.agents)]))
            if ownerType.type == "abc":
                self.owners.append(ABCOwner(ownerType.name, ownerType.color, [i for i in range(ownerType.agents)]))

        self.history = History(
            self.dimensions,
            self.allocator,
            self.environment,
            self.owners,
        )
        self.simulator = Simulator(
            self.owners,
            self.allocator,
            self.environment,
            self.history,
        )
        while self.simulator.time_step <= self.dimensions.t:
            print(f"STEP: {self.simulator.time_step}")
            self.simulator.tick()

        self.statistics = Statistics(self.simulator, self.name, self.description)
        return self.statistics
