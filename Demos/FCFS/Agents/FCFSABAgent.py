from AAS import ABAgent
from Demos.FCFS.Bids.FCFSABBid import FCFSABBid


class FCFSABAgent(ABAgent):
    def __init__(
        self,
        a,
        b,
        simulator,
        agent_id=None,
        speed=None,
        battery=None,
        near_radius=None,
        far_radius=None,
    ):
        super().__init__(a,
                         b,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius,
                         far_radius=far_radius)

    def get_bid(self, _):
        return FCFSABBid(self.battery, self.a, self.b)

    def initialize_clone(self):
        clone = FCFSABAgent(self.a,
                            self.b,
                            self.simulator,
                            agent_id=self.id,
                            speed=self.speed,
                            battery=self.battery,
                            near_radius=self.near_radius)
        return clone
