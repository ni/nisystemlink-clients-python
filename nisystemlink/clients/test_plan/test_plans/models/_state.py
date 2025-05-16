from enum import Enum


class State(Enum):
    """The state of the test plan."""

    New = "NEW"
    Defined = "DEFINED"
    Reviewed = "REVIEWED"
    Scheduled = "SCHEDULED"
    InProgress = "IN_PROGRESS"
    PendingApproval = "PENDING_APPROVAL"
    Closed = "CLOSED"
    Canceled = "CANCELED"
