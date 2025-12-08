from typing import List

from nisystemlink.clients.alarm.models._partial_success_response_base import (
    PartialSuccessResponseBase,
)


class AcknowledgeByInstanceIdResponse(PartialSuccessResponseBase):
    """Contains information about which alarms were acknowledged."""

    acknowledged: List[str]
    """The instanceIds of the alarms which were successfully acknowledged."""
