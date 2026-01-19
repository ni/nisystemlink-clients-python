# -*- coding: utf-8 -*-
from typing import Any, Callable, Generator

from nisystemlink.clients.core._uplink._with_paging import WithPaging


def paginate(
    fetch_function: Callable[..., WithPaging],
    items_field: str,
    **fetch_kwargs: Any,
) -> Generator[Any, None, None]:
    """Generate items from paginated API responses using continuation tokens.

    This helper function provides a convenient way to iterate over all items
    from a paginated API endpoint that uses continuation tokens. It automatically
    handles fetching subsequent pages until all items are retrieved.

    Args:
        fetch_function: The API function to call to fetch each page of items.
            Must accept a ``continuation_token`` parameter and return a response
            that derives from ``WithPaging``.
        items_field: The name of the field in the response object that contains
            the list of items to yield.
        **fetch_kwargs: Additional keyword arguments to pass to the fetch function
            on every call (e.g., filters, take limits, etc.).

    Yields:
        Individual items from each page of results.

    Note:
        The fetch function will be called with the `continuation_token` parameter
        set to `None` on the first call, then with each subsequent token until
        the response contains a `None` continuation token.
    """
    continuation_token = None

    while True:
        # Set the continuation token parameter for this page
        fetch_kwargs["continuation_token"] = continuation_token

        # Fetch the current page
        response = fetch_function(**fetch_kwargs)

        # Get the items from the response using the specified field name
        items = getattr(response, items_field, [])

        # Yield each item individually
        for item in items:
            yield item

        # Get the continuation token for the next page
        next_continuation_token = response.continuation_token

        # Stop if there are no more pages
        if next_continuation_token is None:
            break

        # Guard against infinite loop if continuation token doesn't change
        if next_continuation_token == continuation_token:
            raise RuntimeError("Continuation token did not change between iterations.")

        continuation_token = next_continuation_token
