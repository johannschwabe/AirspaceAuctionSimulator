import math
from typing import Dict, List, TYPE_CHECKING

from .Coordinate2D import Coordinate2D

if TYPE_CHECKING:
    from .Coordinate4D import Coordinate4D


class Coordinate3D(Coordinate2D):

    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, z)
        self.y: int = y

    def to_dict(self) -> Dict[str, int]:
        return {"x": self.x, "y": self.y, "z": self.z}

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and \
               self.y == other.y and \
               self.z == other.z

    def __add__(self, other) -> "Coordinate3D":
        return Coordinate3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other) -> "Coordinate3D":
        return Coordinate3D(self.x - other.x, self.y - other.y, self.z - other.z)

    @property
    def l1(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def l2(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def volume(self) -> int:
        return self.x * self.y * self.z

    def to_2D(self) -> Coordinate2D:
        return Coordinate2D(self.x, self.z)

    def distance(self, other: "Coordinate3D", l2: bool = False) -> float:
        if l2:
            return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5
        else:
            return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def distance_block(self, block: List["Coordinate4D"]) -> float:
        front = block[0].x - self.x > 0
        below = block[0].y - self.y > 0
        left = block[0].z - self.z > 0
        behind = block[1].x - self.x < 0
        above = block[1].y - self.y < 0
        right = block[1].z - self.z < 0
        same_x = not front and not behind
        same_y = not above and not below
        same_z = not left and not right
        distance: float = 0.0
        if front and below and left:  # Bottom left below
            distance = Coordinate3D.distance(self, block[0], l2=True)

        if front and above and left:  # Bottom left above
            distance = Coordinate3D.distance(self, Coordinate3D(block[0].x, block[1].y, block[0].z), l2=True)

        if front and same_y and left:  # Bottom left same
            distance = self.to_2D().distance(Coordinate2D(block[0].x, block[0].z), l2=True)

        if front and below and right:  # Bottom right below
            distance = Coordinate3D.distance(self, Coordinate3D(block[0].x, block[0].y, block[1].z), l2=True)

        if front and above and right:  # Bottom right above
            distance = Coordinate3D.distance(self, Coordinate3D(block[0].x, block[1].y, block[1].z), l2=True)

        if front and same_y and right:  # Bottom right same
            distance = self.to_2D().distance(Coordinate2D(block[0].x, block[1].z), l2=True)

        if behind and below and left:  # Top left below
            distance = Coordinate3D.distance(self, Coordinate3D(block[1].x, block[0].y, block[0].z), l2=True)

        if behind and above and left:  # Top left above
            distance = Coordinate3D.distance(self, Coordinate3D(block[1].x, block[1].y, block[0].z), l2=True)

        if behind and same_y and left:  # Top left same
            distance = self.to_2D().distance(Coordinate2D(block[1].x, block[0].z), l2=True)

        if behind and below and right:  # Top right below
            distance = Coordinate3D.distance(self, Coordinate3D(block[1].x, block[0].y, block[1].z), l2=True)

        if behind and above and right:  # Top right above
            distance = Coordinate3D.distance(self, Coordinate3D(block[1].x, block[1].y, block[1].z), l2=True)

        if behind and same_y and right:  # Top right same
            distance = self.to_2D().distance(Coordinate2D(block[1].x, block[1].z), l2=True)

        if same_x and above and left:  # Left side above
            distance = Coordinate2D(self.y, self.z).distance(Coordinate2D(block[1].y, block[0].z))

        if same_x and below and left:  # Left side below
            distance = Coordinate2D(self.y, self.z).distance(Coordinate2D(block[0].y, block[0].z))

        if same_x and same_y and left:  # Left side same
            distance = block[0].z - self.z

        if same_x and above and right:  # Right side above
            distance = Coordinate2D(self.y, self.z).distance(Coordinate2D(block[1].y, block[1].z))

        if same_x and below and right:  # Right side below
            distance = Coordinate2D(self.y, self.z).distance(Coordinate2D(block[0].y, block[1].z))

        if same_x and same_y and right:  # Right side same
            distance = self.z - block[1].z

        if front and above and same_z:  # front side above
            distance = Coordinate2D(self.x, self.y).distance(Coordinate2D(block[0].x, block[1].y))

        if front and below and same_z:  # front side below
            distance = Coordinate2D(self.x, self.y).distance(Coordinate2D(block[0].x, block[0].y))

        if front and same_y and same_z:  # front side same
            distance = block[0].x - self.x

        if behind and above and same_z:  # behind side above
            distance = Coordinate2D(self.x, self.y).distance(Coordinate2D(block[1].x, block[1].y))

        if behind and below and same_z:  # front side below
            distance = Coordinate2D(self.x, self.y).distance(Coordinate2D(block[1].x, block[0].y))

        if behind and same_y and same_z:  # front side same
            distance = self.x - block[1].x

        if same_x and above and same_z:  # above same
            distance = self.y - block[1].y

        if same_x and below and same_z:  # above same
            distance = block[0].y - self.y

        if same_x and same_y and same_z:  # contained
            distance = 0
        return distance

    def clone(self) -> "Coordinate3D":
        return Coordinate3D(self.x, self.y, self.z)
