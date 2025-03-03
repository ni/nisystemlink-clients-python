from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.spec.models._specification import (
    Specification,
    SpecificationServerManaged,
    SpecificationType,
    SpecificationUpdated,
    SpecificationUserManaged,
)


class UpdateSpecificationsRequestObject(Specification):
    id: str
    """The global Id of the specification."""

    version: int
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """

    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    type: SpecificationType
    """Type of the specification."""


class UpdateSpecificationsRequest(JsonModel):

    specs: Optional[List[UpdateSpecificationsRequestObject]] = None
    """List of specifications to be updated."""


class UpdatedSpecification(
    SpecificationUserManaged,
    SpecificationServerManaged,
    SpecificationUpdated,
):
    """A specification that was updated on the server."""

    id: str
    """The global Id of the specification."""

    version: int
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """

    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """


class UpdateSpecificationsPartialSuccess(JsonModel):

    updated_specs: Optional[List[UpdatedSpecification]] = None
    """Information about each of the updated specification(s)."""

    failed_specs: Optional[List[UpdateSpecificationsRequestObject]] = None
    """Information about each of the specification request(s) that failed during the update."""

    error: Optional[ApiError] = None
    """Any errors that occurred."""
