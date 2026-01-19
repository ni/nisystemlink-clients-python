from typing import List

from nisystemlink.clients.alarm.models._alarm_instances_partial_success import (
    AlarmInstancesPartialSuccess,
)


class DeleteAlarmsResponse(AlarmInstancesPartialSuccess):
    """Contains information about alarms that were deleted."""

    deleted: List[str]
    """The instanceIds of the alarms that were successfully deleted."""
