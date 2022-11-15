from enum import Enum


class ColumnType(str, Enum):
    """Represents the different column types for a table column."""

    Normal = "NORMAL"
    """The column has no special properties. This is the default."""

    Index = "INDEX"
    """The column provides a unique value per row. Each table must provide
    exactly one INDEX column. The column's :class:`.DataType` must be INT32,
    INT64, or TIMESTAMP."""

    Nullable = "NULLABLE"
    """Rows may contain null values for this column. When appending rows,
    NULLABLE columns may be left out entirely, in which case all rows being
    appended will use null values for that column."""
