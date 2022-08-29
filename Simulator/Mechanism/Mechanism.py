from typing import List

from Simulator.Agents.Agent import Agent
from Simulator.Allocations.Allocation import Allocation
from Simulator.Environment.Environment import Environment
from Simulator.Mechanism.Allocator import Allocator
from Simulator.Mechanism.PaymentRule import PaymentRule


class Mechanism:
    def __init__(self, allocator: Allocator, payment_rule: PaymentRule):
        self.allocator = allocator
        self.payment_rule = payment_rule

    def do(self, agents: List[Agent], environment: Environment, tick: int) -> List[Allocation]:
        allocations = self.allocator.allocate(agents, environment, tick)
        self.payment_rule.calculate_preliminary_payments(allocations, self.allocator.get_bid_tracker())
        return allocations

    def calculate_final_payments(self, environment: Environment):
        return self.payment_rule.calculate_final_payments(environment, self.allocator.get_bid_tracker())
