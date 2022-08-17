from typing import Optional

from Demos.Bidding.Bids.BiddingABBid import BiddingABBid
from AAS.Agent import ABAgent, Agent
from AAS.Coordinates import Coordinate4D


class BiddingABAgent(ABAgent):
    def __init__(self,
                 a: Coordinate4D,
                 b: Coordinate4D,
                 priority: float,
                 speed: Optional[int] = None,
                 battery: Optional[int] = None,
                 ):
        super().__init__(a, b, speed, battery)
        self.priority = priority

    def get_bid(self, t: int) -> BiddingABBid:
        if len(self._allocated_segments) == 0 or self._allocated_segments[0][0].t >= t:
            return BiddingABBid(self.battery, self.a, self.b, self.priority, False)
        start = self._allocated_segments[-1][-1]
        return BiddingABBid(self.battery - (int(t - self._allocated_segments[0][0].t)),
                            start,
                            self.b,
                            self.priority,
                            True)

    def clone(self):
        clone = BiddingABAgent(self.a, self.b, self.priority, self.speed, self.battery)
        clone.id = self.id
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.is_clone = True
        Agent._id -= 1
        return clone

    def generalized_bid(self):
        return {
            "Prio": self.priority,
            "!value": self.priority
        }
