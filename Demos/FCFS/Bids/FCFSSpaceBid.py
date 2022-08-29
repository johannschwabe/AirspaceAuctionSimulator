from Simulator import Bid, SpaceAgent


class FCFSSpaceBid(Bid):
    def __init__(self, agent: "SpaceAgent"):
        super().__init__(agent)

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return True
