from enum import Enum
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.core._uplink._with_paging import WithPaging


class StepOrderBy(str, Enum):
    """The valid ways to order steps query response.

    This contains only limited fields available in a Step.
    """

    NAME = "NAME"
    STEP_TYPE = "STEP_TYPE"
    STEP_ID = "STEP_ID"
    PARENT_ID = "PARENT_ID"
    RESULT_ID = "RESULT_ID"
    PATH = "PATH"
    TOTAL_TIME_IN_SECONDS = "TOTAL_TIME_IN_SECONDS"
    STARTED_AT = "STARTED_AT"
    UPDATED_AT = "UPDATED_AT"
    DATA_MODEL = "DATA_MODEL"


class StepField(str, Enum):
    """The valid field values that can be queried.

    This contains only limited fields available in a Step.
    """

    NAME = "NAME"
    STEP_TYPE = "STEP_TYPE"
    STEP_ID = "STEP_ID"
    PARENT_ID = "PARENT_ID"
    RESULT_ID = "RESULT_ID"
    PATH = "PATH"
    TOTAL_TIME_IN_SECONDS = "TOTAL_TIME_IN_SECONDS"
    STARTED_AT = "STARTED_AT"
    UPDATED_AT = "UPDATED_AT"
    DATA_MODEL = "DATA_MODEL"


class StepProjection(str, Enum):
    """An enumeration of all fields in a Step.

    This enumeration is used to specify the fields to project in a step query.
    """

    NAME = "NAME"
    STEP_TYPE = "STEP_TYPE"
    STEP_ID = "STEP_ID"
    PARENT_ID = "PARENT_ID"
    RESULT_ID = "RESULT_ID"
    PATH = "PATH"
    PATH_IDS = "PATH_IDS"
    STATUS = "STATUS"
    TOTAL_TIME_IN_SECONDS = "TOTAL_TIME_IN_SECONDS"
    STARTED_AT = "STARTED_AT"
    UPDATED_AT = "UPDATED_AT"
    INPUTS = "INPUTS"
    OUTPUTS = "OUTPUTS"
    DATA_MODEL = "DATA_MODEL"
    DATA = "DATA"
    HAS_CHILDREN = "HAS_CHILDREN"
    WORKSPACE = "WORKSPACE"
    KEYWORDS = "KEYWORDS"
    PROPERTIES = "PROPERTIES"


class QueryStepsBase(JsonModel):
    filter: Optional[str] = None
    """The step query filter in Dynamic Linq format."""

    substitutions: Optional[List[str]] = None
    """String substitutions into the `filter`.

    Makes substitutions in the query filter expression. Substitutions for the query expression are
    indicated by non-negative integers that are prefixed with the "at" symbol. Each substitution in
    the given expression will be replaced by the element at the corresponding index (zero-based) in
    this list. For example, "@0" in the filter expression will be replaced with the element at the
    zeroth index of the substitutions list.
    """


class QueryStepsRequest(QueryStepsBase, WithPaging):
    order_by: Optional[StepOrderBy] = None
    """Specifies the fields to use to sort the steps."""

    descending: Optional[bool] = None
    """Specifies whether to return the steps in descending order."""

    take: Optional[int] = None
    """Maximum number of steps to return in the current API response."""

    return_count: Optional[bool] = None
    """If true, the response will include a count of all steps matching the filter.

    By default, this value is `False` and count is not returned. Note that returning the count may
    incur performance penalties as the service may have to do a complete walk of the database to
    compute count.
    """

    result_filter: Optional[str] = None
    """The result query filter in Dynamic Linq format."""

    result_substitutions: Optional[List[str]] = None
    """String substitutions into the `result_filter`."""

    projection: Optional[List[StepProjection]] = None
    """Specifies the step fields to project. When a field value is given here,
    the corresponding field will be present in all returned steps, and all
    unspecified fields will be excluded. If no projection is specified,
    all step fields will be returned.
    """


class QueryStepValuesRequest(QueryStepsBase):
    field: StepField
    """The step field to return for this query."""

    starts_with: Optional[str] = None
    """Only return string parameters prefixed by this value (case sensitive)."""
