from enum import Enum
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import StrictFloat, StrictInt, StrictStr


class ConditionType(Enum):
    """Conditions are either numeric or string type."""

    NUMERIC = "NUMERIC"
    """Numeric condition."""

    STRING = "STRING"
    """String condition."""


class ConditionRange(JsonModel):
    """Specifies the range of values that the condition must cover."""

    min: float | None = None
    """Minimum value of the condition range."""

    max: float | None = None
    """Maximum value of the condition range."""

    step: float | None = None
    """Step value of the condition range."""


class ConditionValueBase(JsonModel):
    """The base type for conditions that can be represented in several styles."""

    condition_type: ConditionType | None = None
    """Type of the Condition."""


class NumericConditionValue(ConditionValueBase):
    """A numeric condition.

    Numeric conditions can contain a combination of ranges and discrete lists.
    """

    range: List[ConditionRange] | None = None
    """List of condition range values."""

    # StrictFloat and StrictInt are used here because discrete is a common property for
    # NumericConditionValue and StringConditionValue.
    # If float/int is used, pydantic converts string of number into float/int by default
    # when deserializing a StringCondition JSON and misinterprets it as NumericConditionValue type.
    discrete: List[StrictFloat | StrictInt | None] | None = None
    """List of condition discrete values."""

    unit: str | None = None
    """Unit of the condition."""


class StringConditionValue(ConditionValueBase):
    """A string condition.

    String conditions may only contain discrete lists of values.
    """

    # StrictStr is used here because discrete is a common property for
    # NumericConditionValue and StringConditionValue.
    # If str is used, pydantic converts any datatype into string by default when deserializing a
    # NumericCondition JSON and misinterprets it as StringConditionValue type.
    discrete: List[StrictStr] | None = None
    """List of condition discrete values."""


class Condition(JsonModel):
    """A single condition."""

    name: str | None = None
    """Name of the condition."""

    # Ideal approach is to set the dtype here as ConditionValue and use pydantic discriminator to
    # deserialize/serialize the JSON into correct ConditionValue sub types. But Union of dtypes is
    # used here as the discriminator field could be none when projection is used in query API.
    value: NumericConditionValue | StringConditionValue | None = None
    """Value of the condition."""
