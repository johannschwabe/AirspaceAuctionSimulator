from Simulator import ABABid


class FCFSABABid(ABABid):
    def __init__(self, battery, a, b, stay):
        super().__init__(battery, a, b, stay)
