from enum import Enum


class GetFilesOrderBy(Enum):
    """Order Files Query Response by Metadata."""

    CREATED = "created"
    ID = "id"
    SIZE = "size"
    LAST_UPDATED_TIMESTAMP = "lastUpdatedTimestamp"


class QueryFilesLinqOrderBy(Enum):
    """Order Files LINQ Query by Metadata."""

    CREATED = "created"
    UPDATED = "updated"
    EXTENSION = "extension"
    SIZE = "size"
    WORKSPACE = "workspace"
