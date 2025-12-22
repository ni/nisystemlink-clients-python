from typing import List

from nisystemlink.clients.alarm.models._alarm_instances_partial_success import (
    AlarmInstancesPartialSuccess,
)


class AcknowledgeAlarmsResponse(AlarmInstancesPartialSuccess):
    """Contains information about which alarms were acknowledged."""

    acknowledged: List[str]
    """The instanceIds of the alarms that were successfully acknowledged."""
