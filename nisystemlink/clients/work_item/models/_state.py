from enum import Enum


class State(Enum):
    """The state of the work item."""

    NEW = "NEW"
    DEFINED = "DEFINED"
    REVIEWED = "REVIEWED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"
