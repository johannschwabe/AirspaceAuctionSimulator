from typing import Optional

from simulator.agents import Agent
from simulator.bids.Bid import Bid
from simulator.Coordinates.TimeCoordinate import TimeCoordinate


class Field:
	def __init__(self, coordinates: TimeCoordinate):
		self.coordinates: TimeCoordinate = coordinates

		self.allocated_to: Optional[Agent.Agent] = None
		self.occupied_by: Optional[Agent.Agent] = None
		self.bid: Optional[Bid] = None

	def is_occupied(self) -> bool:
		return self.occupied_by is not None

	def is_allocated(self) -> bool:
		return self.allocated_to is not None
