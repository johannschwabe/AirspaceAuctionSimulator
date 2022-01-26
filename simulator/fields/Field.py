from typing import Optional

from simulator.agents.Agent import Agent
from simulator.bids.Bid import Bid
from simulator.coordinates.TimeCoordinates import TimeCoordinates


class Field:
	def __init__(self, coordinates: TimeCoordinates, ):
		self.coordinates: TimeCoordinates = coordinates

		self.allocated_to: Optional[Agent] = None
		self.occupied_by: Optional[Agent] = None
		self.bid: Optional[Bid] = None

	def is_occupied(self) -> bool:
		return self.occupied_by is None

	def is_allocated(self) -> bool:
		return self.allocated_to is None
