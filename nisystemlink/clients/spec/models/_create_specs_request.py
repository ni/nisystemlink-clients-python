from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import (
    SpecificationCreation,
    SpecificationDefinition,
    SpecificationServerManaged,
    SpecificationUserManaged,
)


class CreateSpecificationsRequest(JsonModel):
    """Create multiple specifications."""

    specs: Optional[List[SpecificationDefinition]] = None
    """List of specifications to be created."""


class CreatedSpecification(
    SpecificationServerManaged, SpecificationUserManaged, SpecificationCreation
):
    """A specification successfully created on the server."""


class CreateSpecificationsPartialSuccess(JsonModel):
    """When some specs can not be created, this contains the list that was and was not created."""

    created_specs: Optional[List[CreatedSpecification]] = None
    """Information about the created specification(s)"""

    failed_specs: Optional[List[SpecificationDefinition]] = None
    """List of specification requests that failed during creation."""

    error: Optional[ApiError] = None
