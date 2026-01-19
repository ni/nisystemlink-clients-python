from datetime import datetime
from enum import Enum
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class TransitionInclusionOption(str, Enum):
    """Determines which transitions to include in the query results."""

    NONE = "NONE"
    """No transitions are included."""

    MOST_RECENT_ONLY = "MOST_RECENT_ONLY"
    """The most recent transition is included."""

    ALL = "ALL"
    """All transitions are included."""


class AlarmOrderBy(str, Enum):
    """The sort order of the returned list of alarms."""

    UPDATED_AT = "UPDATED_AT"
    """The date and time the alarm was last updated."""


class QueryAlarmsWithFilterRequest(JsonModel):
    """Contains filter information for querying alarms."""

    filter: str | None = None
    """The alarm query filter in `Dynamic LINQ`_ format.

    .. _Dynamic LINQ: https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language

    Allowed properties in the filter are:

    * ``acknowledged``: Boolean value that indicates an alarm acknowledgment
    * ``acknowledgedAt``: DateTime value that represents when the alarm was acknowledged
    * ``active``: Boolean value that indicates an active alarm
    * ``alarmId``: String value that identifies the process or condition tracked by the alarm
    * ``channel``: String value that identifies the tag or resource associated with the alarm
    * ``clear``: Boolean value that indicates an alarm clearance
    * ``createdBy``: String value that identifies the user that created the alarm
    * ``currentSeverityLevel``: Int32 value that represents the severity level of the alarm
    * ``description``: String value that describes the alarm
    * ``displayName``: String value that represents the alarm name in the user interface
    * ``highestSeverityLevel``: Int32 value that represents the highest severity level of the alarm
    * ``keywords``: List of string values associated with the alarm
    * ``mostRecentSetOccurredAt``: DateTime value that represents when the most recent set transition occurred
    * ``mostRecentTransitionOccurredAt``: DateTime value that represents when the most recent transition occurred
    * ``occurredAt``: DateTime value that represents when the alarm was created or first occurred
    * ``occurredWithin``: TimeSpan value that represents when the alarm was created or first occurred
    * ``properties``: Dictionary that contains the string keys and values representing alarm metadata
    * ``resourceType``: String value that represents the resource type of the alarm
    * ``workspace``: String ID of the workspace to use in the query
    * ``workspaceName``: String name of the workspace of the alarm

    Allowed constants in the filter are:

    * ``RelativeTime.CurrentDay``: TimeSpan representing the elapsed time between now and
      the start of the current day
    * ``RelativeTime.CurrentWeek``: TimeSpan representing the elapsed time between now and
      the start of the current week
    * ``RelativeTime.CurrentMonth``: TimeSpan representing the elapsed time between now and
      the start of the current month
    * ``RelativeTime.CurrentYear``: TimeSpan representing the elapsed time between now and
      the start of the current year
    """

    substitutions: List[bool | int | str | None] | None = None
    """Makes substitutions in the query filter expression.

    Substitutions for the query expression are indicated by non-negative integers that are
    prefixed with the @ symbol. Each substitution in the given expression will be replaced by
    the element at the corresponding index (zero-based) in this list.
    """

    return_most_recently_occurred_only: bool = False
    """Whether or not the Alarm Service should group the alarms matched by this query by alarmId.

    When true, only return the most recent alarm for each grouping. In this context, recency is
    based on when the alarm occurred, not when it was last updated.
    """

    transition_inclusion_option: TransitionInclusionOption | None = None
    """Determines which transitions to include in the query results, if any."""

    reference_time: datetime | None = None
    """The date and time to use as the reference point for RelativeTime filters.

    Includes time zone information. Defaults to the current time in UTC.
    """

    take: int | None = 1000
    """Limits the returned list to the specified number of results. Maximum is 1000."""

    order_by: AlarmOrderBy | None = None
    """The sort order of the returned list of alarms.

    By default, alarms are sorted in ascending order based on the specified value.
    """

    order_by_descending: bool = False
    """Whether to sort descending instead of ascending.

    The elements in the list are sorted ascending by default. If true, sorts descending.
    """

    continuation_token: str | None = None
    """A token which allows the user to resume a query at the next item in the matching results.

    When querying, a token will be returned if a query may be continued. To obtain the next page
    of results, pass the token to the service on a subsequent request.
    """

    return_count: bool = False
    """Whether to return the total number of alarms that match the provided filter.

    This disregards the take value.
    """
