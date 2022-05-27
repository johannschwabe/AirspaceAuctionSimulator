from typing import Optional, TYPE_CHECKING

from .BiddingABBid import BiddingABBid
from Simulator.Agent import ABAgent, Agent
from Simulator.Coordinate import TimeCoordinate

if TYPE_CHECKING:
    from Simulator import Tick


class BiddingABAgent(ABAgent):
    def __init__(self,
        a: TimeCoordinate,
        b: TimeCoordinate,
        priority: float,
        speed: Optional[int] = None,
        battery: Optional[int] = None,
    ):
        super().__init__(a,b,speed,battery)
        self.priority = priority

    def get_bid(self, t: "Tick") -> BiddingABBid:
        if len(self._allocated_segments) == 0 or self._allocated_segments[0][0].t >= t:
            return BiddingABBid(self.battery, self.a, self.b, self.priority, False)
        start = self._allocated_segments[0][t - self._allocated_segments[0][0]]
        return BiddingABBid(self.battery - (t - self._allocated_segments[0][0]), start, self.b, self.priority, True)

    def clone(self):
        clone = BiddingABAgent(self.a, self.b, self.priority, self.speed, self.battery)
        clone.id = self.id
        clone.set_allocated_segments([segment.clone() for segment in self.get_allocated_segments()])
        clone.is_clone = True
        Agent._id -= 1
        return clone
