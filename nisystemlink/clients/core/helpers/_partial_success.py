from typing import Any, Sequence, TypeVar

from nisystemlink.clients import core

_ItemT = TypeVar("_ItemT")
_ONE_OR_MORE_ERRORS_OCCURRED_NAME = "Skyline.OneOrMoreErrorsOccurred"
_ONE_OR_MORE_ERRORS_OCCURRED_CODE = -251041


def _unwrap_single_inner_error(error: core.ApiError | None) -> core.ApiError | None:
    if error is None:
        return None

    if len(error.inner_errors) != 1:
        return error

    if (
        error.name == _ONE_OR_MORE_ERRORS_OCCURRED_NAME
        or error.code == _ONE_OR_MORE_ERRORS_OCCURRED_CODE
    ):
        return error.inner_errors[0]

    return error


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
            error=_unwrap_single_inner_error(error),
            response_data=response_data,
        )

    if not items:
        raise core.ApiException(
            empty_message,
            response_data=response_data,
        )

    if len(items) != 1:
        raise core.ApiException(
            f"Expected exactly one successful item but received {len(items)}.",
            response_data=response_data,
        )

    return items[0]
