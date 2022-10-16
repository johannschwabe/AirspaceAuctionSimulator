from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from ..Agents.AgentType import AgentType
from ..Owners.Owner import Owner

if TYPE_CHECKING:
    from ..Agents.PathAgent import PathAgent
    from ..Location.GridLocation import GridLocation
    from ..Environment.Environment import Environment
    from ..Coordinates.Coordinate4D import Coordinate4D
    from ..Bids.BiddingStrategy import BiddingStrategy
    from ..ValueFunction.ValueFunction import ValueFunction


class PathOwner(Owner, ABC):
    allocation_type: str = AgentType.PATH.value

    def __init__(self,
                 owner_id: str,
                 bidding_strategy: "BiddingStrategy",
                 value_function: "ValueFunction",
                 config: Optional[Dict[str, Any]] = None):
        super().__init__(owner_id, bidding_strategy, value_function, config)

    @staticmethod
    def generate_stop_coordinate(stop: "GridLocation", env: "Environment", t: int,
                                 near_radius: float) -> "Coordinate4D":
        coord = stop.generate_coordinates(env, t + 1)

        while coord.y < env.min_height or env.is_coordinate_blocked_forever(coord, near_radius):
            coord.y += 1
            if coord.y > env.dimension.y:
                coord.y = env.min_height
                print("BLOCKED")
                break

        return coord

    @abstractmethod
    def generate_agents(self, t: int, environment: "Environment") -> List["PathAgent"]:
        pass
