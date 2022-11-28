from typing import Optional

from ._json_model import JsonModel


class WithPaging(JsonModel):
    continuation_token: Optional[str] = None
    """A token which allows the user to resume a query at the next item in the matching results.

    When querying, a token will be returned if a query may be
    continued. To obtain the next page of results, pass the token to the service
    on a subsequent request. The service will respond with a new continuation
    token. To paginate results, continue sending requests with the newest
    continuation token provided by the service, until this value is null.
    """
