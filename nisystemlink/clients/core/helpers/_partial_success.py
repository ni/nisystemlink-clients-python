from typing import Any, Sequence, TypeVar

from nisystemlink.clients import core

_ItemT = TypeVar("_ItemT")


def unwrap_single_item_partial_success(
    *,
    response: Any | None,
    items: Sequence[_ItemT] | None,
    failed: Sequence[Any] | None,
    error: core.ApiError | None,
    failure_message: str,
    empty_message: str,
) -> _ItemT:
    """Return the first successful item from a partial-success response.

    Raises:
        ApiException: if the response reports a failure or contains no successful item.
    """
    response_data = (
        response.model_dump(mode="json", by_alias=True)
        if response is not None
        else None
    )

    if failed or error:
        raise core.ApiException(
            failure_message,
            error=error,
            response_data=response_data,
        )

    if not items:
        raise core.ApiException(
            empty_message,
            response_data=response_data,
        )

    return items[0]
