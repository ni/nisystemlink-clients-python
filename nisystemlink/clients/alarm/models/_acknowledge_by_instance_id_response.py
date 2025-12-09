from typing import List

from nisystemlink.clients.alarm.models._partial_success_response_base import (
    AlarmInstancesPartialSuccess,
)


class AcknowledgeByInstanceIdResponse(AlarmInstancesPartialSuccess):
    """Contains information about which alarms were acknowledged."""

    acknowledged: List[str]
    """The instanceIds of the alarms that were successfully acknowledged."""
