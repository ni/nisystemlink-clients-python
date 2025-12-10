from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

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

    filter: Optional[str] = None
    """The alarm query filter in Dynamic Linq.

    Allowed properties in the filter are: acknowledged, acknowledgedAt, active, alarmId,
    channel, clear, createdBy, currentSeverityLevel, description, displayName,
    highestSeverityLevel, keywords, mostRecentSetOccurredAt, mostRecentTransitionOccurredAt,
    occurredAt, occurredWithin, properties, resourceType, workspace, workspaceName.

    Allowed constants: RelativeTime.CurrentDay, RelativeTime.CurrentWeek,
    RelativeTime.CurrentMonth, RelativeTime.CurrentYear.
    """

    substitutions: Optional[List[Union[bool, int, str, None]]] = None
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

    transition_inclusion_option: Optional[TransitionInclusionOption] = None
    """Determines which transitions to include in the query results, if any."""

    reference_time: Optional[datetime] = None
    """The date and time to use as the reference point for RelativeTime filters.

    Includes time zone information. Defaults to the current time in UTC.
    """

    take: Optional[int] = 1000
    """Limits the returned list to the specified number of results. Maximum is 1000."""

    order_by: Optional[AlarmOrderBy] = None
    """The sort order of the returned list of alarms.

    By default, alarms are sorted in ascending order based on the specified value.
    """

    order_by_descending: bool = False
    """Whether to sort descending instead of ascending.

    The elements in the list are sorted ascending by default. If true, sorts descending.
    """

    continuation_token: Optional[str] = None
    """A token which allows the user to resume a query at the next item in the matching results.

    When querying, a token will be returned if a query may be continued. To obtain the next page
    of results, pass the token to the service on a subsequent request.
    """

    return_count: bool = False
    """Whether to return the total number of alarms that match the provided filter.

    This disregards the take value.
    """
