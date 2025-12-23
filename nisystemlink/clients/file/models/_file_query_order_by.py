from enum import Enum


class FileQueryOrderBy(Enum):
    """Order Files Query Response by Metadata for GET /files endpoint."""

    CREATED = "created"
    ID = "id"
    SIZE = "size"
    LAST_UPDATED_TIMESTAMP = "lastUpdatedTimestamp"


class FileLinqQueryOrderBy(str, Enum):
    """Order Files LINQ Query by Metadata for POST /query-files-linq endpoint."""

    NAME = "name"
    CREATED = "created"
    UPDATED = "updated"
    EXTENSION = "extension"
    SIZE = "size"
    WORKSPACE = "workspace"


class SearchFilesOrderBy(str, Enum):
    """Order Files Search by Metadata for POST /search-files endpoint."""

    NAME = "name"
    CREATED = "created"
    UPDATED = "updated"
    EXTENSION = "extension"
    SIZE = "size"
    WORKSPACE = "workspace"
