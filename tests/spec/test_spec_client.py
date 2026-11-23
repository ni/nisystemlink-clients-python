"""Unit tests for client-side behavior of SpecClient.

Server-side behavior (validation, storage, projections) is covered by the integration tests.
"""

import json

import pytest
import responses
from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    CreateSpecificationsRequest,
    CreateSpecificationsRequestObject,
    MeasurementMappingItem,
    QuerySpecificationsRequest,
    SpecificationType,
    UpdateSpecificationsRequest,
    UpdateSpecificationsRequestObject,
)

BASE_URL = "https://example.com"

MAPPING = [MeasurementMappingItem(filter="F1", result_filter="R1")]
MAPPING_JSON = [{"filter": "F1", "resultFilter": "R1"}]

SPEC_JSON = {
    "id": "1",
    "productId": "P1",
    "specId": "S1",
    "workspace": "w",
    "version": 0,
    "type": "PARAMETRIC",
}


def _client() -> SpecClient:
    return SpecClient(HttpConfiguration(server_uri=BASE_URL))


def _create_request(**fields) -> CreateSpecificationsRequest:
    return CreateSpecificationsRequest(
        specs=[
            CreateSpecificationsRequestObject(
                product_id="P1",
                spec_id="S1",
                type=SpecificationType.PARAMETRIC,
                **fields,
            )
        ]
    )


def _update_request(**fields) -> UpdateSpecificationsRequest:
    return UpdateSpecificationsRequest(
        specs=[
            UpdateSpecificationsRequestObject(
                id="1",
                product_id="P1",
                spec_id="S1",
                workspace="w",
                version=0,
                type=SpecificationType.PARAMETRIC,
                **fields,
            )
        ]
    )


def _sent_spec() -> dict:
    call = responses.calls[0]
    assert isinstance(call, responses.Call)
    return json.loads(call.request.body)["specs"][0]


class TestSpecClientRequestPayload:
    @pytest.mark.parametrize(
        "fields, expected",
        [
            ({}, None),
            ({"measurement_mapping": MAPPING}, MAPPING_JSON),
        ],
        ids=["not_set", "items"],
    )
    @responses.activate
    def test__create_specs_measurement_mapping__payload_reflects_what_was_set(
        self, fields, expected
    ):
        responses.post(f"{BASE_URL}/nispec/v1/specs", json={}, status=200)

        _client().create_specs(_create_request(**fields))

        spec = _sent_spec()
        if expected is None:
            assert "measurementMapping" not in spec
        else:
            assert spec["measurementMapping"] == expected

    @pytest.mark.parametrize(
        "fields, expected",
        [
            ({}, None),
            ({"measurement_mapping": None}, "null"),
            ({"measurement_mapping": []}, []),
            ({"measurement_mapping": MAPPING}, MAPPING_JSON),
        ],
        ids=["not_set", "explicit_none", "empty_list", "items"],
    )
    @responses.activate
    def test__update_specs_measurement_mapping__payload_reflects_what_was_set(
        self, fields, expected
    ):
        responses.post(f"{BASE_URL}/nispec/v1/update-specs", json={}, status=200)

        _client().update_specs(_update_request(**fields))

        spec = _sent_spec()
        if expected is None:
            assert "measurementMapping" not in spec
        elif expected == "null":
            assert "measurementMapping" in spec
            assert spec["measurementMapping"] is None
        else:
            assert spec["measurementMapping"] == expected


class TestSpecClientResponseParsing:
    @responses.activate
    def test__get_spec_without_measurement_mapping__returns_none(self):
        responses.get(f"{BASE_URL}/nispec/v1/specs/1", json=SPEC_JSON, status=200)

        assert _client().get_spec("1").measurement_mapping is None

    @responses.activate
    def test__query_specs_without_measurement_mapping__returns_none(self):
        responses.post(
            f"{BASE_URL}/nispec/v1/query-specs",
            json={"specs": [SPEC_JSON]},
            status=200,
        )

        response = _client().query_specs(QuerySpecificationsRequest(product_ids=["P1"]))

        assert response.specs is not None
        assert response.specs[0].measurement_mapping is None

    @pytest.mark.parametrize("operation", ["create", "update"])
    @responses.activate
    def test__failed_specs_response__error_name_and_message_preserved(self, operation):
        error = {
            "name": "MeasurementMappingCountExceeded",
            "message": "Some server message.",
            "innerErrors": [],
        }
        failed_spec = {**SPEC_JSON, "measurementMapping": MAPPING_JSON}
        if operation == "create":
            responses.post(
                f"{BASE_URL}/nispec/v1/specs",
                json={"failedSpecs": [failed_spec], "error": error},
                status=200,
            )
            response = _client().create_specs(_create_request())
        else:
            responses.post(
                f"{BASE_URL}/nispec/v1/update-specs",
                json={"failedSpecs": [failed_spec], "error": error},
                status=200,
            )
            response = _client().update_specs(_update_request())

        assert response.failed_specs is not None
        assert [s.spec_id for s in response.failed_specs] == ["S1"]
        assert response.error is not None
        assert response.error.name == error["name"]
        assert response.error.message == error["message"]
