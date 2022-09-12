from enum import Enum


class AllocationType(Enum):
    FIRST_ALLOCATION = "FIRST_ALLOCATION"
    AGENT = "AGENT"
    ALLOCATION_FAILED = "ALLOCATION_FAILED"
    CRASH = "CRASH"
