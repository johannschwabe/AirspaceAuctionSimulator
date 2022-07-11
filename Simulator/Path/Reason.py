from enum import Enum
from typing import List


class Reasons(Enum):
    FIRST_ALLOCATION = "FIRST_ALLOCATION"
    AGENT = "AGENT"
    BLOCKER = "BLOCKER"
    OWNER = "OWNER"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    ALLOCATION_FAILED = "ALLOCATION_FAILED"


class Reason:
    def __init__(self, reason: Reasons):
        self.reason = reason


class AgentReason(Reason):
    def __init__(self, reason: Reasons, colliding_agents_ids: List[int]):
        super().__init__(reason)
        self.colliding_agents_ids = colliding_agents_ids

