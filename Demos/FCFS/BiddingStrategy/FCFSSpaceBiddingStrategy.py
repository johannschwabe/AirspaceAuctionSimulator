from Demos.FCFS.Bids.FCFSSpaceBid import FCFSSpaceBid
from Simulator.Agents.SpaceAgent import SpaceAgent
from Simulator.Bids.BiddingStrategy import BiddingStrategy
from Simulator.Environment.Environment import Environment


class FCFSSpaceBiddingStrategy(BiddingStrategy):
    def generate_bid(self, agent: SpaceAgent, _environment: Environment, _time_step: int) -> FCFSSpaceBid:
        return FCFSSpaceBid(agent)
