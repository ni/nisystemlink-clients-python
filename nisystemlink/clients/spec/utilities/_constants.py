from dataclasses import dataclass
from typing import List, Optional

from nisystemlink.clients.spec.models._condition import ConditionRange


class DataFrameHeaders:
    CONDITION_COLUMN_HEADER_PREFIX = "condition_"

    PROPERTY_COLUMN_HEADER_PREFIX = "properties."

    KEYWORDS_COLUMN_HEADER = "keywords"


@dataclass
class TempNumericCondition:
    """A temp numeric condition to store condition type as string."""

    condition_type: str
    range: Optional[List[ConditionRange]] = None
    discrete: Optional[List[float]] = None
    unit: Optional[str] = None


@dataclass
class TempStringCondition:
    """A temp string condition to store condition type as string."""

    condition_type: str
    discrete: Optional[List[str]] = None
