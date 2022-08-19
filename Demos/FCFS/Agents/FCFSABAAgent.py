from Simulator import ABAAgent
from Demos.FCFS.Bids.FCFSABABid import FCFSABABid


class FCFSABAAgent(ABAAgent):
    def __init__(
        self,
        a,
        b,
        stay,
        simulator,
        agent_id=None,
        speed=None,
        battery=None,
        near_radius=None,
        far_radius=None
    ):
        super().__init__(a,
                         b,
                         stay,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius,
                         far_radius=far_radius)

    def get_bid(self, _):
        return FCFSABABid(self.battery, self.a, self.b, self.stay)

    def initialize_clone(self):
        clone = FCFSABAAgent(self.a,
                             self.b,
                             self.stay,
                             self.simulator,
                             agent_id=self.id,
                             speed=self.speed,
                             battery=self.battery,
                             near_radius=self.near_radius,
                             far_radius=self.far_radius)
        return clone
