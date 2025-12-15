from datetime import datetime
from enum import Enum
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._condition import Condition


class SpecificationLimit(JsonModel):
    """A limit for a specification.

    The limit is the value that a measurement should be compared against during analysis to
    determine the health or pass/fail status of that measurement.
    """

    min: float | None = None
    """Minimum limit of the specification.

    All measurements that map to this specification should be > this limit.
    """

    typical: float | None = None
    """Typical value of the specification."""

    max: float | None = None
    """Maximum value of the specification.

    All measurements that map to this specification should be < this limit.
    """


class SpecificationType(Enum):
    """The overall type of the specification."""

    PARAMETRIC = "PARAMETRIC"
    """Parametric specs have limits."""

    FUNCTIONAL = "FUNCTIONAL"
    """Functional specs only have pass/fail status."""


class SpecificationDefinition(JsonModel):

    product_id: str | None = None
    """Id of the product to which the specification will be associated."""

    spec_id: str | None = None
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    name: str | None = None
    """Name of the specification."""

    category: str | None = None
    """Category of the specification."""

    type: SpecificationType | None = None
    """Type of the specification."""

    symbol: str | None = None
    """Short form identifier of the specification."""

    block: str | None = None
    """Block name of the specification.

    Typically a block is one of the subsystems of the overall product being specified.
    """

    limit: SpecificationLimit | None = None
    """The limits for this spec."""

    unit: str | None = None
    """Unit of the specification."""

    conditions: List[Condition] | None = None
    """Conditions associated with the specification."""

    keywords: List[str] | None = None
    """Keywords or phrases associated with the specification."""

    properties: Dict[str, str] | None = None
    """Additional properties associated with the specification."""

    workspace: str | None = None
    """Id of the workspace to which the specification will be associated.

    Default workspace will be taken if the value is not given.
    """


class Specification(SpecificationDefinition):
    """The complete definition of a specification."""

    id: str | None = None
    """The global Id of the specification."""

    created_at: datetime | None = None
    """ISO-8601 formatted timestamp indicating when the specification was created."""

    created_by: str | None = None
    """Id of the user who created the specification."""

    updated_at: datetime | None = None
    """ISO-8601 formatted timestamp indicating when the specification was last updated."""

    updated_by: str | None = None
    """Id of the user who last updated the specification."""

    version: int | None = None
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """
