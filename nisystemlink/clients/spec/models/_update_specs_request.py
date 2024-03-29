from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import SpecificationBase


class UpdateSpecificationRequestObject(SpecificationBase):
    id: str
    """The global Id of the specification to be updated."""

    version: int
    """
    Current version of the specification to be updated.

    When an update is applied, the version is automatically incremented.
    """


class UpdateSpecificationsRequest(JsonModel):

    specs: Optional[List[UpdateSpecificationRequestObject]] = None
    """List of specifications to be updated."""


class UpdateSpecificationResponseObject(JsonModel):

    id: Optional[str] = None
    """The global Id of the specification."""

    product_id: Optional[str] = None
    """Id of the product to which the specification is associated."""

    spec_id: Optional[str] = None
    """User provided identifier for the specification.

    This will be unique for a product and workspace combination.
    """

    workspace: Optional[str] = None
    """Id of the workspace to which the specification is associated."""

    updated_at: Optional[datetime] = None
    """ISO-8601 formatted UTC timestamp of when the specification was updated."""

    updated_by: Optional[str] = None
    """Id of the user who last updated the specification."""

    version: Optional[int] = None
    """The new version of the specification after the update has been applied."""


class UpdateSpecificationsPartialSuccessResponse(JsonModel):

    updated_specs: Optional[List[UpdateSpecificationResponseObject]] = None
    """Information about each of the updated specification(s)."""

    failed_specs: Optional[List[UpdateSpecificationRequestObject]] = None
    """Information about each of the specification request(s) that failed during the update."""

    error: Optional[ApiError] = None
    """Any errors that occurred."""
