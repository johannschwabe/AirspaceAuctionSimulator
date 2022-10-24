import random
import unittest

from Demos.FCFS.BidTracker.FCFSBidTracker import FCFSBidTracker
from Demos.FCFS.BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Simulator import AStar, Coordinate3D, Coordinate4D, Environment, SpaceAgent, SpaceSegment, StaticBlocker
from Simulator.helpers.helpers import is_valid_for_path_allocation
from test.EnvHelpers import generate_path_agent


class AstarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = Environment(Coordinate4D(20, 1, 20, 1000))
        blocky = StaticBlocker(Coordinate3D(3, 0, 3), Coordinate3D(4, 1, 5))
        blocky.id = 3
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 1000))

        blocky2 = StaticBlocker(Coordinate3D(9, 0, 6), Coordinate3D(2, 1, 8))
        blocky2.id = 4
        blocky2.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 1000))
        self.env.blocker_dict[blocky.id] = blocky
        self.env.blocker_dict[blocky2.id] = blocky2
        self.astar = AStar(self.env, FCFSBidTracker(), 1, g_sum=1, height_adjust=0, max_iter=2000)

    def test_astar(self):
        agi = generate_path_agent()
        res = self.astar.astar(Coordinate4D(0, 0, 5, 2), Coordinate4D(17, 0, 8, 25), agi)
        self.assertEqual(0, len(res[1]))
        self.assertEqual(29, len(res[0]))
        for coordinate in res[0]:
            self.assertTrue(is_valid_for_path_allocation(1, self.env, FCFSBidTracker(), coordinate, agi))

    def test_astar_2(self):
        agi = generate_path_agent()
        res = self.astar.astar(Coordinate4D(0, 0, 5, 0), Coordinate4D(17, 0, 8, 25), agi)
        self.assertEqual(0, len(res[0]))

    def test_astar_3(self):
        agi = generate_path_agent()
        res = self.astar.astar(Coordinate4D(0, 0, 5, 999), Coordinate4D(17, 0, 8, 25), agi)
        self.assertEqual(0, len(res[0]))

    def test_astar_4(self):
        agi = generate_path_agent()
        res = self.astar.astar(Coordinate4D(4, 0, 5, 2), Coordinate4D(17, 0, 8, 25), agi)
        self.assertEqual(0, len(res[0]))

    def test_astar_5(self):
        blocky = StaticBlocker(Coordinate3D(3, 0, 0), Coordinate3D(4, 1, 2))
        blocky.id = 5
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 1000))
        self.env.blocker_dict[blocky.id] = blocky

        blocky2 = StaticBlocker(Coordinate3D(0, 0, 8), Coordinate3D(2, 1, 2))
        blocky2.id = 6
        blocky2.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 1000))
        self.env.blocker_dict[blocky2.id] = blocky2

        agi = generate_path_agent()
        res = self.astar.astar(Coordinate4D(0, 0, 5, 2), Coordinate4D(17, 0, 8, 25), agi)
        self.assertEqual(0, len(res[0]))

    def test_astar_6(self):
        agi = generate_path_agent()
        agi_2 = SpaceAgent(f"AgentName{random.randint(0, 100000)}",
                           FCFSSpaceBiddingStrategy(),
                           FCFSSpaceValueFunction(),
                           [SpaceSegment(Coordinate4D(2, 0, 0, 0), Coordinate4D(6, 0, 2, 8), 0)])
        self.env.allocate_space_segment_for_agent(agi_2,
                                                  SpaceSegment(Coordinate4D(2, 0, 0, 0), Coordinate4D(4, 0, 2, 8), 0))
        self.env.add_agent(agi_2)
        res = self.astar.astar(Coordinate4D(0, 0, 5, 2), Coordinate4D(17, 0, 8, 25), agi)
        self.assertEqual(0, len(res[1]))
        self.assertEqual(31, len(res[0]))
        for coordinate in res[0]:
            self.assertTrue(is_valid_for_path_allocation(1, self.env, FCFSBidTracker(), coordinate, agi))
