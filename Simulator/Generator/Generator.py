import random
from typing import List, Optional, TYPE_CHECKING, Dict

from FCFSAllocator.FCFSAllocator import FCFSAllocator
from .EnvironmentGen import EnvironmentGen
from ..Owner.Heatmap import Heatmap
from ..Owner.HeatmapType import HeatmapType
from ..Owner.OwnerType import OwnerType
from ..Owner.PathOwners.ABAOwner import ABAOwner
from ..Owner.PathOwners.ABCOwner import ABCOwner
from ..Owner.PathOwners.ABOwner import ABOwner
from ..Owner.SpaceOwners.StationaryOwner import StationaryOwner
from ..Statistics.Statistics import Statistics
from ..History import History
from ..Simulator import Simulator
from ..Coordinate import Coordinate4D, Coordinate2D
from ..Owner import Owner, PathStop, StopType

if TYPE_CHECKING:
    from .MapTile import MapTile
    from ..Allocator import Allocator
    from ..Environment import Environment
    from API import APIOwner


class Generator:
    def __init__(
        self,
        name: str,
        description: str,
        owners: List["APIOwner"],
        dimensions: "Coordinate4D",
        maptiles: List["MapTile"],
        allocator: "Allocator"
    ):
        self.name: str = name
        self.description: str = description
        self.ownerTypes: List[APIOwner] = owners
        self.dimensions: "Coordinate4D" = dimensions
        self.owners: List["Owner"] = []
        self.allocator: "Allocator" = allocator
        self.environment: "Environment" = EnvironmentGen(self.dimensions, maptiles).generate()
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History"] = None
        self.statistics: Optional[Statistics] = None
        self.simulator: Optional[Simulator] = None

    @staticmethod
    def extract_owner_stops(owner: "APIOwner"):
        stops: List[PathStop] = []
        for stop in owner.stops:
            if stop.type == StopType.RANDOM.value:
                stops.append(PathStop(StopType.RANDOM.value))
            elif stop.type == StopType.POSITION.value:
                x_str, z_str = stop.position.split("_")
                stops.append(PathStop(StopType.POSITION.value, position=Coordinate2D(int(x_str), int(z_str))))
            elif stop.type == StopType.HEATMAP.value:
                heat_dict: Dict[float, List[Coordinate2D]] = {}
                for key in stop.heatmap:
                    float_key: float = float(key.replace("_", "."))
                    coordinates: List[Coordinate2D] = []
                    for coord_str in stop.heatmap[key]:
                        x_str, z_str = coord_str.split("_")
                        coordinates.append(Coordinate2D(int(x_str), int(z_str)))
                    heat_dict[float_key] = coordinates
                stops.append(PathStop(StopType.HEATMAP.value, heatmap=Heatmap(HeatmapType.INVERSE_SPARSE.value, inverse_sparse=heat_dict)))
        return stops

    def simulate(self):
        for ownerType in self.ownerTypes:
            stops: List["PathStop"] = self.extract_owner_stops(ownerType)
            owners = [_owner for _owner in self.allocator.compatible_owner() if _owner.__name__ == ownerType.type]
            if len(owners) != 1:
                print(f"Owner Type {ownerType} not registered with allocator {self.allocator.__name__}")
                continue
            ownerClass = owners[0]
            print(ownerClass.__name__)
            print(stops)
            self.owners.append(ownerClass(ownerType.name,
                                          ownerType.color,
                                          stops,
                                          self.creation_ticks(self.environment.allocation_period, ownerType.agents)))

        self.simulator = Simulator(
            self.owners,
            self.allocator,
            self.environment,
        )
        while self.simulator.time_step <= self.dimensions.t:
            print(f"STEP: {self.simulator.time_step}")
            self.simulator.tick()

    @staticmethod
    def creation_ticks(duration, total) -> List[int]:
        res = []
        for _ in range(total):
            res.append(random.randint(0, duration - 1))

        return res
