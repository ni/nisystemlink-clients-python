from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class AlarmSeverityLevel(IntEnum):
    """Well-known alarm severity levels.

    The service supports custom severity levels greater than 4, but it is generally discouraged.
    The SystemLink Alarm UI only has display strings for severity levels in the range [1, 4].
    """

    CLEAR = -1
    """Severity level for cleared alarms."""

    LOW = 1
    """Low severity level."""

    MODERATE = 2
    """Moderate severity level."""

    HIGH = 3
    """High severity level."""

    CRITICAL = 4
    """Critical severity level."""


class AlarmTransitionType(str, Enum):
    """Specifies a type of alarm transition."""

    CLEAR = "CLEAR"
    """The transition corresponds to the clearing of the condition tracked by the alarm."""

    SET = "SET"
    """The transition corresponds to the condition tracked by the alarm entering into the triggered state."""


class AlarmTransition(JsonModel):
    """A transition within an instance, or occurrence, of an alarm.

    Alarm transitions record changes to an alarm's clear field as well as an alarm
    increasing or decreasing in severity.
    """

    transition_type: AlarmTransitionType
    """Specifies a type of alarm transition: CLEAR or SET."""

    occurred_at: datetime
    """The date and time when the transition occurred."""

    severity_level: int
    """The severity of the transition.

    Valid values for CLEAR transitions are [-1, -1].
    Valid values for SET transitions are [1, 2147483647].
    Note that the SystemLink Alarm UI only has display strings for SET severities in the range [1, 4].
    The :class:`AlarmSeverityLevel` enum provides values for standard severity levels.
    """

    value: str
    """The value that caused the alarm to transition."""

    condition: str
    """A description of the condition associated with the transition."""

    short_text: str
    """A short description of the condition."""

    detail_text: str
    """A detailed description of the condition."""

    keywords: List[str]
    """Words or phrases associated with a transition.

    Useful for attaching metadata to a transition which could aid in an investigation
    into an alarm's root cause in the future.
    """

    properties: Dict[str, str]
    """Key-value pair metadata associated with a transition.

    Useful for attaching additional metadata to a transition which could aid in an investigation
    into an alarm's root cause in the future. Property keys must be between 1 and 255 characters.
    """


class Alarm(JsonModel):
    """An individual instance, or occurrence, of an alarm.

    The lifecycle of an alarm begins the first time it is triggered and ends when it has been
    both acknowledged and cleared. The service enforces the invariant that there can be at most
    one active=True alarm with the same alarmId.
    """

    instance_id: str
    """The unique identifier for the instance, or occurrence, of the alarm."""

    alarm_id: str
    """A value meant to uniquely identify the particular process or condition tracked by the alarm.

    For example, alarms created by a tag rule engine might have their alarmIds set to the
    concatenation of the path of the tag which caused the rule to be triggered and the ID of the rule.
    """

    workspace: str
    """The workspace the alarm belongs to."""

    active: bool
    """Whether or not the alarm is active.

    An active alarm deserves human or automated attention. Alarms always begin life with active=True.
    This field will be automatically set to false when the clear and acknowledged fields are set to true.
    """

    clear: bool
    """When set to true, the condition that triggered the alarm no longer matches the trigger condition.

    When an alarm is created, clear is initially set to false. The creator of the alarm (typically a
    rule engine or application element of some sort) may determine that the trigger condition no longer
    applies, and may send an update, clearing the alarm. Clearing the alarm does not deactivate the alarm,
    unless the alarm had previously been acknowledged. As long as the alarm is active=true, the alarm may
    transition from clear=True to clear=False (or vice versa) multiple times.
    """

    acknowledged: bool
    """When set to true, the alarm has been acknowledged by an alarm handler, which is typically a human.

    Alarms always begin life with acknowledged=False. Acknowledging an alarm will not affect the active
    flag unless clear is also true. When clear and acknowledged are true, the alarm will become inactive
    (active=False). This field is automatically reset to false when the alarm's highestSeverityLevel field increases.
    """

    acknowledged_at: datetime | None
    """The date and time when the alarm instance was acknowledged.

    This field will be cleared when the alarm's highestSeverityLevel field increases.
    """

    acknowledged_by: str | None
    """The userId of the individual who acknowledged the alarm.

    This field will be cleared when the alarm's highestSeverityLevel field increases.
    """

    occurred_at: datetime
    """The date and time when the alarm was created/first occurred."""

    updated_at: datetime
    """The date and time when the alarm was last updated or modified."""

    created_by: str
    """An identifier for who or what created the alarm.

    This is usually used to identify the particular rule engine which requested that the alarm be created.
    """

    transitions: List[AlarmTransition]
    """A collection of AlarmTransitions for the alarm.

    The service stores the first transition and the most recent 99 other transitions by default.
    The configuration for the service determines the total number of stored transitions per alarm.
    """

    transition_overflow_count: int
    """The number of transitions which overflowed the transitions field for the alarm.

    For example, if the alarm transitioned 250 times, transitionOverflowCount is set to 150 and
    transitions contains the first and most recent 99 transitions. The configuration for the service
    determines the total number of stored transitions per alarm.
    """

    notification_strategy_ids: List[str]
    """The IDs of the notification strategies which will be triggered.

    These are triggered when the alarm is first created and when its highestSeverityLevel increases.
    """

    current_severity_level: int
    """The current severity level of the alarm."""

    highest_severity_level: int
    """The highest severity level that the alarm has ever been in."""

    most_recent_set_occurred_at: datetime | None
    """The date and time of the most recent occurrence of a SET transition.

    This property only considers transitions that cause an alarm state change.
    """

    most_recent_transition_occurred_at: datetime | None
    """The date and time of the most recent occurrence of a transition.

    This property only considers transitions that cause an alarm state change.
    """

    channel: str
    """An identifier for the tag or resource associated with the alarm."""

    condition: str
    """A description of the condition associated with the alarm."""

    display_name: str
    """Optional display name for the alarm. Display names do not need to be unique."""

    description: str
    """Optional description text for the alarm."""

    keywords: List[str]
    """Words or phrases associated with the alarm.

    Alarms can be tagged with keywords to make it easier to find them with queries.
    """

    notes: List[Any]
    """A collection of notes for a given alarm instance.

    Notes are not currently supported and this will always be an empty list.
    """

    properties: Dict[str, str]
    """The alarm's custom properties."""

    resource_type: str
    """The type of resource associated with the alarm."""
