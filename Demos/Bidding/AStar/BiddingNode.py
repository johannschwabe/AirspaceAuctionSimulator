from typing import TYPE_CHECKING, Optional, Set

from AAS.AStar.Node import Node

if TYPE_CHECKING:
    from Demos.Bidding.Agents.BiddingABAgent import BiddingABAgent
    from AAS.Coordinates import Coordinate4D


class BiddingNode(Node):
    def __init__(self, position: "Coordinate4D", parent: Optional["BiddingNode"], collisions: Set["BiddingABAgent"]):
        super().__init__(position, parent, collisions)
