import random
from typing import List, Optional, TYPE_CHECKING, Dict

from .EnvironmentGen import EnvironmentGen
from ..Owner.PathOwners.ABAOwner import ABAOwner
from ..Owner.PathOwners.ABCOwner import ABCOwner
from ..Owner.PathOwners.ABOwner import ABOwner
from ..Owner.SpaceOwners.StationaryOwner import StationaryOwner
from ..Statistics.Statistics import Statistics
from ..Allocator import FCFSAllocator
from ..History import History
from ..Simulator import Simulator
from ..Coordinate import Coordinate4D, Coordinate2D
from ..Owner import Owner, PathStop

if TYPE_CHECKING:
    from .MapTile import MapTile
    from ..Allocator import Allocator
    from ..Environment import Environment
    from API import OwnerType


class Generator:
    def __init__(
        self,
        name: str,
        description: str,
        owners: List["OwnerType"],
        dimensions: "Coordinate4D",
        maptiles: List["MapTile"]
    ):
        self.name: str = name
        self.description: str = description
        self.ownerTypes: List[OwnerType] = owners
        self.dimensions: "Coordinate4D" = dimensions
        self.owners: List["Owner"] = []
        self.allocator: "Allocator" = FCFSAllocator()
        self.environment: "Environment" = EnvironmentGen(self.dimensions, maptiles).generate(10)
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History"] = None
        self.statistics: Optional[Statistics] = None
        self.simulator: Optional[Simulator] = None

    @staticmethod
    def extract_owner_stops(owner: "OwnerType"):
        stops: List[PathStop] = []
        for stop in owner.stops:
            if stop.type == "random":
                stops.append(PathStop(stop.type))
            elif stop.type == "position":
                x_str, z_str = stop.position.split("_")
                stops.append(PathStop(stop.type, position=Coordinate2D(int(x_str), int(z_str))))
            elif stop.type == "heatmap":
                heat_dict: Dict[float, List[Coordinate2D]] = {}
                for key in stop.heatmap:
                    float_key: float = float(key.replace("_", "."))
                    coordinates: List[Coordinate2D] = []
                    for coord_str in stop.heatmap[key]:
                        x_str, z_str = coord_str.split("_")
                        coordinates.append(Coordinate2D(int(x_str), int(z_str)))
                    heat_dict[float_key] = coordinates
                stops.append(PathStop(stop.type, heatmap=heat_dict))
        return stops

    def simulate(self):
        for ownerType in self.ownerTypes:
            stops: List["PathStop"] = self.extract_owner_stops(ownerType)
            if ownerType.type == "ab":
                self.owners.append(ABOwner(ownerType.name,
                                           ownerType.color,
                                           stops,
                                           self.creation_ticks(self.environment.get_dim().t, ownerType.agents)))
            elif ownerType.type == "aba":
                self.owners.append(ABAOwner(ownerType.name,
                                            ownerType.color,
                                            stops,
                                            self.creation_ticks(self.environment.get_dim().t, ownerType.agents)))
            elif ownerType.type == "abc":
                self.owners.append(ABCOwner(ownerType.name,
                                            ownerType.color,
                                            stops,
                                            self.creation_ticks(self.environment.get_dim().t, ownerType.agents)))
            elif ownerType.type == "stat":
                self.owners.append(
                    StationaryOwner(ownerType.name,
                                    ownerType.color,
                                    self.creation_ticks(self.environment.get_dim().t, ownerType.agents)))


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

    @staticmethod
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
            next = max(int(round(random.gauss(expected, std))), 0)
            res.extend(next*[i])
            sum += next
        next_1 = max(int((total-sum)/2), 0)
        res.extend(next_1 * [duration - 2])
        sum += next_1
        next_2 = max(total - sum, 0)
        res.extend(next_2* [duration - 1])
        sum += next_2
        return res
