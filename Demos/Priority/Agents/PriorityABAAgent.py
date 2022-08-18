from AAS import ABAAgent
from Demos.Priority.Bids.PriorityABABid import PriorityABABid


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
                 ):
        super().__init__(a, b, simulator, stay=stay, agent_id=agent_id, speed=speed, battery=battery)
        self.priority = priority

    def get_bid(self, t: int):
        if len(self.allocated_segments) == 0 or self.allocated_segments[0][0].t >= t:
            return PriorityABABid(self.battery, self.a, self.b, self.priority, False)
        start = self.allocated_segments[-1][-1]
        return PriorityABABid(self.battery - (int(t - self.allocated_segments[0][0].t)),
                              start,
                              self.b,
                              self.priority,
                              True)

    def clone(self):
        clone = PriorityABAAgent(self.a,
                                 self.b,
                                 self.priority,
                                 self.simulator,
                                 self.stay,
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
