import pytest
from nisystemlink.clients.core import ApiError, ApiException
from nisystemlink.clients.core.helpers._partial_success import (
    unwrap_single_item_partial_success,
)


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def model_dump(self, *, mode, by_alias):
        assert mode == "json"
        assert by_alias is True
        return self._payload


def test__unwrap_single_item_partial_success__returns_first_item():
    """Return the first item when the partial-success response is successful."""
    response = _FakeResponse({"items": ["created-item"]})

    created_item = unwrap_single_item_partial_success(
        response=response,
        items=["created-item"],
        failed=None,
        error=None,
        failure_message="Failed to create item.",
        empty_message="Server returned no created items.",
    )

    assert created_item == "created-item"


def test__unwrap_single_item_partial_success__raises_on_partial_failure():
    """Raise ApiException when the response reports a structured partial failure."""
    response = _FakeResponse(
        {
            "items": [],
            "failed": [{"id": "request-id"}],
            "error": {"message": "Create failed"},
        }
    )
    error = ApiError(message="Create failed")

    with pytest.raises(ApiException) as exc_info:
        unwrap_single_item_partial_success(
            response=response,
            items=[],
            failed=[{"id": "request-id"}],
            error=error,
            failure_message="Failed to create item.",
            empty_message="Server returned no created items.",
        )

    assert exc_info.value.error == error
    assert exc_info.value.response_data == response.model_dump(
        mode="json", by_alias=True
    )


def test__unwrap_single_item_partial_success__raises_on_empty_success_payload():
    """Raise ApiException when the response succeeds but contains no created item."""
    response = _FakeResponse({"items": []})

    with pytest.raises(
        ApiException, match="Server returned no created items"
    ) as exc_info:
        unwrap_single_item_partial_success(
            response=response,
            items=[],
            failed=None,
            error=None,
            failure_message="Failed to create item.",
            empty_message="Server returned no created items.",
        )

    assert exc_info.value.response_data == response.model_dump(
        mode="json", by_alias=True
    )


def test__unwrap_single_item_partial_success__raises_on_multiple_success_items():
    """Raise ApiException when the response unexpectedly contains multiple items."""
    response = _FakeResponse({"items": ["created-item", "extra-item"]})

    with pytest.raises(
        ApiException, match="Expected exactly one successful item but received 2"
    ) as exc_info:
        unwrap_single_item_partial_success(
            response=response,
            items=["created-item", "extra-item"],
            failed=None,
            error=None,
            failure_message="Failed to create item.",
            empty_message="Server returned no created items.",
        )

    assert exc_info.value.response_data == response.model_dump(
        mode="json", by_alias=True
    )
