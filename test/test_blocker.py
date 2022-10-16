import unittest

from Simulator import BuildingBlocker, Coordinate3D, Coordinate4D, DynamicBlocker, Environment, StaticBlocker


class BlockerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = Environment(Coordinate4D(100, 100, 100, 1000))

    def test_static_add_to_tree(self):
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(10, 10, 10))
        blocky.id = 3
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        intersection = self.env.blocker_tree.intersection([4, 4, 4, 10, 5, 5, 5, 10], objects=True)
        outside_intersection = self.env.blocker_tree.intersection([4, 4, 15, 3, 5, 5, 15, 16], objects=True)
        intersection_list = list(intersection)
        self.assertEqual(len(intersection_list), 1)
        self.assertEqual(intersection_list[0].id, blocky.id)
        self.assertEqual(len(list(outside_intersection)), 0)

    def test_dynamic_blocker_add_to_tree(self):
        blocky = DynamicBlocker([
            Coordinate4D(0, 0, 0, 0),
            Coordinate4D(1, 1, 1, 1),
            Coordinate4D(2, 2, 2, 2),
            Coordinate4D(3, 3, 3, 3),
        ], dimension=Coordinate3D(2, 2, 2))
        blocky.id = 4
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        intersection = self.env.blocker_tree.intersection([1, 1, 1, 0, 1, 1, 1, 0], objects=True)
        intersection_list = list(intersection)
        self.assertEqual(len(intersection_list), 1)
        self.assertEqual(intersection_list[0].id, blocky.id)
        outside_intersection = self.env.blocker_tree.intersection([4, 4, 4, 4, 4, 4, 4, 4], objects=True)
        self.assertEqual(len(list(outside_intersection)), 0)

    def test_building_blocker_add_to_tree(self):
        vertices = [[25.293743400114263, 45.00812708695961], [30.490025531862816, 49.28913767620337],
                    [52.70630814961371, 25.382195425911238], [59.898408444701865, 16.597784087518164],
                    [44.08362068723329, -0.4706607286903285], [9.064726232640718, 31.775912539393612],
                    [25.293743400114263, 45.00812708695961]]
        bounds = [Coordinate3D(9.064726232640718, 0, -0.4706607286903285),
                  Coordinate3D(59.898408444701865, 7.5, 49.28913767620337)]
        holes = [[[20.925884561437933, 31.21993713804947], [28.983978115683396, 23.65867168229747],
                  [36.32656582563742, 30.60836419672894], [33.76604667907642, 33.22144858233531],
                  [32.78703519266998, 32.443083020690544], [31.243193730781222, 34.05541168395647],
                  [32.10924090482372, 35.00056986592547], [29.096869395414778, 38.22522719285238],
                  [20.925884561437933, 31.21993713804947]],
                 [[42.05018948996067, 10.537652214684256], [48.564380667439934, 17.15375948846726],
                  [42.05009620920083, 23.547476601949633], [35.57355934472442, 16.931369328166628],
                  [42.05018948996067, 10.537652214684256]]]
        blocky = BuildingBlocker(vertices, bounds, holes)
        blocky.id = 5
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        intersection = self.env.blocker_tree.intersection([20, 1, 30, 0, 30, 1, 40, 2], objects=True)
        intersection_list = list(intersection)
        self.assertEqual(len(intersection_list), 1)
        self.assertEqual(intersection_list[0].id, blocky.id)
        self.assertTrue(blocky.is_blocking(Coordinate4D(20, 1, 30, 0)))
        self.assertFalse(blocky.is_blocking(Coordinate4D(35, 1, 30, 0)))
        self.assertTrue(blocky.is_blocking(Coordinate4D(35, 1, 30, 0), 1))
        self.assertTrue(blocky.is_box_blocking(Coordinate4D(20, 0, 20, 0), Coordinate4D(25, 1, 25, 1)))


if __name__ == '__main__':
    unittest.main()
