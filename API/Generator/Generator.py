import random
from typing import List, Optional, TYPE_CHECKING, Dict

from Demos.FCFS import FCFSAllocator, FCFSPaymentRule
from Demos.Priority import PriorityAllocator, PriorityPaymentRule
from Simulator import GridLocationType, Coordinate2D, GridLocation, Heatmap, HeatmapType, Simulator, Mechanism, \
    Coordinate4D
from .EnvironmentGen import EnvironmentGen

if TYPE_CHECKING:
    from .MapTile import MapTile
    from Simulator import Allocator, Owner, Environment, History, Statistics
    from ..API import APIOwner
    from ..Area import Area


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
        self.statistics: Optional["Statistics"] = None
        self.simulator: Optional["Simulator"] = None
        self.area = area

    def extract_owner_stops(self, owner: "APIOwner"):
        stops: List["GridLocation"] = []
        for location in owner.locations:
            if location.type == GridLocationType.RANDOM.value:
                stops.append(GridLocation(str(GridLocationType.RANDOM.value)))
            elif location.type == GridLocationType.POSITION.value:
                gridCoord = self.area.point_to_coordinate2D(location.points[0])
                stops.append(GridLocation(str(GridLocationType.POSITION.value),
                                          position=gridCoord))
            elif location.type == GridLocationType.HEATMAP.value:
                heat_dict: Dict[float, List["Coordinate2D"]] = {}
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
        owner_id = 0
        for apiOwner in self.apiOwners:
            stops: List["GridLocation"] = self.extract_owner_stops(apiOwner)
            owners = [_owner for _owner in self.allocator.compatible_owner() if _owner.__name__ == apiOwner.classname]
            if len(owners) != 1:
                print(f"Owner Type {apiOwner} not registered with allocator {self.allocator.__class__.__name__}")
                continue
            ownerClass = owners[0]
            try:
                self.owners.append(ownerClass(owner_id,
                                              apiOwner.name,
                                              apiOwner.color,
                                              stops,
                                              self.creation_ticks(self.environment.allocation_period, apiOwner.agents)))
            except TypeError:
                self.owners.append(ownerClass(owner_id,
                                              apiOwner.name,
                                              apiOwner.color,
                                              stops,
                                              self.creation_ticks(self.environment.allocation_period, apiOwner.agents),
                                              Coordinate4D(50, 50, 50, 50)))
            finally:
                owner_id += 1

        if isinstance(self.allocator, FCFSAllocator):
            mechanism = Mechanism(self.allocator, FCFSPaymentRule())

        elif isinstance(self.allocator, PriorityAllocator):
            mechanism = Mechanism(self.allocator, PriorityPaymentRule())
        else:
            raise Exception("Invalid allocator")

        self.simulator = Simulator(
            self.owners,
            mechanism,
            self.environment,
        )
        while self.simulator.tick():
            pass

        print(f"DONE!")
        print(f"STEP: {self.simulator.time_step}")

    @staticmethod
    def creation_ticks(duration, total) -> List[int]:
        res = []
        for _ in range(total):
            res.append(random.randint(0, duration - 1))

        return res
