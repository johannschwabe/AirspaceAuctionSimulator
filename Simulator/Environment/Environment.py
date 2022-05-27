from typing import List, Dict, TYPE_CHECKING
from rtree import index

from ..Agent import Agent, AgentType
from ..Coordinate import TimeCoordinate
from ..Time import Tick
from ..Blocker import Blocker

if TYPE_CHECKING:
    from ..Generator.MapTile import MapTile


class Environment:
    def __init__(self, dimension: TimeCoordinate, blocker: List[Blocker], maptiles: List["MapTile"]):
        TimeCoordinate.dim = dimension
        self._dimension: TimeCoordinate = dimension
        self._agents: Dict[int, Agent] = {}
        self.blockers: Dict[int, Blocker] = {blocky.id: blocky for blocky in blocker}
        self.maptiles: List["MapTile"] = maptiles
        props = index.Property()
        props.dimension = 4
        self.tree = index.Rtree(properties=props)
        self.blocker_tree = None
        self.near_field_radius = 1

    def deallocate_agent(self, agent: Agent, time_step: Tick):
        allocated_coords = agent.get_allocated_coords()
        for coord in allocated_coords[max(time_step - allocated_coords[0].t, 0):]:
            intersections = self.tree.intersection(coord.tree_query_point_rep(), objects=True)
            for intersection in intersections:
                _index = intersection.id
                bbox = intersection.bbox
                if _index == agent.id:
                    self.tree.delete(agent.id, bbox)
                if bbox[3] < int(time_step):
                    bbox[7] = int(time_step)
                    self.tree.insert(agent.id, bbox)

        new_allocated_paths = []
        for path in agent.get_allocated_paths():
            if path[0].t > time_step:
                break
            if path[-1].t > time_step:
                new_allocated_paths.append(path[:time_step - path[0].t])
            else:
                new_allocated_paths.append(path)
        agent.set_allocated_paths(new_allocated_paths)

    def set_blockers(self):
        props = index.Property()
        props.dimension = 4
        self.blocker_tree = index.Rtree(properties=props)
        for blocker in self.blockers.values():
            blocker.add_to_tree(self.blocker_tree)

    def allocate_paths_for_agent(self, agent: Agent, paths: List[List[TimeCoordinate]]):
        for path in paths:
            self.allocate_path_for_agent(agent, path)

    def allocate_spaces_for_agent(self, agent: Agent, spaces: List[List[TimeCoordinate]]):
        for path in spaces:
            self.allocate_space_for_agent(agent, path)

    def allocate_path_for_agent(self, agent: Agent, path: List[TimeCoordinate]):
        if len(path) == 0:
            return
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

    def allocate_space_for_agent(self, agent: Agent, space: List[TimeCoordinate]):
        agent.add_allocated_paths(space)
        start_locations: Dict[str, TimeCoordinate] = {}
        end_locations: Dict[str, TimeCoordinate] = {}
        for coord in space:
            key = coord.get_key()
            if key not in start_locations:
                start_locations[key] = coord
                end_locations[key] = coord
                continue
            end_locations[key] = coord

        for key in start_locations:
            self.tree.insert(agent.id, start_locations[key].list_rep() + end_locations[key].list_rep())

    def allocate_paths_for_agents(self, agents_paths: Dict[Agent, List[List[TimeCoordinate]]], time_step: Tick):
        for agent, paths in agents_paths.items():
            if agent.id in self._agents:
                self.deallocate_agent(agent, time_step)
            else:
                self._agents[agent.id] = agent

            if agent.agent_type == AgentType.STATIONARY:
                self.allocate_spaces_for_agent(agent, paths)
            else:
                self.allocate_paths_for_agent(agent, paths)

    def original_agents(self, agents_paths: Dict[Agent, List[List[TimeCoordinate]]], newcomers: List[Agent]):
        res = {}
        for agent, path in agents_paths.items():
            newcomer_ids = [_agent.id for _agent in newcomers]
            if agent.id in newcomer_ids:
                res[newcomers[newcomer_ids.index(agent.id)]] = path
            else:
                res[self._agents[agent.id]] = path
        return res

    def is_blocked(self, coord: TimeCoordinate, radius: int = 0, speed: int = 0) -> bool:
        blockers = self.blocker_tree.intersection((
            coord.x - radius, coord.y - radius, coord.z - radius, coord.t,
            coord.x + radius, coord.y + radius, coord.z + radius, coord.t + speed
        ))
        for blocker_id in blockers:
            if self.blockers[blocker_id].is_blocking(coord):
                return True
        return False

    def add_agent(self, agent: Agent):
        self._agents[agent.id] = agent

    def get_agents(self):
        return self._agents

    def get_agent(self, agent_id: int):
        return self._agents[agent_id]

    def get_dim(self):
        return self._dimension

    def is_valid_for_allocation(self, coords: TimeCoordinate, agent: Agent) -> bool: #Todo: Could be in the near-field of another agent
        radius: int = agent.near_radius
        agents = self.intersect(coords, radius, agent.speed)
        return len(list(agents)) == 0 and not self.is_blocked(coords, radius, agent.speed)

    def intersect(self, coords: TimeCoordinate, radius: int = 0, speed: int = 0):
        return self.tree.intersection((
            coords.x - radius, coords.y - radius, coords.z - radius, coords.t,
            coords.x + radius, coords.y + radius, coords.z + radius, coords.t + speed
        ))

    def get_agents_at(self, coords: TimeCoordinate) -> List[Agent]:
        return [self._agents[_id] for _id in self.tree.intersection(coords.tree_query_point_rep())]

    def visualize(self, current_time_step, before=0, nr_steps=1):
        for t in range(current_time_step - before, current_time_step + nr_steps):
            print(f"t = {t}")
            for y in range(self._dimension.y):
                print(f"y={y: >2}", end="")
                for i in range(self._dimension.x):
                    print(f" {i: >4}", end="")
                print("  -> X")
                for z in range(self._dimension.z):
                    print(f"  {z: >2} ", end="")
                    for x in range(self._dimension.x):
                        coord = TimeCoordinate(x, y, z, Tick(t))
                        agents = list(self.tree.intersection(coord.tree_query_point_rep()))
                        if len(agents) > 0:
                            print(f" {','.join(map(str, agents))}".rjust(5, ' '), end="")

                        elif self.is_blocked(coord):
                            print("✖".rjust(5, ' '), end="")
                        else:
                            print(".".rjust(5, ' '), end="")
                    print("")
                print("")
            print(" ↓\n Z")

    def new_clear(self):
        new_env = Environment(self._dimension, list(self.blockers.values()), self.maptiles)
        new_env.blocker_tree = self.blocker_tree
        return new_env

    def clone(self):
        cloned = Environment(self._dimension, list(self.blockers.values()), self.maptiles)
        if len(self.tree) > 0:
            for item in self.tree.intersection(self.tree.bounds, objects=True):
                cloned.tree.insert(item.id, item.bbox)
        cloned.blocker_tree = self.blocker_tree
        for agent in self._agents.values():
            cloned.add_agent(agent.clone())
        return cloned
