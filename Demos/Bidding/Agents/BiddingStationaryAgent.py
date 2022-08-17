from typing import List, TYPE_CHECKING

from Demos.Bidding.Bids.BiddingStationaryBid import BiddingStationaryBid
from AAS.Agent import StationaryAgent, Agent
from AAS.Bid import Bid

if TYPE_CHECKING:
    from AAS.Coordinates import Coordinate4D


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
