class Coords:
	dim_x = 0
	dim_y = 0
	dim_z = 0
	dim_t = 0
	def __init__(self, x, y, z, t):
		self.x = x
		self.y = y
		self.z = z
		self.t = t

	def get_key(self):
		return f"{self.x}_{self.y}_{self.z}_{self.t}"

	def __repr__(self):
		return f"({self.x}, {self.y}, {self.z}, {self.t})"

	def __eq__(self, other):
		return self.x == other.x and \
		       self.y == other.y and \
		       self.z == other.z and \
		       self.t == other.t

	def intertemporal_equal(self, other):
		return self.x == other.x and \
		       self.y == other.y and \
		       self.z == other.z

	def adjacent(self, delta_t):
		res = [Coords(self.x, self.y, self.z, self.t + 1)]
		if self.x > 0:
			res.append(Coords(self.x-1, self.y, self.z, self.t + delta_t))
		if self.y > 0:
			res.append(Coords(self.x, self.y-1, self.z, self.t + delta_t))
		if self.z > 0:
			res.append(Coords(self.x, self.y, self.z-1, self.t + delta_t))
		if self.x < Coords.dim_x - 1:
			res.append(Coords(self.x+1, self.y, self.z, self.t + delta_t))
		if self.y < Coords.dim_y - 1:
			res.append(Coords(self.x, self.y+1, self.z, self.t + delta_t))
		if self.z < Coords.dim_z - 1:
			res.append(Coords(self.x, self.y, self.z+1, self.t + delta_t))
		return res