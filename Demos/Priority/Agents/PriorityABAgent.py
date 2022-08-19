from Simulator import ABAgent, Coordinate4D, Simulator
from Demos.Priority.Bids.PriorityABBid import PriorityABBid


class PriorityABAgent(ABAgent):
    def __init__(self,
                 a: Coordinate4D,
                 b: Coordinate4D,
                 priority: float,
                 simulator: Simulator,
                 agent_id: int | None = None,
                 speed: int | None = None,
                 battery: int | None = None,
                 ):
        super().__init__(a, b, simulator, agent_id=agent_id, speed=speed, battery=battery)
        self.priority = priority

    def get_bid(self, t: int):
        if len(self.allocated_segments) == 0 or self.allocated_segments[0][0].t >= t:
            return PriorityABBid(self.battery, self.a, self.b, self.priority, False)
        start = self.allocated_segments[-1][-1]
        return PriorityABBid(self.battery - (int(t - self.allocated_segments[0][0].t)),
                             start,
                             self.b,
                             self.priority,
                             True)

    def clone(self):
        clone = PriorityABAgent(self.a,
                                self.b,
                                self.priority,
                                self.simulator,
                                agent_id=self.id,
                                speed=self.speed,
                                battery=self.battery)
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone

    def generalized_bid(self):
        return {
            "Prio": self.priority,
            "!value": self.priority
        }
