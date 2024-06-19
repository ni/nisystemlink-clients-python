from enum import Enum
from typing import List, Optional, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ConditionType(Enum):
    """Conditions are either numeric or string type."""

    NUMERIC = "NUMERIC"
    """Numeric condition."""

    STRING = "STRING"
    """String condition."""


class ConditionRange(JsonModel):
    """Specifies the range of values that the condition must cover."""

    min: Optional[float] = None
    """Minimum value of the condition range."""

    max: Optional[float] = None
    """Maximum value of the condition range."""

    step: Optional[float] = None
    """Step value of the condition range."""


class ConditionValueBase(JsonModel):
    """The base type for conditions that can be represented in several styles."""

    condition_type: ConditionType
    """Type of the Condition."""


class NumericConditionValue(ConditionValueBase):
    """A numeric condition.

    Numeric conditions can contain a combination of ranges and discrete lists.
    """

    range: Optional[List[ConditionRange]] = None
    """List of condition range values."""

    discrete: Optional[List[float]] = None
    """List of condition discrete values."""

    unit: Optional[str] = None
    """Unit of the condition."""


class StringConditionValue(ConditionValueBase):
    """A string condition.

    String conditions may only contain discrete lists of values.
    """

    discrete: Optional[List[str]] = None
    """List of condition discrete values."""


class Condition(JsonModel):
    """A single condition."""

    name: Optional[str] = None
    """Name of the condition."""

    value: Optional[Union[NumericConditionValue, StringConditionValue]] = None
    """Value of the condition."""
