from enum import Enum


class FileQueryOrderBy(Enum):
    """Order Files Query Response by Metadata for GET /files endpoint."""

    CREATED = "created"
    ID = "id"
    SIZE = "size"
    LAST_UPDATED_TIMESTAMP = "lastUpdatedTimestamp"


class FileLinqQueryOrderBy(Enum):
    """Order Files LINQ Query by Metadata for POST /query-files-linq endpoint."""

    CREATED = "created"
    UPDATED = "updated"
    EXTENSION = "extension"
    SIZE = "size"
    WORKSPACE = "workspace"
