from Demos.Priority.Bids.PriorityStationaryBid import PriorityStationaryBid
from Simulator import StationaryAgent


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

    def initialize_clone(self):
        clone = PriorityStationaryAgent(self.blocks, self.priority, self.simulator, agent_id=self.id)
        return clone
