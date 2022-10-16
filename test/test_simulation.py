import unittest

from API.GridLocation.GridLocation import GridLocation
from API.GridLocation.GridLocationType import GridLocationType
from API.WebClasses import WebPathOwner
from Demos.Priority import PriorityAllocator, PriorityPathBiddingStrategy, PriorityPathValueFunction, \
    PriorityPaymentRule
from Simulator import Coordinate2D, Coordinate3D, Coordinate4D, Environment, Mechanism, Simulator, StaticBlocker


class SimulationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.blockers = [StaticBlocker(Coordinate3D(6, 0, 2), Coordinate3D(3, 1, 3)),
                         StaticBlocker(Coordinate3D(0, 0, 0), Coordinate3D(1, 1, 1))]
        self.env = Environment(Coordinate4D(10, 1, 10, 200), self.blockers)

    def test_tick(self):
        owners = [WebPathOwner("po_1",
                               "Ghettobox",
                               "#123456",
                               [GridLocation(str(GridLocationType.POSITION.value), position=Coordinate2D(3, 3)),
                                GridLocation(str(GridLocationType.POSITION.value), position=Coordinate2D(7, 7))],
                               [3],
                               PriorityPathBiddingStrategy(),
                               PriorityPathValueFunction(),
                               near_radius=1,
                               battery=100,
                               speed=1,
                               config={"priority": 0.1}),
                  WebPathOwner("po_2", "SCHMITTAG", "#654321",
                               [GridLocation(str(GridLocationType.POSITION.value), position=Coordinate2D(6, 7)),
                                GridLocation(str(GridLocationType.POSITION.value), position=Coordinate2D(3, 3))],
                               [4], PriorityPathBiddingStrategy(), PriorityPathValueFunction(), near_radius=1,
                               battery=100, speed=1, config={"priority": 0.2}),
                  WebPathOwner("po_3", "EHHHH", "#999999",
                               [GridLocation(str(GridLocationType.POSITION.value), position=Coordinate2D(1, 8)),
                                GridLocation(str(GridLocationType.POSITION.value), position=Coordinate2D(4, 0))],
                               [5], PriorityPathBiddingStrategy(), PriorityPathValueFunction(), near_radius=1,
                               battery=100, speed=5, config={"priority": 0.2})
                  ]
        mechi = Mechanism(PriorityAllocator(), PriorityPaymentRule(0.02))
        simi = Simulator(owners, mechi, self.env)
        simi.tick()
        self.assertEqual(len(self.env.agents), 0)
        simi.tick()
        simi.tick()
        simi.tick()
        self.assertEqual(len(self.env.agents), 1)
        self.assertIn(Coordinate4D(4, 0, 6, 8), self.env.agents[hash('po_1-0')].allocated_segments[0].coordinates)
        simi.tick()
        self.assertEqual(len(self.env.agents), 2)
        self.assertIn(Coordinate4D(4, 0, 6, 8), self.env.agents[hash('po_2-0')].allocated_segments[0].coordinates)
        self.assertNotIn(Coordinate4D(4, 0, 6, 8), self.env.agents[hash('po_1-0')].allocated_segments[0].coordinates)
        simi.tick()
        self.assertEqual(len(self.env.agents), 3)
