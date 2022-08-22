from Demos.Priority.Bids.PriorityABBid import PriorityABBid
from Simulator import ABAgent


class PriorityABAgent(ABAgent):
    def __init__(self,
                 a,
                 b,
                 priority,
                 simulator,
                 agent_id=None,
                 speed=None,
                 battery=None,
                 near_radius=None):
        super().__init__(a,
                         b,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)
        self.priority = priority

    def get_bid(self, t: int):
        if len(self.allocated_segments) == 0 or self.allocated_segments[0].min.t >= t:
            return PriorityABBid(self.battery, self.a, self.b, self.priority, False)
        start = self.allocated_segments[-1].max
        return PriorityABBid(self.battery - (int(t - self.allocated_segments[0].min.t)),
                             start,
                             self.b,
                             self.priority,
                             True)

    def initialize_clone(self):
        clone = PriorityABAgent(self.a,
                                self.b,
                                self.priority,
                                self.simulator,
                                agent_id=self.id,
                                speed=self.speed,
                                battery=self.battery,
                                near_radius=self.near_radius)
        return clone
