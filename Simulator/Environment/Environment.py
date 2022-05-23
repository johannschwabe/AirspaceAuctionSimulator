from typing import List, Dict
from rtree import index

from ..Agent import Agent
from ..Coordinate import TimeCoordinate
from ..Time import Tick
from ..Blocker import Blocker


class Environment:
    def __init__(self, dimension: TimeCoordinate):
        TimeCoordinate.dim = dimension
        self._dimension: TimeCoordinate = dimension
        self._agents: Dict[int, Agent] = {}
        props = index.Property()
        props.dimension = 4
        self.tree = index.Rtree(properties=props)
        self.blocker_tree = None
        self.near_field_radius = 1

    def deallocate_agent(self, agent: Agent, time_step: Tick):
        agent._allocated_paths = [[]]
        for coord in agent.get_allocated_coords():
            if coord.t > time_step:
                self.tree.delete(agent.id, coord.tree_query_point_rep())

    def add_blocker(self, blockers: List[Blocker]):
        props = index.Property()
        props.dimension = 4
        self.blocker_tree = index.Rtree(properties=props)
        for blocker in blockers:
            blocker.add_to_tree(self.blocker_tree)


    def allocate_paths_for_agent(self, agent: Agent, paths: List[List[TimeCoordinate]]):
        for path in paths:
            self.allocate_path_for_agent(agent, path)

    def allocate_path_for_agent(self, agent: Agent, path: List[TimeCoordinate]):
        agent.add_allocated_paths(path)
        iterator = path[0]
        for coord in path:
            if coord.inter_temporal_equal(iterator):
                continue
            aggregated = iterator.tree_query_point_rep()
            aggregated[7] = coord.t - 1
            self.tree.insert(agent.id, aggregated)
            iterator = coord
        aggregated = iterator.tree_query_point_rep()
        aggregated[7] = path[-1].t
        self.tree.insert(agent.id, aggregated)

    def allocate_paths_for_agents(self, agents_paths: Dict[Agent, List[List[TimeCoordinate]]], time_step: Tick):
        for agent, paths in agents_paths.items():
            if agent in self._agents:
                self.deallocate_agent(agent, time_step)
            else:
                self._agents[agent.id] = agent

            for path in paths:
                self.allocate_path_for_agent(agent, path)

    def is_blocked(self, coords: TimeCoordinate) -> bool:
        blockers = self.blocker_tree.intersection(coords.tree_query_point_rep())
        return len(list(blockers)) > 0


    def add_agent(self, agent: Agent):
        self._agents[agent.id] = agent

    def get_agents(self):
        return self._agents

    def get_dim(self):
        return self._dimension

    def is_valid_for_allocation(self, coords: TimeCoordinate, agent: Agent) -> bool:
        radius: int = agent.near_radius
        agents = self.tree.intersection((
            coords.x - radius, coords.y - radius, coords.z - radius, coords.t,
            coords.x + radius, coords.y + radius, coords.z + radius, coords.t + agent.speed
        ))

        return len(list(agents)) == 0 and not self.is_blocked(coords)

    def get_agents_at(self, coords: TimeCoordinate) -> List[Agent]:
        return [self._agents[_id] for _id in self.tree.intersection(coords.tree_query_point_rep())]

    def visualize(self, current_time_step, before=0, nr_steps=1):
        for t in range(current_time_step - before, current_time_step + nr_steps):
            print(f"t = {t}")
            for z in range(self._dimension.z):
                print(f"z={z: >2}", end="")
                for i in range(self._dimension.x):
                    print(f" {i: >4}", end="")
                print("  -> X")
                for y in range(self._dimension.y):
                    print(f"  {y: >2} ", end="")
                    for x in range(self._dimension.x):
                        coord = TimeCoordinate(x, y, z, Tick(t))
                        agents = list(self.tree.intersection(coord.tree_query_point_rep()))
                        if len(agents) > 0:
                            print(f" {','.join(map(str, agents))}".rjust(5, ' '), end="")

                        elif self.is_blocked(coord):
                            print("✖".rjust(5, ' '), end="")
                        # elif field.is_near():
                        #     print("*".rjust(5, ' '), end="")
                        # elif field.is_far():
                        #     print("-".rjust(5, ' '), end="")
                        else:
                            print(".".rjust(5, ' '), end="")
                    print("")
                print("")
            print(" ↓\n Y")

    def new_clear(self):
        new_env = Environment(self._dimension)
        new_env.blocker_tree = self.blocker_tree
        return new_env

    def clone(self):
        cloned = Environment(self._dimension)
        if len(self.tree) > 0:
            for item in self.tree.intersection(self.tree.bounds, objects=True):
                cloned.tree.insert(item.id, item.bbox)
        cloned.blocker_tree = self.blocker_tree
        return cloned
