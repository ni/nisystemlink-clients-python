from typing import List

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._alarm import Alarm


class QueryAlarmsWithFilterResponse(WithPaging):
    """Contains information about the alarms matched by a query."""

    alarms: List[Alarm]
    """The list of alarms returned by the query."""

    total_count: int | None = None
    """The total number of alarms which matched the query, if requested."""
