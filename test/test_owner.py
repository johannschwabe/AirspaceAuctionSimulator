import unittest

from Demos.FCFS.BiddingStrategy.FCFSPathBiddingStrategy import FCFSPathBiddingStrategy
from Demos.FCFS.BiddingStrategy.FCFSSpaceBiddingStrategy import FCFSSpaceBiddingStrategy
from Demos.FCFS.ValueFunction.FCFSPathValueFunction import FCFSPathValueFunction
from Demos.FCFS.ValueFunction.FCFSSpaceValueFunction import FCFSSpaceValueFunction
from Simulator import GridLocation, Heatmap, SpaceOwner, GridLocationType, Environment, Coordinate3D, Coordinate4D, \
    PathOwner, StaticBlocker
from Simulator.Coordinates.Coordinate2D import Coordinate2D
from Simulator.Location.HeatmapType import HeatmapType


class OwnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path_owner = PathOwner("Test Path Owner",
                                    "testosteroni",
                                    "#123456",
                                    [GridLocation(str(GridLocationType.RANDOM.value)),
                                     GridLocation(str(GridLocationType.RANDOM.value))],
                                    [10],
                                    FCFSPathBiddingStrategy(),
                                    FCFSPathValueFunction({}),
                                    1, 1000, 1, {})
        self.space_owner = SpaceOwner("Test Space Owner",
                                      "Bluberatus",
                                      "#654321",
                                      [GridLocation(str(GridLocationType.HEATMAP.value),
                                                    heatmap=Heatmap(heatmap_type=str(HeatmapType.INVERSE_SPARSE.value),
                                                                    inverse_sparse={0.1: [Coordinate2D(20, 20),
                                                                                          Coordinate2D(30, 30)]}))],
                                      [10],
                                      Coordinate4D(3, 3, 1, 10),
                                      FCFSSpaceBiddingStrategy(),
                                      FCFSSpaceValueFunction({}),
                                      {})
        self.env = Environment(Coordinate4D(100, 100, 100, 1000), min_height=10)

    def test_generate_stop_coordinates(self):
        blocky = StaticBlocker(Coordinate3D(0, 0, 0), Coordinate3D(100, 20, 100))
        blocky.id = 3
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        self.env.blocker_dict[blocky.id] = blocky
        stop = PathOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)), self.env, 4, 1)
        self.assertTrue(stop.y >= self.env.min_height)
        self.assertFalse(self.env.is_blocked_forever(stop, 1))

    def test_generate_stop_coordinates_2(self):
        blocky = StaticBlocker(Coordinate3D(0, 0, 0), Coordinate3D(100, 100, 100))
        blocky.id = 4
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 1000))
        self.env.blocker_dict[blocky.id] = blocky
        stop = PathOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)), self.env, 4, 1)
        self.assertTrue(self.env.is_blocked_forever(stop, 1))

    def test_generate_agents_path(self):
        stops = self.path_owner.generate_agents(0, self.env)
        self.assertEqual(len(stops), 0)

        stops_2 = self.path_owner.generate_agents(10, self.env)
        self.assertEqual(len(self.path_owner.agents), 1)
        self.assertEqual(len(stops_2[0].locations), 2)
        self.assertGreaterEqual(stops_2[0].locations[-1].t - stops_2[0].locations[-0].t,
                                stops_2[0].locations[-1].inter_temporal_distance(stops_2[0].locations[0]) * stops_2[
                                    0].speed)

    def test_generate_stop_coordinate(self):
        stop = SpaceOwner.generate_stop_coordinates(GridLocation(str(GridLocationType.HEATMAP.value),
                                                                 heatmap=Heatmap(
                                                                     heatmap_type=str(HeatmapType.INVERSE_SPARSE.value),
                                                                     inverse_sparse={
                                                                         0.1: [Coordinate2D(20, 20),
                                                                               Coordinate2D(30, 30)]})),
                                                    self.env, 10)
        self.assertIn(stop,
                      [Coordinate4D(20, self.env.min_height, 20, 11), Coordinate4D(30, self.env.min_height, 30, 11)])

    def test_generate_agents_space(self):
        agents = self.space_owner.generate_agents(10, self.env)
        self.assertEqual(len(agents), 1)
        self.assertEqual(len(agents[0].blocks), 1)
        self.assertEqual(agents[0].blocks[0][1] - agents[0].blocks[0][0], self.space_owner.size)
