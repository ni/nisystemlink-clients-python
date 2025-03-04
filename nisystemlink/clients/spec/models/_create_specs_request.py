from datetime import datetime
from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import (
    SpecificationDefinition,
    SpecificationType,
)


class CreateSpecificationsRequestObject(SpecificationDefinition):
    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    type: SpecificationType
    """Type of the specification."""


class CreateSpecificationsRequest(JsonModel):
    """Create multiple specifications."""

    specs: Optional[List[CreateSpecificationsRequestObject]] = None
    """List of specifications to be created."""


class BaseSpecificationResponse(JsonModel):
    """Base Response Model for create specs response and update specs response."""

    id: str
    """The global Id of the specification."""

    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    workspace: str
    """Id of the workspace to which the specification will be associated.

    Default workspace will be taken if the value is not given.
    """

    version: int
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """


class CreatedSpecification(BaseSpecificationResponse):
    """A specification successfully created on the server."""

    created_at: datetime
    """ISO-8601 formatted timestamp indicating when the specification was created."""

    created_by: str
    """Id of the user who created the specification."""


class CreateSpecificationsPartialSuccess(JsonModel):
    """When some specs can not be created, this contains the list that was and was not created."""

    created_specs: Optional[List[CreatedSpecification]] = None
    """Information about the created specification(s)"""

    failed_specs: Optional[List[CreateSpecificationsRequestObject]] = None
    """List of specification requests that failed during creation."""

    error: Optional[ApiError] = None
