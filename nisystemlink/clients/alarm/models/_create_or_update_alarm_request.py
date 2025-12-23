from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import model_validator

from ._alarm import AlarmSeverityLevel, AlarmTransitionType


class CreateAlarmTransition(JsonModel):
    """Contains information about a transition used to create or update an instance of an alarm."""

    transition_type: AlarmTransitionType
    """Specifies a type of alarm transition: CLEAR or SET."""

    occurred_at: datetime | None = None
    """The date and time when the transition occurred."""

    severity_level: int | None = 2
    """The severity of the transition.

    Valid values for CLEAR transitions are [-1, -1].
    Valid values for SET transitions are [1, 2147483647].
    Note that the SystemLink Alarm UI only has display strings for SET severities in the range [1, 4].
    The :class:`AlarmSeverityLevel` enum provides values for standard severity levels.
    """

    value: str | None = None
    """The value that caused the alarm to transition."""

    condition: str | None = None
    """A description of the condition associated with the transition."""

    short_text: str | None = None
    """A short description of the condition."""

    detail_text: str | None = None
    """A detailed description of the condition."""

    keywords: List[str] | None = None
    """Words or phrases associated with a transition.

    Useful for attaching metadata to a transition which could aid in an investigation
    into an alarm's root cause in the future.
    """

    properties: Dict[str, str] | None = None
    """Key-value pair metadata associated with a transition.

    Useful for attaching additional metadata to a transition which could aid in an investigation
    into an alarm's root cause in the future. Property keys must be between 1 and 255 characters.
    Property values can be up to 1000 characters.
    """


class SetAlarmTransition(CreateAlarmTransition):
    """Contains information about a SET transition used to create or update an instance of an alarm.

    This is a convenience class that automatically sets transition_type to SET.
    """

    transition_type: AlarmTransitionType = AlarmTransitionType.SET

    @model_validator(mode="after")
    def _set_transition_type(self) -> "SetAlarmTransition":
        self.transition_type = AlarmTransitionType.SET
        return self


class ClearAlarmTransition(CreateAlarmTransition):
    """Contains information about a CLEAR transition used to clear an instance of an alarm.

    This is a convenience class that automatically sets transition_type to CLEAR
    and severity_level to -1 (CLEAR severity).
    """

    transition_type: AlarmTransitionType = AlarmTransitionType.CLEAR
    severity_level: int | None = AlarmSeverityLevel.CLEAR

    @model_validator(mode="after")
    def _set_clear_defaults(self) -> "ClearAlarmTransition":
        self.transition_type = AlarmTransitionType.CLEAR
        self.severity_level = AlarmSeverityLevel.CLEAR
        return self


class CreateOrUpdateAlarmRequest(JsonModel):
    """Contains information about the alarm to create or update.

    If an alarm is being updated, only alarmId, workspace, and transition are applied.
    """

    alarm_id: str
    """A value meant to uniquely identify the particular process or condition tracked by the alarm.

    For example, alarms created by a tag rule engine might have their alarmIds set to the
    concatenation of the path of the tag which caused the rule to be triggered and the ID of the rule.
    """

    workspace: str | None = None
    """The ID of the workspace in which to create or update the alarm.

    When not specified, the default workspace is used based on the requesting user.
    """

    transition: CreateAlarmTransition
    """Contains information about a transition used to create or update an instance of an alarm.

    Consider using SetAlarmTransition to trigger an alarm or ClearAlarmTransition to clear an alarm.
    These convenience classes automatically set the appropriate transition type and severity level.
    """

    notification_strategy_ids: List[str] | None = None
    """The IDs of the notification strategies which should be triggered.

    These are triggered if this request results in an alarm being created or
    transitioning to a new highest severity.
    """

    created_by: str | None = None
    """An identifier for who or what created the alarm.

    This is usually used to identify the particular rule engine which requested
    that the alarm be created.
    """

    channel: str | None = None
    """An identifier for the tag or resource associated with the alarm."""

    resource_type: str | None = None
    """The type of resource associated with the alarm."""

    display_name: str | None = None
    """Optional display name for the alarm. Display names do not need to be unique."""

    description: str | None = None
    """Optional description text for the alarm."""

    keywords: List[str] | None = None
    """Words or phrases associated with the alarm.

    Alarms can be tagged with keywords to make it easier to find them with queries.
    """

    properties: Dict[str, str] | None = None
    """The alarm's custom properties. Property keys must be between 1 and 255 characters.
    Property values can be up to 1000 characters."""
