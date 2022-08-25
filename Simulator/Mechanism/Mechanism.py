from typing import List

from Simulator.Allocations.Allocation import Allocation
from Simulator.Bids.Bid import Bid
from Simulator.Environment.Environment import Environment
from Simulator.Mechanism.Allocator import Allocator
from Simulator.Mechanism.PaymentRule import PaymentRule


class Mechanism:
    def __init__(self, allocator: Allocator, payment_rule: PaymentRule):
        self.allocator = allocator
        self.payment_rule = payment_rule

    def do(self, bids: List[Bid], environment: Environment, tick: int) -> List[Allocation]:
        allocations = self.allocator.allocate(bids, environment, tick)
        self.payment_rule.calculate_payments(allocations)
        return allocations
