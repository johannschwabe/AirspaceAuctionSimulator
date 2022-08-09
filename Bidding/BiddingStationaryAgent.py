from typing import List, TYPE_CHECKING

from Bidding.BiddingStationaryBid import BiddingStationaryBid
from Simulator.Agent import StationaryAgent, Agent
from Simulator.Bid import Bid

if TYPE_CHECKING:
    from Simulator.Coordinate import Coordinate4D


class BiddingStationaryAgent(StationaryAgent):
    def __init__(
        self,
        blocks: List[List["Coordinate4D"]],
        priority: float,
    ):
        super().__init__(blocks)
        self.priority = priority

    def get_bid(self, t: int) -> Bid:
        return BiddingStationaryBid(self.blocks, self.priority)

    def clone(self):
        clone = BiddingStationaryAgent(self.blocks, self.priority)
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.id = self.id
        clone.is_clone = True
        Agent._id -= 1

        return clone

    def generalized_bid(self):
        return {
            "Prio": self.priority,
            "!value": self.priority
        }
