import math
import random
from typing import List, Optional, TYPE_CHECKING, Dict
from .Area import Area
from .EnvironmentGen import EnvironmentGen
from ..Owner.Heatmap import Heatmap
from ..Owner.HeatmapType import HeatmapType
from ..Statistics.Statistics import Statistics
from ..History import History
from ..Simulator import Simulator
from ..Coordinate import Coordinate4D, Coordinate2D
from ..Owner import Owner, GridLocation, GridLocationType

if TYPE_CHECKING:
    from .MapTile import MapTile
    from ..Allocator import Allocator
    from ..Environment import Environment
    from API import APIOwner


class Generator:
    def __init__(
        self,
        owners: List["APIOwner"],
        dimensions: "Coordinate4D",
        maptiles: List["MapTile"],
        allocator: "Allocator",
        area: "Area"
    ):
        self.apiOwners: List["APIOwner"] = owners
        self.dimensions: "Coordinate4D" = dimensions
        self.owners: List["Owner"] = []
        self.allocator: "Allocator" = allocator
        self.environment: "Environment" = EnvironmentGen(self.dimensions, maptiles).generate()
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History"] = None
        self.statistics: Optional[Statistics] = None
        self.simulator: Optional[Simulator] = None
        self.area = area

    def extract_owner_stops(self, owner: "APIOwner"):
        stops: List[GridLocation] = []
        for location in owner.locations:
            if location.type == GridLocationType.RANDOM.value:
                stops.append(GridLocation(str(GridLocationType.RANDOM.value)))
            elif location.type == GridLocationType.POSITION.value:
                gridCoord = self.area.point_to_coordinate2D(location.points[0])
                stops.append(GridLocation(str(GridLocationType.POSITION.value),
                             position=gridCoord))
            elif location.type == GridLocationType.HEATMAP.value:
                heat_dict: Dict[float, List[Coordinate2D]] = {}
                for point in location.points:
                    coordinate = self.area.point_to_coordinate2D(point)
                    if point.value in heat_dict:
                        heat_dict[point.value].append(coordinate)
                    else:
                        heat_dict[point.value] = [coordinate]
                stops.append(GridLocation(str(GridLocationType.HEATMAP.value),
                                          heatmap=Heatmap(str(HeatmapType.INVERSE_SPARSE.value),
                                          inverse_sparse=heat_dict)))
        return stops

    def simulate(self):
        for apiOwner in self.apiOwners:
            stops: List["GridLocation"] = self.extract_owner_stops(apiOwner)
            owners = [_owner for _owner in self.allocator.compatible_owner() if _owner.__name__ == apiOwner.classname]
            if len(owners) != 1:
                print(f"Owner Type {apiOwner} not registered with allocator {self.allocator.__class__.__name__}")
                continue
            ownerClass = owners[0]
            self.owners.append(ownerClass(apiOwner.name,
                                          apiOwner.color,
                                          stops,
                                          self.creation_ticks(self.environment.allocation_period, apiOwner.agents)))

        self.simulator = Simulator(
            self.owners,
            self.allocator,
            self.environment,
        )
        while self.simulator.time_step <= self.dimensions.t:
            self.simulator.tick()

        print(f"DONE!")
        print(f"STEP: {self.simulator.time_step}")

    @staticmethod
    def creation_ticks(duration, total) -> List[int]:
        res = []
        for _ in range(total):
            res.append(random.randint(0, duration - 1))

        return res
