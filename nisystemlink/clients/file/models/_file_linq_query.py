from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.file.models._file_metadata import LinqQueryFileMetadata
from nisystemlink.clients.file.models._file_query_order_by import FileLinqQueryOrderBy


class FileLinqQueryRequest(JsonModel):
    filter: Optional[str] = None
    """
    The filter criteria for files. Consists of a string of queries composed using AND/OR operators.
    String values and date strings need to be enclosed in double quotes. Parentheses can be used
    around filters to better define the order of operations.

    Example Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'
    """

    order_by: Optional[FileLinqQueryOrderBy] = None
    """The property by which to order the files in the response."""

    order_by_descending: Optional[bool] = False
    """If true, the files are ordered in descending order based on the property specified in `order_by`."""

    take: Optional[int] = None
    """The maximum number of files to return in the response. Default value is 1000"""


class TotalCount(JsonModel):
    """The total number of files that match the query regardless of skip and take values"""

    relation: str
    """
    Describes the relation the returned total count value has with respect to the total number of
    files matched by the query.

    Possible values:

    - "eq" -> equals, meaning that the returned items are all the items that matched the filter.

    - "gte" -> greater or equal, meaning that there the take limit has been hit, but there are further
    items that match the query in the database.
    """

    value: int
    """Describes the number of files that were returned as a result of the query in the database"""


class FileLinqQueryResponse(JsonModel):
    available_files: List[LinqQueryFileMetadata]
    """The list of files returned by the query"""

    total_count: TotalCount
    """The total number of files that match the query regardless of skip and take values"""
