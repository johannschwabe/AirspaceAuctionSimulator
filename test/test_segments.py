import unittest

from Simulator import Coordinate4D, SpaceSegment
from test.EnvHelpers import generate_path_segment


class SegmentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.segment = generate_path_segment(Coordinate4D(2, 3, 4, 5))

    def test_same(self):
        other = generate_path_segment(Coordinate4D(2, 3, 4, 5))
        self.assertTrue(self.segment.same(other))
        other.index = 1
        self.assertFalse(self.segment.same(other))

    def test_nr_voxels(self):
        self.assertEqual(12, self.segment.nr_voxels)

    def test_min_max(self):
        self.assertEqual(Coordinate4D(2, 3, 4, 5), self.segment.min)
        self.assertEqual(Coordinate4D(5, 6, 7, 16), self.segment.max)

    def test_split_temporal(self):
        first, second = self.segment.split_temporal(8)
        self.assertEqual(first.start, self.segment.start)
        self.assertEqual(second.start, self.segment.start)
        self.assertEqual(first.end, self.segment.end)
        self.assertEqual(second.end, self.segment.end)
        self.assertEqual(Coordinate4D(2, 3, 6, 8), first.max)
        self.assertEqual(Coordinate4D(2, 4, 6, 9), second.min)

    def test_join(self):
        other = generate_path_segment(Coordinate4D(9, 3, 4, 5))
        self.assertRaises(AssertionError, self.segment.join, other)

    def test_space_split(self):
        space_segment = SpaceSegment(Coordinate4D(2, 3, 4, 5), Coordinate4D(10, 30, 40, 50), 0)
        first, second = space_segment.split_temporal(30)
        self.assertEqual(first.max.t, 30)
        self.assertEqual(second.min.t, 31)
