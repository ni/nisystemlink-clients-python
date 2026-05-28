"""Tests for TestMonitorClient convenience methods."""

import pytest
from nisystemlink.clients.core import ApiError, ApiException
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateResultRequest,
    CreateResultsPartialSuccess,
    Result,
    Status,
)


class TestTestMonitorClient:
    """Test cases for TestMonitorClient convenience methods."""

    def test__create_result__returns_created_result(self):
        """Test that create_result returns the created result on success."""
        request = CreateResultRequest(
            part_number="Part Number",
            program_name="Program Name",
            status=Status.PASSED(),
        )
        created_result = Result(
            id="result-id",
            part_number=request.part_number,
            program_name=request.program_name,
            status=request.status,
        )
        captured_results = []
        client = object.__new__(TestMonitorClient)

        def fake_create_results(results):
            captured_results.append(results)
            return CreateResultsPartialSuccess(results=[created_result])

        client.create_results = fake_create_results  # type: ignore[method-assign]

        response = client.create_result(request)

        assert response == created_result
        assert captured_results == [[request]]

    def test__create_result__raises_api_exception_on_partial_failure(self):
        """Test that create_result raises with the structured error on failure."""
        request = CreateResultRequest(
            part_number="Part Number",
            program_name="Program Name",
            status=Status.PASSED(),
        )
        error = ApiError(message="Create failed")
        client = object.__new__(TestMonitorClient)

        def fake_create_results(results):
            return CreateResultsPartialSuccess(
                results=[],
                failed=results,
                error=error,
            )

        client.create_results = fake_create_results  # type: ignore[method-assign]

        with pytest.raises(ApiException) as exc_info:
            client.create_result(request)

        assert exc_info.value.error == error
        assert exc_info.value.response_data == {
            "results": [],
            "failed": [request.model_dump(mode="json", by_alias=True)],
            "error": error.model_dump(mode="json", by_alias=True),
        }

    def test__create_result__raises_on_missing_created_result(self):
        """Test that create_result rejects an unexpected empty success payload."""
        request = CreateResultRequest(
            part_number="Part Number",
            program_name="Program Name",
            status=Status.PASSED(),
        )
        client = object.__new__(TestMonitorClient)

        def fake_create_results(_results):
            return CreateResultsPartialSuccess(results=[])

        client.create_results = fake_create_results  # type: ignore[method-assign]

        with pytest.raises(ApiException, match="Server returned no created results"):
            client.create_result(request)
