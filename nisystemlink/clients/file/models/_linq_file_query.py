from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.file.models._file_query_order_by import QueryFilesLinqOrderBy


class LinqFileQueryRequest(JsonModel):
    filter: Optional[str] = None
    """
    The filter criteria for files. Consists of a string of queries composed using AND/OR operators. 
    String values and date strings need to be enclosed in double quotes. Parentheses can be used around filters to better define the order of operations.

    Example Filter syntax: '[property name][operator][operand] and [property name][operator][operand]'
    """

    ordery_by: Optional[QueryFilesLinqOrderBy] = None
    """The property by which to order the files in the response."""

    order_by_descending: Optional[bool] = False
    """If true, the files are ordered in descending order based on the property specified in `ordery_by`."""

    take: Optional[int] = None
    """The maximum number of files to return in the response. Default value is 1000"""


class LinqFileMetadata(JsonModel):
    created: Optional[datetime] = None
    """
    The date and time the file was created in the file service.

    example :2018-05-15T18:54:27.519Z
    """

    updated: Optional[datetime] = None
    """
    The date and time the file was last updated in the file service.

    example :2018-05-15T18:54:27.519Z
    """

    id: Optional[str] = None
    """
    The file's ID within the service group.

    example: "5afb2ce3741fe11d88838cc9"
    """

    properties: Optional[Dict[str, str]] = None
    """
    The file's properties
    Example - {"Name": "myfile.txt", "MyProperty": "Value"}
    """

    service_group: Optional[str] = None
    """
    The service group that owns the file
    """

    size: Optional[int] = None
    """
    The 32-bit file size in bytes. If the value is larger than a 32-bit integer,
    this value is -1 and the size64 parameter contains the correct value.
    """

    size64: Optional[int] = None
    """
    The 64-bit file size in bytes
    """

    workspace: Optional[str] = None
    """
    The workspace the file belongs to
    """


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

class LinqQueryResponse(JsonModel):
    available_files: List[LinqFileMetadata]
    """The list of files returned by the query"""

    total_count: TotalCount
    """The total number of files that match the query regardless of skip and take values"""
