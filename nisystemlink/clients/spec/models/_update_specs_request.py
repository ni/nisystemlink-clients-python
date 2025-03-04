from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._create_specs_request import (
    BaseSpecificationResponse,
)
from nisystemlink.clients.spec.models._specification import (
    SpecificationDefinition,
    SpecificationType,
)


class UpdateSpecificationsRequestObject(SpecificationDefinition):
    id: str
    """The global Id of the specification."""

    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    type: SpecificationType
    """Type of the specification."""

    workspace: str
    """Id of the workspace to which the specification will be associated.

    Default workspace will be taken if the value is not given.
    """

    version: int
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """


class UpdateSpecificationsRequest(JsonModel):

    specs: Optional[List[UpdateSpecificationsRequestObject]] = None
    """List of specifications to be updated."""


class UpdatedSpecification(BaseSpecificationResponse):
    """A specification that was updated on the server."""

    updated_at: datetime
    """ISO-8601 formatted timestamp indicating when the specification was last updated."""

    updated_by: str
    """Id of the user who last updated the specification."""


class UpdateSpecificationsPartialSuccess(JsonModel):

    updated_specs: Optional[List[UpdatedSpecification]] = None
    """Information about each of the updated specification(s)."""

    failed_specs: Optional[List[UpdateSpecificationsRequestObject]] = None
    """Information about each of the specification request(s) that failed during the update."""

    error: Optional[ApiError] = None
    """Any errors that occurred."""
