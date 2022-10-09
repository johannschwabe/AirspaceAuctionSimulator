from abc import ABC
from typing import List, TYPE_CHECKING, Dict, Any, Optional

from ..Agents.AgentType import AgentType
from ..Owners.Owner import Owner

if TYPE_CHECKING:
    from ..Location.GridLocation import GridLocation
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class PathOwner(Owner, ABC):
    allocation_type: str = AgentType.PATH.value
    min_locations = 2
    max_locations = 100
    meta = []

    def __init__(self, owner_id: str,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 near_radius: float,
                 battery: int,
                 speed: int,
                 meta: Optional[Dict[str, Any]] = None):
        super().__init__(owner_id, bidding_strategy, value_function, creation_ticks, name, color, meta if meta else {})
        assert near_radius >= 1
        self.stops = stops
        self.near_radius = near_radius
        self.battery = battery
        self.speed = speed
