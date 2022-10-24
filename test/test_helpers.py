import unittest

from Demos.FCFS.BidTracker.FCFSBidTracker import FCFSBidTracker
from Simulator.Blocker.DynamicBlocker import DynamicBlocker
from Simulator.Blocker.StaticBlocker import StaticBlocker
from Simulator.Coordinates.Coordinate3D import Coordinate3D
from Simulator.Coordinates.Coordinate4D import Coordinate4D
from Simulator.Environment.Environment import Environment
from Simulator.helpers.helpers import find_valid_path_tick, find_valid_space_tick, is_valid_for_space_allocation
from test.EnvHelpers import generate_path_agent, generate_space_agent, generate_space_allocation, \
    generate_path_allocation


class HelpersTest(unittest.TestCase):
    def setUp(self) -> None:
        self.blockers = [StaticBlocker(Coordinate3D(30, 30, 0), Coordinate3D(10, 10, 10)),
                         StaticBlocker(Coordinate3D(49, 49, 0), Coordinate3D(10, 10, 10)),
                         DynamicBlocker([Coordinate4D(10, 10, 0, 5),
                                         Coordinate4D(10, 10, 0, 6),
                                         Coordinate4D(10, 10, 0, 7)], Coordinate3D(10, 10, 10))
                         ]
        self.env = Environment(Coordinate4D(100, 100, 100, 1000), self.blockers)
        self.FCFSBidTracker = FCFSBidTracker()
        self.path_agent = generate_path_agent()
        self.space_agent = generate_space_agent()

    def test_find_valid_path_tick(self):
        self.assertEqual(1, find_valid_path_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                 position=Coordinate4D(3, 3, 3, 1), agent=self.path_agent, min_tick=0,
                                                 max_tick=1000))
        self.assertEqual(10, find_valid_path_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                  position=Coordinate4D(3, 3, 3, 1), agent=self.path_agent, min_tick=10,
                                                  max_tick=1000))
        self.assertIsNone(find_valid_path_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                               position=Coordinate4D(3, 3, 3, 1001), agent=self.path_agent, min_tick=10,
                                               max_tick=1000))
        self.assertEqual(8, find_valid_path_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                 position=Coordinate4D(11, 11, 5, 6), agent=self.path_agent, min_tick=3,
                                                 max_tick=1000))

    def test_find_valid_space_tick(self):
        self.assertEqual(1, find_valid_space_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                  min_position=Coordinate4D(11, 11, 3, 1),
                                                  max_position=Coordinate4D(17, 17, 6, 10), agent=self.path_agent,
                                                  min_tick=0, max_tick=1000, avoid_blockers=False))
        self.assertEqual(8, find_valid_space_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                  min_position=Coordinate4D(11, 11, 3, 1),
                                                  max_position=Coordinate4D(17, 17, 6, 10), agent=self.path_agent,
                                                  min_tick=0, max_tick=1000, avoid_blockers=True))
        self.assertEqual(5, find_valid_space_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                  min_position=Coordinate4D(11, 11, 3, 1),
                                                  max_position=Coordinate4D(17, 17, 6, 10), agent=self.path_agent,
                                                  min_tick=5, max_tick=1000, avoid_blockers=False))
        self.assertIsNone(find_valid_space_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                min_position=Coordinate4D(11, 11, 3, 1001),
                                                max_position=Coordinate4D(17, 17, 6, 1005), agent=self.path_agent,
                                                min_tick=5, max_tick=1000, avoid_blockers=False))
        self.assertIsNone(find_valid_space_tick(tick=0, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                                min_position=Coordinate4D(11, 11, 3, 5),
                                                max_position=Coordinate4D(17, 17, 6, 7), agent=self.path_agent,
                                                min_tick=5, max_tick=1000, avoid_blockers=True))

    def test_is_valid_for_space_allocation(self):
        self.assertTrue(
            is_valid_for_space_allocation(allocation_tick=1, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                          min_position=Coordinate4D(60, 60, 0, 4),
                                          max_position=Coordinate4D(80, 80, 10, 10), space_agent=self.space_agent,
                                          avoid_blockers=False)[0])
        self.assertRaises(BaseException, is_valid_for_space_allocation, allocation_tick=10, environment=self.env,
                          bid_tracker=self.FCFSBidTracker,
                          min_position=Coordinate4D(60, 60, 0, 4),
                          max_position=Coordinate4D(80, 80, 10, 10),
                          space_agent=self.space_agent,
                          avoid_blockers=False)
        self.env.allocate_segments_for_agents([generate_space_allocation()], 1)
        self.assertFalse(
            is_valid_for_space_allocation(allocation_tick=1, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                          min_position=Coordinate4D(40, 40, 40, 10),
                                          max_position=Coordinate4D(80, 80, 50, 11), space_agent=self.space_agent,
                                          avoid_blockers=False)[0])
        self.env.allocate_segments_for_agents([generate_path_allocation()], 1)
        self.assertFalse(
            is_valid_for_space_allocation(allocation_tick=1, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                          min_position=Coordinate4D(1, 1, 1, 5),
                                          max_position=Coordinate4D(2, 2, 2, 6), space_agent=self.space_agent,
                                          avoid_blockers=False)[0])

    def test_is_valid_for_space_allocation_2(self):
        self.env.allocate_segments_for_agents([generate_path_allocation()], 1)
        self.env.max_near_radius = 10
        self.assertTrue(
            is_valid_for_space_allocation(allocation_tick=1, environment=self.env, bid_tracker=self.FCFSBidTracker,
                                          min_position=Coordinate4D(8, 8, 8, 27),
                                          max_position=Coordinate4D(10, 10, 10, 28), space_agent=self.space_agent,
                                          avoid_blockers=False)[0])
