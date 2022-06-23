import math
import random
from typing import List, Optional, Tuple, TYPE_CHECKING

from .EnvironmentGen import EnvironmentGen
from ..Owner.ABAOwner import ABAOwner
from ..Owner.ABCOwner import ABCOwner
from ..Owner.ABOwner import ABOwner
from ..Owner.StationaryOwner import StationaryOwner
from ..Statistics.Statistics import Statistics
from ..Allocator import FCFSAllocator
from ..History import History
from ..Simulator import Simulator

if TYPE_CHECKING:
    from .MapTile import MapTile
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
        maptiles: List["MapTile"]
    ):
        self.name: str = name
        self.description: str = description
        self.ownerTypes = owners
        self.dimensions: "TimeCoordinate" = dimensions
        self.owners: List["Owner"] = []
        self.allocator: "Allocator" = FCFSAllocator()
        self.environment: "Environment" = EnvironmentGen(self.dimensions, maptiles).generate(10)
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History"] = None
        self.statistics: Optional[Statistics] = None
        self.simulator: Optional[Simulator] = None

    def simulate(self):
        for ownerType in self.ownerTypes:
            if ownerType.type == "ab":
                self.owners.append(ABOwner(ownerType.name,
                                           ownerType.color,
                                           creation_ticks(self.environment.get_dim().t, ownerType.agents)))
            if ownerType.type == "aba":
                self.owners.append(ABAOwner(ownerType.name,
                                            ownerType.color,
                                            creation_ticks(self.environment.get_dim().t, ownerType.agents)))
            if ownerType.type == "stat":
                self.owners.append(
                    StationaryOwner(ownerType.name,
                                    ownerType.color,
                                    creation_ticks(self.environment.get_dim().t, ownerType.agents)))
            if ownerType.type == "abc":
                self.owners.append(ABCOwner(ownerType.name,
                                            ownerType.color,
                                            creation_ticks(self.environment.get_dim().t, ownerType.agents)))

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


def creation_ticks(duration, total, std=-1) -> List[int]:
    res = []
    if duration == 1:
        return [0]*total
    if duration == 2:
        return ([0] * int(total/2)) + ([1] * int(total/2))

    if std == -1:
        std = total/duration/3
    sum = 0
    for i in range(duration-2):
        expected = (total - sum)/(duration - i)
        next = max(int(random.gauss(expected, std)), 0)
        res.extend(next*[i])
        sum += next
    next_1 = max(int((total-sum)/2), 0)
    res.extend(next_1 * [duration - 2])
    sum += next_1
    next_2 = max(total - sum, 0)
    res.extend(next_2* [duration - 1])
    sum += next_2
    print(sum)
    return res
