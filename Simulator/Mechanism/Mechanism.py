from typing import List, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from ..Agents.Agent import Agent
    from ..Allocations.Allocation import Allocation
    from ..Environment.Environment import Environment
    from ..Mechanism.Allocator import Allocator
    from ..Mechanism.PaymentRule import PaymentRule


class Mechanism:
    """
    Wrapper to plug in allocator and payment rule.
    Generates allocations with corresponding payments.
    """

    def __init__(self, allocator: "Allocator", payment_rule: "PaymentRule"):
        """
        Initialize allocator to generate new allocations and payment-rule to calculate payments for the allocations.
        :param allocator:
        :param payment_rule:
        """
        self.allocator = allocator
        self.payment_rule = payment_rule

    def do(self, agents: List["Agent"], environment: "Environment", tick: int) -> Dict["Agent", "Allocation"]:
        """
        Allocate agents and calculate payments for allocations.
        :param agents:
        :param environment:
        :param tick:
        :return:
        """
        allocations = self.allocator.allocate(agents, environment, tick)
        self.payment_rule.calculate_payments(allocations, self.allocator.get_bid_tracker())
        return allocations
