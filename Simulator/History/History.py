from typing import List

from .. import Simulator
from ..Coordinate import Coordinate
from ..Owner import Owner
from ..IO import Stringify
from .EnvironmentGen import Environment


class History(Stringify):

    def __init__(
        self,
        name: str,
        description: str,
        simulator: Simulator,
    ):
        self.name: str = name
        self.description: str = description
        self.dimensions: Coordinate = simulator.environment._dimension
        self.environment: Environment = simulator.environment
        self.owners: List[Owner] = simulator.owners
