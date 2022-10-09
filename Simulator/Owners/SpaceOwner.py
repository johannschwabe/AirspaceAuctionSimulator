from abc import ABC
from typing import List, TYPE_CHECKING, Dict, Any, Optional

from .Owner import Owner

if TYPE_CHECKING:
    from ..Location.GridLocation import GridLocation
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class SpaceOwner(Owner, ABC):
    def __init__(self,
                 owner_id: str,
                 name: str,
                 color: str,
                 stops: List["GridLocation"],
                 creation_ticks: List[int],
                 size: "Coordinate4D",
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 meta: Optional[Dict[str, Any]] = None):
        super().__init__(owner_id, bidding_strategy, value_function, creation_ticks, name, color, meta if meta else {})
        self.stops = stops
        self.size: "Coordinate4D" = size
