class DataFrameError(Exception):
    """Base class for Dataframe errors."""

    pass


class InvalidIndexError(DataFrameError):
    """Raised when an invalid or missing index column is encountered."""

    def __init__(self, index_name: str = None) -> None:
        self.index_name = index_name
        self.message = "Data frame must contain one index."
        if index_name:
            self.message = (
                f"Column '{self.index_name}' must be of type INT32, INT64, or TIMESTAMP to be an index column."
            )
        super().__init__(self.message)


class InvalidColumnTypeError(DataFrameError):
    """Raised when a column has an unsupported data type."""

    def __init__(self, column_name: str, column_type: str) -> None:
        self.column_name = column_name
        self.column_type = column_type
        self.message = f"Column '{column_name}' has an unsupported datatype: {column_type}"
        super().__init__(self.message)
