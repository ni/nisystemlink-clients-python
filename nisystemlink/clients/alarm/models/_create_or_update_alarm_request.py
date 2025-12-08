from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._alarm import AlarmTransitionType


class CreateAlarmTransition(JsonModel):
    """Contains information about a transition used to create or update an instance of an alarm."""

    transition_type: AlarmTransitionType
    """Specifies a type of alarm transition: CLEAR or SET."""

    occurred_at: Optional[datetime] = None
    """The date and time when the transition occurred."""

    severity_level: Optional[int] = 2
    """The severity of the transition.

    Valid values for CLEAR transitions are [-1, -1].
    Valid values for SET transitions are [1, infinity].
    Note that the SystemLink Alarm UI only has display strings for SET severities in the range [1, 4].
    """

    value: Optional[str] = None
    """The value that caused the alarm to transition."""

    condition: Optional[str] = None
    """A description of the condition associated with the transition."""

    short_text: Optional[str] = None
    """A short description of the condition."""

    detail_text: Optional[str] = None
    """A detailed description of the condition."""

    keywords: Optional[List[str]] = None
    """Words or phrases associated with a transition.

    Useful for attaching metadata to a transition which could aid in an investigation
    into an alarm's root cause in the future.
    """

    properties: Optional[Dict[str, str]] = None
    """Key-value pair metadata associated with a transition.

    Useful for attaching additional metadata to a transition which could aid in an investigation
    into an alarm's root cause in the future. Property keys must be between 1 and 255 characters.
    Property values can be up to 1000 characters.
    """


class CreateOrUpdateAlarmRequest(JsonModel):
    """Contains information about the alarm to create or update.

    If an alarm is being updated, only alarmId, workspace, and transition are applied.
    """

    alarm_id: str
    """A value meant to uniquely identify the particular process or condition tracked by the alarm.

    For example, alarms created by a tag rule engine might have their alarmIds set to the
    concatenation of the path of the tag which caused the rule to be triggered and the ID of the rule.
    """

    workspace: Optional[str] = None
    """The ID of the workspace in which to create or update the alarm.

    When not specified, the default workspace is used based on the requesting user.
    """

    transition: CreateAlarmTransition
    """Contains information about a transition used to create or update an instance of an alarm."""

    notification_strategy_ids: Optional[List[str]] = None
    """The IDs of the notification strategies which should be triggered.

    These are triggered if this request results in an alarm being created or
    transitioning to a new highest severity.
    """

    created_by: Optional[str] = None
    """An identifier for who or what created the alarm.

    This is usually used to identify the particular rule engine which requested
    that the alarm be created.
    """

    channel: Optional[str] = None
    """An identifier for the tag or resource associated with the alarm."""

    resource_type: Optional[str] = None
    """The type of resource associated with the alarm."""

    display_name: Optional[str] = None
    """Optional display name for the alarm. Display names do not need to be unique."""

    description: Optional[str] = None
    """Optional description text for the alarm."""

    keywords: Optional[List[str]] = None
    """Words or phrases associated with the alarm.

    Alarms can be tagged with keywords to make it easier to find them with queries.
    """

    properties: Optional[Dict[str, str]] = None
    """The alarm's custom properties. Property keys must be between 1 and 255 characters.
    Property values can be up to 1000 characters."""
