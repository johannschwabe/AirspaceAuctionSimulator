from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation
    from ..Environment.Environment import Environment
    from ..Mechanism.Allocator import Allocator
    from ..Mechanism.PaymentRule import PaymentRule


class Mechanism:
    def __init__(self, allocator: "Allocator", payment_rule: "PaymentRule"):
        self.allocator = allocator
        self.payment_rule = payment_rule

    def do(self, agents: List["Agent"], environment: "Environment", tick: int) -> List["Allocation"]:
        allocations = self.allocator.allocate(agents, environment, tick)
        self.payment_rule.calculate_preliminary_payments(allocations, self.allocator.get_bid_tracker())
        return allocations

    def calculate_final_payments(self, environment: "Environment"):
        return self.payment_rule.calculate_final_payments(environment, self.allocator.get_bid_tracker())
