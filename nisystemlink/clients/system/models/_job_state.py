from enum import Enum


class JobState(Enum):
    """The state of the job."""

    SUCCEEDED = "SUCCEEDED"
    OUTOFQUEUE = "OUTOFQUEUE"
    INQUEUE = "INQUEUE"
    INPROGRESS = "INPROGRESS"
    CANCELED = "CANCELED"
    FAILED = "FAILED"
