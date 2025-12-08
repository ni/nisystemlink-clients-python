from typing import List

from nisystemlink.clients.alarm.models._partial_success_response_base import (
    PartialSuccessResponseBase,
)


class DeleteByInstanceIdResponse(PartialSuccessResponseBase):
    """Contains information about which alarms were deleted."""

    deleted: List[str]
    """The instanceIds of the alarms that were successfully deleted."""
