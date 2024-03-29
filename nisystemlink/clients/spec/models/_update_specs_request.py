from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import (
    Specification,
    SpecificationUpdated,
)


class UpdateSpecificationsRequest(JsonModel):

    specs: Optional[List[Specification]] = None
    """List of specifications to be updated."""


class UpdateSpecificationResponseObject(SpecificationUpdated):

    id: Optional[str] = None
    """The global Id of the specification."""

    version: Optional[int] = None
    """The new version of the specification after the update has been applied."""

    product_id: Optional[str] = None
    """Id of the product to which the specification is associated."""

    spec_id: Optional[str] = None
    """User provided identifier for the specification.

    This will be unique for a product and workspace combination.
    """

    workspace: Optional[str] = None
    """Id of the workspace to which the specification is associated."""


class UpdateSpecificationsPartialSuccessResponse(JsonModel):

    updated_specs: Optional[List[UpdateSpecificationResponseObject]] = None
    """Information about each of the updated specification(s)."""

    failed_specs: Optional[List[Specification]] = None
    """Information about each of the specification request(s) that failed during the update."""

    error: Optional[ApiError] = None
    """Any errors that occurred."""
