from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import (
    Specification,
    SpecificationServerManaged,
    SpecificationUpdated,
    SpecificationUserManaged,
)


class UpdateSpecificationsRequest(JsonModel):

    specs: Optional[List[Specification]] = None
    """List of specifications to be updated."""


class UpdatedSpecification(
    SpecificationUserManaged,
    SpecificationServerManaged,
    SpecificationUpdated,
):
    """A specification that was updated on the server."""


class UpdateSpecificationsPartialSuccess(JsonModel):

    updated_specs: Optional[List[UpdatedSpecification]] = None
    """Information about each of the updated specification(s)."""

    failed_specs: Optional[List[Specification]] = None
    """Information about each of the specification request(s) that failed during the update."""

    error: Optional[ApiError] = None
    """Any errors that occurred."""
