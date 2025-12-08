from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._alarm import Alarm


class QueryWithFilterResponse(JsonModel):
    """Contains information about the alarms matched by a query."""

    alarms: List[Alarm]
    """The list of alarms returned by the query."""

    total_count: Optional[int] = None
    """The total number of alarms which matched the query, if requested."""

    continuation_token: Optional[str] = None
    """A token which allows the user to resume a query at the next item in the matching results.

    When querying, a token will be returned if a query may be continued. To obtain the next page
    of results, pass the token to the service on a subsequent request.
    """
