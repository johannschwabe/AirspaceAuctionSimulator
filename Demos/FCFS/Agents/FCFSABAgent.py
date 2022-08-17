from AAS import ABAgent, Coordinate4D, Simulator
from Demos.FCFS.Bids.FCFSABBid import FCFSABBid


class FCFSABAgent(ABAgent):
    def __init__(
        self,
        a: Coordinate4D,
        b: Coordinate4D,
        simulator: Simulator,
        agent_id: int | None = None,
        speed: int | None = None,
        battery: int | None = None,
        near_radius: int | None = None,
    ):
        super().__init__(a,
                         b,
                         simulator,
                         agent_id=agent_id,
                         speed=speed,
                         battery=battery,
                         near_radius=near_radius)

    def get_bid(self) -> FCFSABBid:
        return FCFSABBid(self.battery, self.a, self.b)

    def clone(self):
        clone = FCFSABAgent(self.a,
                            self.b,
                            self.simulator,
                            agent_id=self.agent_id,
                            speed=self.speed,
                            battery=self.battery,
                            near_radius=self.near_radius)
        clone.allocated_segments = [segment.clone() for segment in self.allocated_segments]
        return clone
