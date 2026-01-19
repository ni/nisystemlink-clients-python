from enum import Enum
from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._file_metadata import LinqQueryFileMetadata


class TotalCountRelation(str, Enum):
    """Describes the relation the returned total count value has with respect to the total number of files."""

    EQUALS = "eq"
    """Equals, meaning that the returned items are all the items that matched the filter."""

    GREATER_THAN_OR_EQUAL = "gte"
    """Greater or equal, meaning that the take limit has been hit, but there are further items that match the query."""


class TotalCount(JsonModel):
    """The total number of files that match the query regardless of skip and take values"""

    relation: TotalCountRelation
    """
    Describes the relation the returned total count value has with respect to the total number of
    files matched by the query.
    """

    value: int
    """Describes the number of files that were returned as a result of the query in the database"""


class BaseFileResponse(JsonModel):
    """Base class for file response models containing a list of files and total count."""

    available_files: List[LinqQueryFileMetadata]
    """The list of files returned by the query"""

    total_count: TotalCount
    """The total number of files that match the query regardless of skip and take values"""
