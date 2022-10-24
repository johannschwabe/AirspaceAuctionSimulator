import unittest

from Simulator import Coordinate4D
from Simulator.Coordinates.Coordinate3D import Coordinate3D
from Simulator.Environment.Environment import Environment
from test.EnvHelpers import generate_path_agent, generate_path_segment


class PathAgentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = generate_path_agent()

    def test_add_allocated_segment(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        segment.end = Coordinate3D(9, 9, 9)
        self.agent.add_allocated_segment(segment)
        self.assertEqual(self.agent.allocated_segments[0], segment)
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 14))
        self.agent.add_allocated_segment(segment2)
        self.assertEqual(len(self.agent.allocated_segments), 1)

    def test_add_allocated_segment_2(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        self.agent.add_allocated_segment(segment)
        self.assertEqual(self.agent.allocated_segments[0], segment)
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 14))
        segment2.index = 1
        self.agent.add_allocated_segment(segment2)
        self.assertEqual(len(self.agent.allocated_segments), 2)

    def test_get_airtime(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        self.agent.add_allocated_segment(segment)
        self.assertEqual(self.agent.get_airtime(), 12)
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 14))
        segment2.index = 1
        self.agent.add_allocated_segment(segment2)
        self.assertEqual(self.agent.get_airtime(), 23)

    def test_get_position_at_tick(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 20))
        segment2.index = 1
        self.agent.add_allocated_segment(segment)
        self.agent.add_allocated_segment(segment2)
        self.assertEqual(Coordinate4D(3, 3, 5, 5), self.agent.get_position_at_tick(5))
        self.assertEqual(Coordinate4D(6, 6, 8, 22), self.agent.get_position_at_tick(22))
        self.assertIsNone(self.agent.get_position_at_tick(50))

    def test_get_allocated_coords(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 20))
        segment2.index = 1
        self.agent.add_allocated_segment(segment)
        self.agent.add_allocated_segment(segment2)
        self.assertEqual(segment.coordinates + segment2.coordinates, self.agent.get_allocated_coords())

    def test_does_collide(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 20))
        segment2.index = 1
        agi = generate_path_agent()
        self.agent.add_allocated_segment(segment)
        self.agent.add_allocated_segment(segment2)
        self.assertTrue(self.agent.does_collide(Coordinate4D(6, 7, 8, 24), agi))
        self.assertTrue(self.agent.does_collide(Coordinate4D(7, 7, 8, 24), agi))
        self.assertFalse(self.agent.does_collide(Coordinate4D(7, 8, 8, 24), agi))

    def test_allocated_value(self):
        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 20))
        segment2.index = 1
        self.agent.add_allocated_segment(segment)
        self.agent.locations[-1] = Coordinate4D(6, 6, 6, 14)
        self.assertEqual(19.8, self.agent.get_allocated_value())
        self.agent.locations.append(Coordinate4D(9, 9, 9, 31))
        self.agent.add_allocated_segment(segment2)
        self.assertEqual(34.65, self.agent.get_allocated_value())

    def test_get_bid(self):
        env = Environment(Coordinate4D(100, 100, 100, 1000))
        bid = self.agent.get_bid(3, env)
        self.assertEqual(bid.locations, self.agent.locations)
        self.assertEqual(bid.battery, self.agent.battery)
