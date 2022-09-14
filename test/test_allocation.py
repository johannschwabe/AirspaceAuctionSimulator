import unittest

from test.EnvHelpers import generate_path_allocation, generate_path_agent


class AllocationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.allocation = generate_path_allocation()

    def test_get_real_allocation(self):
        agi = generate_path_agent()
        agi.id = "notAClone"
        new_allocation = self.allocation.get_allocation_with_agent(agi)
        self.assertNotEqual(new_allocation.agent.id, self.allocation.agent.id)

    def test_nr_voxels(self):
        self.assertEqual(self.allocation.nr_voxels, 24)


if __name__ == '__main__':
    unittest.main()
