from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import SpecificationBase


class CreateSpecificationsRequest(JsonModel):
    """Create multiple specifications."""

    specs: Optional[List[SpecificationBase]] = None
    """List of specifications to be created."""


class CreateSpecificationResponseObject(JsonModel):
    """Response to specification creation requests."""

    id: Optional[str] = None
    """The global ID of the specification."""

    product_id: Optional[str] = None
    """Id of the product to which the specification is associated."""

    spec_id: Optional[str] = None
    """User provided value using which the specification is identified.

    This is unique for a product and workspace combination. This is not the same as `id` which is
    the globally unique identifier for a specification.
    """

    workspace: Optional[str] = None
    """Id of the workspace to which the specification is associated."""

    created_at: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the specification was created."""

    created_by: Optional[str] = None
    """Id of the user who created the specification."""

    version: Optional[int] = None
    """Version of the specification. The initial version starts with 0."""


class CreateSpecificationsPartialSuccessResponse(JsonModel):
    """When some specs can not be created, this contains the list that was and was not created."""

    created_specs: Optional[List[CreateSpecificationResponseObject]] = None
    """Information about the created specification(s)"""

    failed_specs: Optional[List[SpecificationBase]] = None
    """List of specification requests that failed during creation."""

    error: Optional[ApiError] = None
