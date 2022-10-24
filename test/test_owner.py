import unittest

from API.GridLocation.GridLocation import GridLocation
from API.GridLocation.GridLocationType import GridLocationType
from API.GridLocation.Heatmap import Heatmap
from API.GridLocation.HeatmapType import HeatmapType
from API.WebClasses import WebPathOwner, WebSpaceOwner
from Demos.FCFS import FCFSPathBiddingStrategy, FCFSPathValueFunction, FCFSSpaceBiddingStrategy, FCFSSpaceValueFunction
from Simulator import Coordinate2D, Coordinate3D, Coordinate4D, Environment, StaticBlocker


class OwnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path_owner = WebPathOwner("Test Path Owner",
                                       "testosteroni",
                                       "#123456",
                                       [GridLocation(str(GridLocationType.RANDOM.value)),
                                        GridLocation(str(GridLocationType.RANDOM.value))],
                                       [10],
                                       FCFSPathBiddingStrategy(),
                                       FCFSPathValueFunction(),
                                       1, 1000, 1, {})
        self.space_owner = WebSpaceOwner("Test Space Owner",
                                         "Bluberatus",
                                         "#654321",
                                         [GridLocation(str(GridLocationType.HEATMAP.value),
                                                       heatmap=Heatmap(
                                                           heatmap_type=str(HeatmapType.INVERSE_SPARSE.value),
                                                           inverse_sparse={0.1: [Coordinate2D(20, 20),
                                                                                 Coordinate2D(30, 30)]}))],
                                         [10],
                                         Coordinate4D(3, 3, 1, 10),
                                         FCFSSpaceBiddingStrategy(),
                                         FCFSSpaceValueFunction(),
                                         {})
        self.env = Environment(Coordinate4D(100, 100, 100, 1000), min_height=10)

    def test_generate_stop_coordinates(self):
        blocky = StaticBlocker(Coordinate3D(0, 0, 0), Coordinate3D(100, 20, 100))
        blocky.id = 3
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        self.env.blocker_dict[blocky.id] = blocky
        stop = WebPathOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)), self.env, 4, 1)
        self.assertTrue(stop.y >= self.env.min_height)
        self.assertFalse(self.env.is_coordinate_blocked_forever(stop, 1))

    def test_generate_stop_coordinates_2(self):
        blocky = StaticBlocker(Coordinate3D(0, 0, 0), Coordinate3D(100, 100, 100))
        blocky.id = 4
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 1000))
        self.env.blocker_dict[blocky.id] = blocky
        stop = WebPathOwner.generate_stop_coordinate(GridLocation(str(GridLocationType.RANDOM.value)), self.env, 4, 1)
        self.assertTrue(self.env.is_coordinate_blocked_forever(stop, 1))

    def test_generate_agents_path(self):
        stops = self.path_owner.generate_agents(0, self.env)
        self.assertEqual(len(stops), 0)

        stops_2 = self.path_owner.generate_agents(10, self.env)
        self.assertEqual(len(self.path_owner.agents), 1)
        self.assertEqual(len(stops_2[0].locations), 2)
        self.assertGreaterEqual(stops_2[0].locations[-1].t - stops_2[0].locations[-0].t,
                                stops_2[0].locations[-1].distance(stops_2[0].locations[0]) * stops_2[
                                    0].speed)

    def test_generate_stop_coordinate(self):
        stop = WebSpaceOwner.generate_stop_coordinates(GridLocation(str(GridLocationType.HEATMAP.value),
                                                                    heatmap=Heatmap(
                                                                        heatmap_type=str(
                                                                            HeatmapType.INVERSE_SPARSE.value),
                                                                        inverse_sparse={
                                                                            0.1: [Coordinate2D(20, 20),
                                                                                  Coordinate2D(30, 30)]})),
                                                       self.env, 10)
        self.assertTrue(
            stop.inter_temporal_equal(Coordinate4D(20, self.env.min_height, 20, 11)) or stop.inter_temporal_equal(
                Coordinate4D(30, self.env.min_height, 30, 11)))

    def test_generate_agents_space(self):
        agents = self.space_owner.generate_agents(10, self.env)
        self.assertEqual(len(agents), 1)
        self.assertEqual(len(agents[0].blocks), 1)
        self.assertEqual(agents[0].blocks[0].max - agents[0].blocks[0].min, self.space_owner.size)

    def test_tombola_inverse(self):
        heatmap = Heatmap(heatmap_type=str(HeatmapType.INVERSE_SPARSE.value), inverse_sparse={
            0.1: [Coordinate2D(1, 1), Coordinate2D(1, 2), Coordinate2D(2, 1), Coordinate2D(2, 2)],
            0.2: [Coordinate2D(3, 3), Coordinate2D(3, 4), Coordinate2D(4, 3), Coordinate2D(4, 4)],
            0.8: [Coordinate2D(8, 8), Coordinate2D(8, 9), Coordinate2D(9, 8), Coordinate2D(9, 9)]
        })
        tombola = heatmap.assemble_tombola()
        self.assertEqual(tombola.count(Coordinate2D(1, 1)), 1)
        self.assertEqual(tombola.count(Coordinate2D(2, 2)), 1)
        self.assertEqual(tombola.count(Coordinate2D(3, 3)), 2)
        self.assertEqual(tombola.count(Coordinate2D(4, 4)), 2)
        self.assertEqual(tombola.count(Coordinate2D(8, 8)), 8)
        self.assertEqual(tombola.count(Coordinate2D(9, 8)), 8)

    def test_tombola_matrix(self):
        matrix = [[min(i, j) / 10 for j in range(10)] for i in range(10)]
        heatmap = Heatmap(heatmap_type=str(HeatmapType.MATRIX.value),
                          matrix=matrix)
        tombola = heatmap.assemble_tombola()
        self.assertEqual(tombola.count(Coordinate2D(1, 1)), 1)
        self.assertEqual(tombola.count(Coordinate2D(2, 2)), 2)
        self.assertEqual(tombola.count(Coordinate2D(3, 3)), 3)
        self.assertEqual(tombola.count(Coordinate2D(4, 4)), 4)
        self.assertEqual(tombola.count(Coordinate2D(8, 8)), 8)
        self.assertEqual(tombola.count(Coordinate2D(9, 8)), 8)

    def test_tombola_sparse(self):
        heatmap = Heatmap(heatmap_type=str(HeatmapType.SPARSE.value),
                          sparse={
                              Coordinate2D(1, 1): 0.1,
                              Coordinate2D(2, 2): 0.2,
                              Coordinate2D(3, 3): 0.3,
                              Coordinate2D(4, 4): 0.4,
                              Coordinate2D(8, 8): 0.8,
                              Coordinate2D(9, 8): 0.8,
                          })
        tombola = heatmap.assemble_tombola()
        self.assertEqual(tombola.count(Coordinate2D(1, 1)), 1)
        self.assertEqual(tombola.count(Coordinate2D(2, 2)), 2)
        self.assertEqual(tombola.count(Coordinate2D(3, 3)), 3)
        self.assertEqual(tombola.count(Coordinate2D(4, 4)), 4)
        self.assertEqual(tombola.count(Coordinate2D(8, 8)), 8)
        self.assertEqual(tombola.count(Coordinate2D(9, 8)), 8)
