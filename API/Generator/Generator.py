import random
from typing import List, Optional, TYPE_CHECKING, Dict

from Simulator import PathOwner, SpaceOwner, GridLocationType, GridLocation, Heatmap, HeatmapType, Simulator, Mechanism, \
    Coordinate4D
from .EnvironmentGen import EnvironmentGen

if TYPE_CHECKING:
    from .MapTile import MapTile
    from Simulator import Allocator, Owner, Environment, History, Statistics, PaymentRule, Coordinate2D
    from ..API import APIOwner
    from ..Area import Area


class Generator:
    def __init__(
        self,
        owners: List["APIOwner"],
        dimensions: "Coordinate4D",
        maptiles: List["MapTile"],
        allocator: "Allocator",
        map_playfield_area: "Area",
        payment_rule: "PaymentRule",
        allocation_period: int = 50
    ):
        self.api_owners: List["APIOwner"] = owners
        self.dimensions: "Coordinate4D" = dimensions
        self.owners: List["Owner"] = []
        self.allocator: "Allocator" = allocator
        self.environment: "Environment" = EnvironmentGen(self.dimensions, maptiles,
                                                         min_height=map_playfield_area.min_height,
                                                         allocation_period=allocation_period,
                                                         map_playfield_area=map_playfield_area).generate()
        self.simulator: Optional["Simulator"] = None
        self.history: Optional["History"] = None
        self.statistics: Optional["Statistics"] = None
        self.simulator: Optional["Simulator"] = None
        self.map_playfield_area = map_playfield_area
        self.payment_rule = payment_rule

    def extract_owner_stops(self, owner: "APIOwner"):
        stops: List["GridLocation"] = []
        for location in owner.locations:
            if location.type == GridLocationType.RANDOM.value:
                stops.append(GridLocation(str(GridLocationType.RANDOM.value)))
            elif location.type == GridLocationType.POSITION.value:
                gridCoord = self.map_playfield_area.point_to_coordinate2D(location.points[0])
                stops.append(GridLocation(str(GridLocationType.POSITION.value),
                                          position=gridCoord))
            elif location.type == GridLocationType.HEATMAP.value:
                heat_dict: Dict[float, List["Coordinate2D"]] = {}
                for point in location.points:
                    coordinate = self.map_playfield_area.point_to_coordinate2D(point)
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
        for apiOwner in self.api_owners:
            stops: List["GridLocation"] = self.extract_owner_stops(apiOwner)
            bidding_strategy = [bs for bs in self.allocator.compatible_bidding_strategies() if
                                bs.__name__ == apiOwner.biddingStrategy.classname]
            if len(bidding_strategy) != 1:
                raise Exception(f"{len(bidding_strategy)} bidding strategies found")
            selected_bidding_strategy = bidding_strategy[0]()

            print(apiOwner.valueFunction)
            value_functions = [vf for vf in selected_bidding_strategy.compatible_value_functions() if
                               vf.__name__ == apiOwner.valueFunction]
            if len(value_functions) != 1:
                raise Exception(f"{len(value_functions)} bidding strategies found")
            selected_value_functions = value_functions[0]()

            if apiOwner.biddingStrategy.allocationType == "space":
                dim_x = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                         meta_config["key"] == "size_x"][0]
                dim_y = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                         meta_config["key"] == "size_y"][0]
                dim_z = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                         meta_config["key"] == "size_z"][0]
                dim_t = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                         meta_config["key"] == "size_t"][0]
                other_meta_config = {meta_config["key"]: meta_config["value"] for meta_config in
                                     apiOwner.biddingStrategy.meta if
                                     meta_config["key"] not in ["size_x", "size_y", "size_z", "size_t"]}
                newOwner = SpaceOwner(str(owner_id),
                                      apiOwner.name,
                                      apiOwner.color,
                                      stops,
                                      self.creation_ticks(self.environment.allocation_period, apiOwner.agents),
                                      bidding_strategy=selected_bidding_strategy,
                                      value_function=selected_value_functions,
                                      size=Coordinate4D(dim_x, dim_y, dim_z, dim_t),
                                      meta=other_meta_config)
            else:
                near_field = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                              meta_config["key"] == "near_field"][0]
                battery = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                           meta_config["key"] == "battery"][0]
                speed = [meta_config["value"] for meta_config in apiOwner.biddingStrategy.meta if
                         meta_config["key"] == "speed"][0]
                other_meta_config = {meta_config["key"]: meta_config["value"] for meta_config in
                                     apiOwner.biddingStrategy.meta if
                                     meta_config["key"] not in ["near_field", "speed", "battery"]}
                newOwner = PathOwner(str(owner_id),
                                     apiOwner.name,
                                     apiOwner.color,
                                     stops,
                                     self.creation_ticks(self.environment.allocation_period, apiOwner.agents),
                                     bidding_strategy=selected_bidding_strategy,
                                     value_function=selected_value_functions,
                                     near_radius=near_field,
                                     battery=battery,
                                     speed=speed,
                                     meta=other_meta_config
                                     )
            self.owners.append(newOwner)
            owner_id += 1
        mech = Mechanism(self.allocator, self.payment_rule)
        self.simulator = Simulator(
            self.owners,
            mech,
            self.environment,
        )
        while self.simulator.tick():
            pass

        print(f"DONE!")
        print(f"STEP: {self.simulator.time_step}")

    @staticmethod
    def creation_ticks(duration, total) -> List[int]:
        # return [1] * total
        res = []
        for _ in range(total):
            res.append(random.randint(0, duration - 1))

        return res
