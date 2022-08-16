from typing import TYPE_CHECKING, List, Optional, Set

from Simulator.Coordinate import Coordinate4D

if TYPE_CHECKING:
    from Simulator.Agent import PathAgent
    from Simulator.Coordinate import Coordinate3D


class Node:
    def __init__(self, position: "Coordinate4D", parent: Optional["Node"], collisions: Set["PathAgent"]):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost
        self.collisions: Set["PathAgent"] = collisions

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return f"{self.position}: {self.f}, {self.h}"

    def adjacent_coordinates(self, dim: "Coordinate3D", speed: int) -> List["Coordinate4D"]:
        res = [Coordinate4D(self.position.x, self.position.y, self.position.z,
                            self.position.t + speed)]
        if self.position.x > 0:
            res.append(Coordinate4D(self.position.x - 1, self.position.y, self.position.z,
                                    self.position.t + speed))
        if self.position.y > 0:
            res.append(Coordinate4D(self.position.x, self.position.y - 1, self.position.z,
                                    self.position.t + speed))
        if self.position.z > 0:
            res.append(Coordinate4D(self.position.x, self.position.y, self.position.z - 1,
                                    self.position.t + speed))
        if self.position.x < dim.x - 1:
            res.append(Coordinate4D(self.position.x + 1, self.position.y, self.position.z,
                                    self.position.t + speed))
        if self.position.y < dim.y - 1:
            res.append(Coordinate4D(self.position.x, self.position.y + 1, self.position.z,
                                    self.position.t + speed))
        if self.position.z < dim.z - 1:
            res.append(Coordinate4D(self.position.x, self.position.y, self.position.z + 1,
                                    self.position.t + speed))
        return res
