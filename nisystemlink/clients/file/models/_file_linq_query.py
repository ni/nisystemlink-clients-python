from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.file.models._base_file_response import BaseFileResponse
from nisystemlink.clients.file.models._file_query_order_by import FileLinqQueryOrderBy


class FileLinqQueryRequest(JsonModel):
    filter: str | None = None
    """
    The filter criteria for files. Consists of a string of queries composed using AND/OR operators.
    String values and date strings need to be enclosed in double quotes. Parentheses can be used
    around filters to better define the order of operations.

    Example Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'
    """

    order_by: FileLinqQueryOrderBy | None = None
    """The property by which to order the files in the response."""

    order_by_descending: bool | None = False
    """If true, the files are ordered in descending order based on the property specified in `order_by`."""

    take: int | None = None
    """The maximum number of files to return in the response. Default value is 1000"""


class FileLinqQueryResponse(BaseFileResponse):
    """Response model for LINQ query operations."""

    pass
