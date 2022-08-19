import random
from typing import List, Optional, TYPE_CHECKING, Dict

from Simulator.Coordinates import Coordinate4D, Coordinate2D
from Simulator.History import History
from Simulator.Owners import Owner, GridLocation, GridLocationType
from Simulator.Owners.Heatmap import Heatmap
from Simulator.Owners.HeatmapType import HeatmapType
from Simulator.Simulator import Simulator
from Simulator.Statistics.Statistics import Statistics
from .EnvironmentGen import EnvironmentGen

if TYPE_CHECKING:
    from .MapTile import MapTile
    from Simulator.Allocator import Allocator
    from Simulator.Environment import Environment
    from API.API import APIOwner


class Generator:
    def __init__(
        self,
        owners: List["APIOwner"],
        dimensions: "Coordinate4D",
        maptiles: List["MapTile"],
        allocator: "Allocator"
    ):
        self.apiOwners: List["APIOwner"] = owners
        self.dimensions: "Coordinate4D" = dimensions
        self.owners: List["Owners"] = []
        self.allocator: "Allocator" = allocator
        self.environment: "Environment" = EnvironmentGen(self.dimensions, maptiles).generate()
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History"] = None
        self.statistics: Optional[Statistics] = None
        self.simulator: Optional[Simulator] = None

    @staticmethod
    def extract_owner_stops(owner: "APIOwner"):
        stops: List[GridLocation] = []
        for location in owner.locations:
            if location.type == GridLocationType.RANDOM.value:
                stops.append(GridLocation(str(GridLocationType.RANDOM.value)))
            elif location.type == GridLocationType.POSITION.value:
                stops.append(GridLocation(str(GridLocationType.POSITION.value),
                                          position=Coordinate2D(location.gridCoordinates[0].x,
                                                                location.gridCoordinates[0].y)))
            elif location.type == GridLocationType.HEATMAP.value:
                heat_dict: Dict[float, List[Coordinate2D]] = {}
                for gridCoord in location.gridCoordinates:
                    coordinate = Coordinate2D(gridCoord.x, gridCoord.y)
                    if gridCoord.value in heat_dict:
                        heat_dict[gridCoord.value].append(coordinate)
                    else:
                        heat_dict[gridCoord.value] = [coordinate]
                stops.append(GridLocation(str(GridLocationType.HEATMAP.value),
                                          heatmap=Heatmap(str(HeatmapType.INVERSE_SPARSE.value),
                                                          inverse_sparse=heat_dict)))
        return stops

    def simulate(self):
        for apiOwner in self.apiOwners:
            stops: List["GridLocation"] = self.extract_owner_stops(apiOwner)
            owners = [_owner for _owner in self.allocator.compatible_owner() if _owner.__name__ == apiOwner.classname]
            if len(owners) != 1:
                print(f"Owners Type {apiOwner} not registered with allocator {self.allocator.__class__.__name__}")
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
