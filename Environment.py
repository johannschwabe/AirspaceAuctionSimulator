
from abc import ABC, abstractmethod
from Agent import Agent
from Field import Field
from coords import Coords



class Environment(ABC):
	def __init__(self):
		self.agents = []
		self.fields = {}         # x_y_z_t -> Field

	@abstractmethod
	def reset(self):
		pass

	@abstractmethod
	def add_agent(self, agent: Agent, time_step):
		pass

	def is_blocked(self, coords):
		intertemporal_block_key = f"{coords.x}_{coords.y}_{coords.z}_-1"
		if intertemporal_block_key in self.fields and self.fields[intertemporal_block_key].blocked:
			return self.fields[intertemporal_block_key]
		return None

	def block(self, coords):
		intertemporal_block_key = f"{coords.x}_{coords.y}_{coords.z}_-1"
		new_field = Field()
		new_field.blocked = True
		self.fields[intertemporal_block_key] = new_field

	def get_field(self, coords, creating):
		blocked = self.is_blocked(coords)
		if blocked:
			return blocked
		key = coords.get_key()
		if key not in self.fields:
			if creating:
				new_field = Field()
				self.fields[key] = new_field
			else:
				return None
		return self.fields[key]
	@abstractmethod
	def move(self):
		pass

	def visualize(self, current_time_step, before = 0, nr_steps=1):
		for t in range(current_time_step - before, current_time_step+nr_steps):
			print(f"t = {t}")
			for z in range(Coords.dim_z):
				print(f"z={z: >2}", end="")
				for i in range(Coords.dim_x):
					print(f" {i: >2} ", end="")
				print("  -> X")
				for y in range(Coords.dim_y):
					print(f"  {y: >2} ", end="")
					for x in range(Coords.dim_x):
						field = self.get_field(Coords(x,y,z,t), False)
						if field:
							if field.reserved_for and t == current_time_step:
								print(f"|{field.reserved_for.id}| ", end="")
							elif field.reserved_for:
								print(f" {field.reserved_for.id}  ", end="")
							elif field.blocked:
								print(" ✖  ", end="")
						else:
							print(" .  ", end="")
					print("")
				print("")
			print(" ↓\n Y")

	# Implemented based on https://www.annytab.com/a-star-search-algorithm-in-python/
	def astar(self, start: Coords, end: Coords, agent, speed=1):
		open = []
		closed = []

		start_node = Node(start, None)
		end = Node(end, None)

		open.append(start_node)

		while len(open) > 0:
			open.sort()
			current_node = open.pop(0)
			closed.append(current_node)
			if current_node.posi.intertemporal_equal(end.posi):
				path = []
				while current_node != start_node:
					path.append(current_node.posi)
					current_node = current_node.parent
				return path[::-1]

			neighbors = current_node.posi.adjacent(1)
			for next in neighbors:
				field = self.get_field(next, False)
				if not field or (
						(field.reserved_for is None or field.reserved_for == agent) and
						 not field.blocked):
					neighbor = Node(next, current_node)
					if neighbor in closed:
						other = closed[closed.index(neighbor)]
						if other.posi.t > neighbor.posi.t:
							other.parent = neighbor.parent
							other.posi.t = neighbor.posi.t
						continue

					neighbor.g = current_node.g + 1
					neighbor.h = distance(neighbor.posi, end.posi)
					neighbor.f = neighbor.g + neighbor.h

					if neighbor in open:
						alternative_index = open.index(neighbor)
						alternative = open[alternative_index]
						if alternative.f > neighbor.f:
							open[alternative_index] = neighbor
					else:
						open.append(neighbor)



def distance(start: Coords, end: Coords):
	return abs(start.x - end.x) + abs(start.y - end.y) + abs(start.z - end.z)

class Node:
	def __init__(self, position: Coords, parent):
		self.posi = position
		self.parent = parent
		self.g = 0      # Distance to start node
		self.h = 0      # Distance to goal node
		self.f = 0      # Total cost

	def __eq__(self, other):
		return self.posi.intertemporal_equal(other.posi)

	def __lt__(self, other):
		return self.f < other.f

	def __repr__(self):
		return f"{self.posi}: {self.f}"