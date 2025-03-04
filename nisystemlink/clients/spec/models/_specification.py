from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._condition import Condition


class SpecificationLimit(JsonModel):
    """A limit for a specification.

    The limit is the value that a measurement should be compared against during analysis to
    determine the health or pass/fail status of that measurement.
    """

    min: Optional[float] = None
    """Minimum limit of the specification.

    All measurements that map to this specification should be > this limit.
    """

    typical: Optional[float] = None
    """Typical value of the specification."""

    max: Optional[float] = None
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

    product_id: Optional[str] = None
    """Id of the product to which the specification will be associated."""

    spec_id: Optional[str] = None
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    name: Optional[str] = None
    """Name of the specification."""

    category: Optional[str] = None
    """Category of the specification."""

    type: Optional[SpecificationType] = None
    """Type of the specification."""

    symbol: Optional[str] = None
    """Short form identifier of the specification."""

    block: Optional[str] = None
    """Block name of the specification.

    Typically a block is one of the subsystems of the overall product being specified.
    """

    limit: Optional[SpecificationLimit] = None
    """The limits for this spec."""

    unit: Optional[str] = None
    """Unit of the specification."""

    conditions: Optional[List[Condition]] = None
    """Conditions associated with the specification."""

    keywords: Optional[List[str]] = None
    """Keywords or phrases associated with the specification."""

    properties: Optional[Dict[str, str]] = None
    """Additional properties associated with the specification."""

    workspace: Optional[str] = None
    """Id of the workspace to which the specification will be associated.

    Default workspace will be taken if the value is not given.
    """


class Specification(SpecificationDefinition):
    """The complete definition of a specification."""

    id: Optional[str] = None
    """The global Id of the specification."""

    created_at: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the specification was created."""

    created_by: Optional[str] = None
    """Id of the user who created the specification."""

    updated_at: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the specification was last updated."""

    updated_by: Optional[str] = None
    """Id of the user who last updated the specification."""

    version: Optional[int] = None
    """
    Current version of the specification.

    When an update is applied, the version is automatically incremented.
    """
