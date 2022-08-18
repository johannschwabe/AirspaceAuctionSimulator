from AAS import StationaryAgent
from Demos.Priority.Bids.PriorityStationaryBid import PriorityStationaryBid


class PriorityStationaryAgent(StationaryAgent):
    def __init__(
        self,
        blocks,
        priority,
        simulator,
        agent_id=None
    ):
        super().__init__(blocks, simulator, agent_id=agent_id)
        self.priority = priority

    def get_bid(self, t: int):
        return PriorityStationaryBid(self.blocks, self.priority)

    def clone(self):
        clone = PriorityStationaryAgent(self.blocks, self.priority, self.simulator, agent_id=self.id)
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone

    def generalized_bid(self):
        return {
            "Prio": self.priority,
            "!value": self.priority
        }
