from typing import List, Optional, Set, TYPE_CHECKING

from ..Coordinates.Coordinate4D import Coordinate4D

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Coordinates.Coordinate3D import Coordinate3D


class Node:
    def __init__(self, position: "Coordinate4D", parent: Optional["Node"], collisions: Set["Agent"]):
        self.position: "Coordinate4D" = position
        self.parent: Optional["Node"] = parent
        self.collisions: Set["Agent"] = collisions

        self.g: float = 0  # Distance to start node
        self.h: float = 0  # Distance to target node
        self.f: float = 0  # Total cost

    def __eq__(self, other) -> bool:
        return self.position == other.position

    def __lt__(self, other) -> bool:
        return self.f < other.f

    def __hash__(self) -> int:
        return hash(self.position)

    def __repr__(self) -> str:
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
