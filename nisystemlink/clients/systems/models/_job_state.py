from enum import Enum


class JobState(Enum):
    """The state of the jobs."""

    SUCCEEDED = "SUCCEEDED"
    OUTOFQUEUE = "OUTOFQUEUE"
    INQUEUE = "INQUEUE"
    INPROGRESS = "INPROGRESS"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
