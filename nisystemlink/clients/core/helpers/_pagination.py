# -*- coding: utf-8 -*-
from typing import Any, Callable, Generator, TypeVar

ItemType = TypeVar("ItemType")


def paginate(
    fetch_function: Callable[..., Any],
    items_field: str = "items",
    continuation_token_field: str = "continuation_token",
    **fetch_kwargs: Any,
) -> Generator[ItemType, None, None]:
    """Generate items from paginated API responses using continuation tokens.

    This helper function provides a convenient way to iterate over all items
    from a paginated API endpoint that uses continuation tokens. It automatically
    handles fetching subsequent pages until all results are retrieved.

    Args:
        fetch_function: The API function to call to fetch each page of results.
            Must accept a ``continuation_token`` parameter (or a parameter name
            matching ``continuation_token_field``).
        items_field: The name of the field in the response object that contains
            the list of items to yield. Defaults to "items".
        continuation_token_field: The name of the field in the response object
            that contains the continuation token. Defaults to "continuation_token".
        **fetch_kwargs: Additional keyword arguments to pass to the fetch function
            on every call (e.g., filters, take limits, etc.).

    Yields:
        Individual items from each page of results.

    Note:
        The fetch function will be called with the continuation_token parameter
        set to None on the first call, then with each subsequent token until
        the response contains a None continuation token.
    """
    continuation_token = None

    while True:
        # Set the continuation token parameter for this page
        fetch_kwargs[continuation_token_field] = continuation_token

        # Fetch the current page
        response = fetch_function(**fetch_kwargs)

        # Get the items from the response using the specified field name
        items = getattr(response, items_field, [])

        # Yield each item individually
        for item in items:
            yield item

        # Get the continuation token for the next page
        continuation_token = getattr(response, continuation_token_field, None)

        # Stop if there are no more pages
        if continuation_token is None:
            break
