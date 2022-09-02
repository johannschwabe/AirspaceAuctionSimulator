import unittest

from Simulator import Environment, Coordinate4D, SpaceSegment, StaticBlocker, Coordinate3D
from Simulator.Blocker.DynamicBlocker import DynamicBlocker
from test.EnvHelpers import generate_path_agent, generate_path_segment, generate_space_agent, \
    generate_path_allocation, generate_space_allocation


class EnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = Environment(Coordinate4D(100, 100, 100, 1000))

    def test_rtree_setup(self):
        newRTree = Environment.setup_rtree()
        self.assertTrue(newRTree.properties.dimension == 4)

    def test_get_blocker_id(self):
        self.assertTrue(self.env._blocker_id == 0)
        new_blocker_id = self.env._get_blocker_id()
        self.assertTrue(new_blocker_id == 0)
        self.assertTrue(self.env._blocker_id == 1)

    def test_allocate_path_segment_for_agent(self):
        self.assertTrue(self.env.tree.properties.dimension == 4)

        agi = generate_path_agent()
        path_segment = generate_path_segment(Coordinate4D(1, 1, 1, 5))
        self.env.allocate_path_segment_for_agent(agi, path_segment)
        r_tree_whole_path = self.env.tree.intersection([0, 0, 0, 0, 5, 5, 5, 20])
        r_tree_single_voxel = self.env.tree.intersection([2, 2, 3, 11, 2, 2, 3, 11])
        r_tree_no_voxel = self.env.tree.intersection([2, 2, 3, 12, 2, 2, 3, 12])
        r_tree_double_voxel = self.env.tree.intersection([1, 1, 3, 7, 1, 1, 3, 8])
        r_tree_end_voxel = self.env.tree.intersection([4, 4, 4, 16, 4, 4, 4, 16], objects=True)
        self.assertEqual(len(list(r_tree_whole_path)), 10)
        self.assertEqual(len(list(r_tree_single_voxel)), 1)
        self.assertEqual(len(list(r_tree_no_voxel)), 0)
        self.assertEqual(len(list(r_tree_double_voxel)), 1)
        rTreeObject = list(r_tree_end_voxel)
        self.assertEqual(rTreeObject[0].id, hash(agi.id))

    def test_allocate_space_segment_for_agent(self):
        agi = generate_space_agent()
        space_segment = SpaceSegment(Coordinate4D(40, 40, 40, 20), Coordinate4D(60, 60, 60, 70))
        self.env.allocate_space_segment_for_agent(agi, space_segment)

        whole_block = self.env.tree.intersection([0, 0, 0, 0, 80, 80, 80, 80])
        sub_block = self.env.tree.intersection([50, 50, 50, 50, 55, 55, 55, 55])
        block_obj = self.env.tree.intersection([30, 30, 30, 20, 41, 41, 41, 21], objects=True)
        off_block = self.env.tree.intersection([30, 30, 30, 20, 39, 39, 39, 21], objects=True)
        self.assertEqual(len(list(whole_block)), 1)
        self.assertEqual(len(list(sub_block)), 1)
        self.assertEqual(len(list(off_block)), 0)
        rTreeObject = list(block_obj)
        self.assertEqual(len(rTreeObject), 1)
        self.assertEqual(rTreeObject[0].id, hash(agi.id))

    def test_allocate_segments_for_agents(self):
        allocation = generate_path_allocation()
        self.env.allocate_segments_for_agents([allocation], 2)
        self.assertIn(hash(allocation.agent), self.env.agents)
        r_tree_whole_path = self.env.tree.intersection([0, 0, 0, 0, 20, 20, 20, 50])
        r_tree_intersection_path = self.env.tree.intersection([4, 4, 4, 16, 4, 4, 4, 16])
        self.assertEqual(len(list(r_tree_whole_path)), 20)
        self.assertEqual(len(list(r_tree_intersection_path)), 2)

    def test_allocate_segments_for_agents_2(self):
        allocation = generate_space_allocation()
        self.env.allocate_segments_for_agents([allocation], 3)
        self.assertIn(hash(allocation.agent), self.env.agents)
        sub_block = self.env.tree.intersection([5, 5, 5, 10, 7, 7, 7, 20])
        double_block = self.env.tree.intersection([12, 12, 12, 10, 12, 12, 12, 12])
        self.assertEqual(len(list(sub_block)), 1)
        self.assertEqual(len(list(double_block)), 2)

    def test_allocate_segments_for_agents_3(self):
        allocation = generate_space_allocation()
        allocation_2 = generate_path_allocation()
        self.env.allocate_segments_for_agents([allocation, allocation_2], 3)
        r_tree_intersection_path = self.env.tree.intersection([2, 2, 3, 10, 2, 2, 3, 10, ])
        self.assertEqual(len(list(r_tree_intersection_path)), 1)
        sub_block = self.env.tree.intersection([5, 5, 5, 10, 7, 7, 7, 20])
        self.assertEqual(len(list(sub_block)), 1)
        whole = self.env.tree.intersection([0, 0, 0, 0, 100, 100, 100, 100])
        self.assertEqual(len(list(whole)), 23)

    def test_register_agent(self):
        agi = generate_space_agent()
        self.env.register_agent(agi, 0)
        self.assertIn(hash(agi.id), self.env.agents)

    def test_deallocate_path_agent(self):
        alloc = generate_path_allocation()
        self.env.allocate_segments_for_agents([alloc], 0)
        self.env.deallocate_path_agent(alloc.agent, 0)
        allocations = self.env.tree.intersection([0, 0, 0, 0, 100, 100, 100, 100])
        self.assertEqual(len(list(allocations)), 0)

    def test_deallocate_space_agent(self):
        alloc = generate_space_allocation()
        self.env.allocate_segments_for_agents([alloc], 0)
        self.env.deallocate_space_agent(alloc.agent, 0)
        allocations = self.env.tree.intersection([0, 0, 0, 0, 100, 100, 100, 100])
        self.assertEqual(len(list(allocations)), 0)

    def test_deallocate_agent(self):
        alloc = generate_path_allocation()
        self.env.allocate_segments_for_agents([alloc], 0)
        self.env.deallocate_agent(alloc.agent, 0)
        allocations = self.env.tree.intersection([0, 0, 0, 0, 100, 100, 100, 100])
        self.assertEqual(len(list(allocations)), 0)

    def test_deallocate_agent_2(self):
        alloc = generate_space_allocation()
        self.env.allocate_segments_for_agents([alloc], 0)
        self.env.deallocate_agent(alloc.agent, 0)
        allocations = self.env.tree.intersection([0, 0, 0, 0, 100, 100, 100, 100])
        self.assertEqual(len(list(allocations)), 0)

    def test_create_real_allocations(self):
        alloc_1 = generate_path_allocation()
        real_agent_1 = alloc_1.agent
        alloc_1.agent = real_agent_1.clone()
        self.env.register_agent(real_agent_1, 0)
        alloc_2 = generate_space_allocation()
        real_agent_2 = alloc_2.agent
        alloc_2.agent = real_agent_2.clone()

        new_agents = {hash(real_agent_2.id): real_agent_2}
        converted = self.env.create_real_allocations([alloc_1, alloc_2], new_agents)
        self.assertFalse(converted[0].agent.is_clone)
        self.assertFalse(converted[1].agent.is_clone)

    def test_get_blockers(self):
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(10, 10, 10))
        blocky2 = StaticBlocker(Coordinate3D(5, 5, 5), Coordinate3D(10, 10, 10))
        blocky.id = 11
        blocky2.id = 22
        blocky.add_to_tree(self.env.blocker_tree, self.env.dimension)
        blocky2.add_to_tree(self.env.blocker_tree, self.env.dimension)
        intersecting_blockers = self.env.get_blockers(Coordinate4D(6, 6, 6, 100), 1, 1)
        intersecting_blockers_list = list(intersecting_blockers)
        self.assertEqual(len(intersecting_blockers_list), 2)
        self.assertIn(blocky.id, intersecting_blockers_list)
        self.assertIn(blocky2.id, intersecting_blockers_list)

    def test_is_blocked(self):
        agi = generate_path_agent()
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(10, 10, 10))
        blocky2 = DynamicBlocker([
            Coordinate4D(0, 0, 0, 0),
            Coordinate4D(1, 1, 1, 1),
            Coordinate4D(2, 2, 2, 2),
            Coordinate4D(3, 3, 3, 3),
        ], dimension=Coordinate3D(2, 2, 2))
        blocky.id = 11
        blocky2.id = 22
        self.env.blocker_dict[blocky.id] = blocky
        self.env.blocker_dict[blocky2.id] = blocky2
        blocky.add_to_tree(self.env.blocker_tree, self.env.dimension)
        blocky2.add_to_tree(self.env.blocker_tree, self.env.dimension)
        is_blocking = self.env.is_blocked(Coordinate4D(4, 4, 4, 10), agi)
        self.assertTrue(is_blocking)

        is_blocked_forever = self.env.is_blocked_forever(Coordinate4D(1, 1, 1, 1), 1)
        is_blocked_forever_2 = self.env.is_blocked_forever(Coordinate4D(10, 10, 10, 1), 1)
        self.assertFalse(is_blocked_forever)
        self.assertTrue(is_blocked_forever_2)

    def test_have_intersections_collision(self):
        agi_1 = generate_path_agent()
        agi_2 = generate_path_agent()
        agi_3 = generate_path_agent()

        self.env.agents = {
            hash(agi_1): agi_1,
            hash(agi_2): agi_2,
            hash(agi_3): agi_3,
        }

        segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        segment2 = generate_path_segment(Coordinate4D(6, 6, 6, 20))
        segment2.index = 1
        agi_1.add_allocated_segment(segment)
        agi_1.add_allocated_segment(segment2)
        res = self.env.have_intersections_collision(Coordinate4D(3, 3, 5, 6),
                                                    agi_2,
                                                    [hash(agi_1), hash(agi_3)], [hash(agi_3)])

        self.assertTrue(res)
        res2 = self.env.have_intersections_collision(Coordinate4D(3, 3, 5, 6),
                                                     agi_2,
                                                     [hash(agi_3), hash(agi_1)], [hash(agi_1)])
        self.assertFalse(res2)

    def test_is_blocked_by_agent(self):
        agi = generate_path_agent()
        agi_2 = generate_path_agent()
        path_segment = generate_path_segment(Coordinate4D(3, 3, 3, 3))
        self.env.allocate_path_segment_for_agent(agi, path_segment)
        self.env.add_agent(agi)
        self.assertTrue(self.env.is_blocked_by_agent(Coordinate4D(3, 3, 5, 6), agi_2))
        self.assertTrue(self.env.is_blocked_by_agent(Coordinate4D(4, 3, 5, 6), agi_2))
        self.assertFalse(self.env.is_blocked_by_agent(Coordinate4D(5, 3, 5, 6), agi_2))
        agi.near_radius = 4
        self.env.max_near_radius = 4
        self.assertTrue(self.env.is_blocked_by_agent(Coordinate4D(5, 3, 5, 6), agi_2))

    def test_is_space_blocked(self):
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(10, 10, 10))
        blocky.id = 3
        self.env.blocker_dict[blocky.id] = blocky
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        is_blocked = self.env.is_space_blocked(Coordinate4D(4, 4, 4, 4), Coordinate4D(15, 15, 15, 15))
        self.assertTrue(is_blocked)
        is_blocked_2 = self.env.is_space_blocked(Coordinate4D(14, 14, 14, 14), Coordinate4D(15, 15, 15, 15))
        self.assertFalse(is_blocked_2)

    def test_is_valid_for_allocation(self):
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(7, 7, 7))
        blocky.id = 3
        self.env.blocker_dict[blocky.id] = blocky
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))
        agi = generate_path_agent()
        path_segment = generate_path_segment(Coordinate4D(11, 11, 11, 3))
        self.env.allocate_path_segment_for_agent(agi, path_segment)
        self.env.add_agent(agi)

        agi_2 = generate_path_agent()
        self.assertFalse(self.env.is_valid_for_allocation(Coordinate4D(4, 4, 4, 4), agi_2))
        self.assertFalse(self.env.is_valid_for_allocation(Coordinate4D(11, 11, 13, 5), agi_2))
        self.assertTrue(self.env.is_valid_for_allocation(Coordinate4D(11, 11, 14, 25), agi_2))

    def test_other_agents_in_space(self):
        agi = generate_path_agent()
        path_segment = generate_path_segment(Coordinate4D(11, 11, 11, 3))
        self.env.allocate_path_segment_for_agent(agi, path_segment)
        self.env.add_agent(agi)

        agi_2 = generate_space_agent()
        other_agents = self.env.other_agents_in_space(Coordinate4D(9, 9, 9, 1), Coordinate4D(12, 12, 12, 5), agi_2)
        self.assertEqual(1, len(other_agents))
        self.assertIn(agi, other_agents)
        other_agents_2 = self.env.other_agents_in_space(Coordinate4D(9, 9, 9, 52), Coordinate4D(12, 12, 12, 80), agi_2)
        self.assertEqual(0, len(other_agents_2))

    def test_new_clear(self):
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(7, 7, 7))
        blocky.id = 3
        self.env.blocker_dict[blocky.id] = blocky
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))

        agi = generate_path_agent()
        path_segment = generate_path_segment(Coordinate4D(11, 11, 11, 3))
        self.env.allocate_path_segment_for_agent(agi, path_segment)
        self.env.add_agent(agi)

        new_clear = self.env.new_clear()
        agi_2 = generate_path_agent()
        self.assertTrue(new_clear.is_blocked(Coordinate4D(4, 4, 4, 4), agi_2))
        self.assertFalse(new_clear.is_blocked_by_agent(Coordinate4D(11, 11, 11, 3), agi_2))

    def test_clone(self):
        blocky = StaticBlocker(Coordinate3D(3, 3, 3), Coordinate3D(7, 7, 7))
        blocky.id = 3
        self.env.blocker_dict[blocky.id] = blocky
        blocky.add_to_tree(self.env.blocker_tree, Coordinate4D(0, 0, 0, 100))

        agi = generate_path_agent()
        path_segment = generate_path_segment(Coordinate4D(11, 11, 11, 3))
        self.env.allocate_path_segment_for_agent(agi, path_segment)
        self.env.add_agent(agi)

        new_clear = self.env.clone()
        agi_2 = generate_path_agent()
        self.assertTrue(new_clear.is_blocked(Coordinate4D(4, 4, 4, 4), agi_2))
        self.assertTrue(new_clear.is_blocked_by_agent(Coordinate4D(11, 11, 11, 3), agi_2))


if __name__ == '__main__':
    unittest.main()
