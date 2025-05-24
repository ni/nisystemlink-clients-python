from enum import Enum


class State(Enum):
    """The state of the test plan."""

    NEW = "NEW"
    DEFINED = "DEFINED"
    REVIEWED = "REVIEWED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"
