from Simulator import ABCAgent
from Demos.Priority.Bids.PriorityABCBid import PriorityABCBid


class PriorityABCAgent(ABCAgent):
    def __init__(self,
                 locations,
                 priority,
                 simulator,
                 stays,
                 agent_id=None,
                 speed=None,
                 battery=None,
                 near_radius=None,
                 ):
        super().__init__(locations, stays, simulator, agent_id=agent_id, speed=speed, battery=battery,
                         near_radius=near_radius)
        self.priority = priority

    def get_bid(self, t: int):
        flying = False  # TODO
        return PriorityABCBid(self.battery, self.locations, self.stays, self.priority, flying)

    def clone(self):
        clone = PriorityABCAgent(self.locations,
                                 self.priority,
                                 self.simulator,
                                 self.stays,
                                 agent_id=self.id,
                                 speed=self.speed,
                                 battery=self.battery,
                                 near_radius=self.near_radius)
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone

    def generalized_bid(self):
        return {
            "Prio": self.priority,
            "!value": self.priority
        }
