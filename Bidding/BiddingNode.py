from typing import TYPE_CHECKING, Optional, Set

from Simulator.AStar.Node import Node

if TYPE_CHECKING:
    from Bidding.BiddingABAgent import BiddingABAgent
    from Simulator.Coordinate import Coordinate4D


class BiddingNode(Node):
    def __init__(self, position: "Coordinate4D", parent: Optional["BiddingNode"], collisions: Set["BiddingABAgent"]):
        super().__init__(position, parent, collisions)
