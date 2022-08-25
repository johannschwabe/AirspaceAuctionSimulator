from Simulator import Bid, SpaceAgent


class FCFSSpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent"):
        super().__init__(agent)
