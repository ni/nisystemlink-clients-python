from enum import Enum
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._condition import Condition


class SpecificationLimit(JsonModel):
    """A limit for a specification.

    The limit is the value that a measurement should be compared against during analysis to
    determine the health or pass/fail status of that measurement.
    """

    min: Optional[float]
    """Minimum limit of the specification.

    All measurements that map to this specification should be > this limit.
    """

    typical: Optional[float]
    """Typical value of the specification."""

    max: Optional[float]
    """Maximum value of the specification.

    All measurements that map to this specification should be < this limit.
    """


class Type(Enum):
    """The overall type of the specification."""

    PARAMETRIC = "PARAMETRIC"
    """Parametric specs have limits."""

    FUNCTIONAL = "FUNCTIONAL"
    """Functional specs only have pass/fail status."""


class SpecificationBase(JsonModel):

    product_id: str
    """Id of the product to which the specification will be associated."""

    spec_id: str
    """User provided value using which the specification will be identified.

    This should be unique for a product and workspace combination.
    """

    name: Optional[str]
    """Name of the specification."""

    category: Optional[str]
    """Category of the specification."""

    type: Type
    """Type of the specification."""

    symbol: Optional[str]
    """Short form identifier of the specification."""

    block: Optional[str]
    """Block name of the specification.

    Typically a block is one of the subsystems of the overall product being specified.
    """

    limit: Optional[SpecificationLimit]
    """The limits for this spec."""

    unit: Optional[str]
    """Unit of the specification."""

    conditions: Optional[List[Condition]]
    """Conditions associated with the specification."""

    keywords: Optional[List[str]]
    """Keywords or phrases associated with the specification."""

    properties: Optional[Dict[str, str]]
    """Additional properties associated with the specification."""

    workspace: Optional[str]
    """Id of the workspace to which the specification will be associated.

    Default workspace will be taken if the value is not given.
    """
