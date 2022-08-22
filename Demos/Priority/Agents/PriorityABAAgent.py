from Demos.Priority.Bids.PriorityABABid import PriorityABABid
from Simulator import ABAAgent


class PriorityABAAgent(ABAAgent):

    def __init__(self,
                 a,
                 b,
                 priority,
                 simulator,
                 stay,
                 agent_id=None,
                 speed=None,
                 battery=None,
                 near_radius=None):
        super().__init__(a,
                         b,
                         stay,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)
        self.priority = priority

    def get_bid(self, t: int):
        # TODO
        if len(self.allocated_segments) == 0 or self.allocated_segments[0].min.t >= t:
            return PriorityABABid(self.battery, self.a, self.b, self.priority, False, self.stay)
        start = self.allocated_segments[-1].max
        return PriorityABABid(self.battery - (int(t - self.allocated_segments[0].min.t)),
                              start,
                              self.b,
                              self.priority,
                              True,
                              self.stay)

    def initialize_clone(self):
        clone = PriorityABAAgent(self.a,
                                 self.b,
                                 self.priority,
                                 self.simulator,
                                 self.stay,
                                 agent_id=self.id,
                                 speed=self.speed,
                                 battery=self.battery,
                                 near_radius=self.near_radius)
        return clone
