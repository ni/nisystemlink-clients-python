from enum import Enum
from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class StatusType(str, Enum):
    """The types of statuses that a result can have."""

    LOOPING = "LOOPING"
    SKIPPED = "SKIPPED"
    CUSTOM = "CUSTOM"
    DONE = "DONE"
    PASSED = "PASSED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"
    ERRORED = "ERRORED"
    TIMED_OUT = "TIMED_OUT"


class Status(JsonModel):
    """Contains information about a status object."""

    status_type: StatusType
    """The type of status."""

    status_name: Optional[str]
    """The name of the status."""

    @staticmethod
    def LOOPING() -> "Status":
        return Status(status_type=StatusType.LOOPING)

    @staticmethod
    def SKIPPED() -> "Status":
        return Status(status_type=StatusType.SKIPPED)

    @staticmethod
    def DONE() -> "Status":
        return Status(status_type=StatusType.DONE)

    @staticmethod
    def PASSED() -> "Status":
        return Status(status_type=StatusType.PASSED)

    @staticmethod
    def FAILED() -> "Status":
        return Status(status_type=StatusType.FAILED)

    @staticmethod
    def RUNNING() -> "Status":
        return Status(status_type=StatusType.RUNNING)

    @staticmethod
    def WAITING() -> "Status":
        return Status(status_type=StatusType.WAITING)

    @staticmethod
    def TERMINATED() -> "Status":
        return Status(status_type=StatusType.TERMINATED)

    @staticmethod
    def ERRORED() -> "Status":
        return Status(status_type=StatusType.ERRORED)

    @staticmethod
    def TIMED_OUT() -> "Status":
        return Status(status_type=StatusType.TIMED_OUT)
