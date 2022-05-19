from typing import Optional

from BiddingAllocator.BiddingABBid import BiddingABBid
from Simulator.Agent import ABAgent, Agent
from Simulator.Coordinate import TimeCoordinate


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

    def get_bid(self) -> BiddingABBid:
        return BiddingABBid(self.battery, self.a, self.b, self.priority)

    def clone(self):
        clone = BiddingABAgent(self.a, self.b, self.priority, self.speed, self.battery)
        clone.id = self.id
        clone.set_allocated_paths([[coord for coord in path] for path in self.get_allocated_paths()])
        clone.is_clone = True
        Agent.id -= 1
        return clone
