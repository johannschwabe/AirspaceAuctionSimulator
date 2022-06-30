from enum import Enum


class Reason(Enum):
    FIRST_ALLOCATION = 0
    AGENT = 1
    BLOCKER = 2
    OWNER = 3
    NOT_IMPLEMENTED = 4
    ALLOCATION_FAILED = 5
