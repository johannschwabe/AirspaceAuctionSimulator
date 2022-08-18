from typing import TYPE_CHECKING, Optional, Set

from AAS.AStar.Node import Node

if TYPE_CHECKING:
    from Demos.Priority.Agents.PriorityABAgent import PriorityABAgent
    from AAS.Coordinates import Coordinate4D


class PriorityNode(Node):
    def __init__(self, position: "Coordinate4D", parent: Optional["PriorityNode"], collisions: Set["PriorityABAgent"]):
        super().__init__(position, parent, collisions)
