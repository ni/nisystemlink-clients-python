from enum import Enum


class FileQueryOrderBy(Enum):
    """Order Files Query Response by Metadata."""

    CREATED = "created"
    ID = "id"
    SIZE = "size"
    LAST_UPDATED_TIMESTAMP = "lastUpdatedTimestamp"
