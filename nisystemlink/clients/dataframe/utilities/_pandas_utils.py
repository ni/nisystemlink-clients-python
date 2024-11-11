from typing import List, Optional, Union

import pandas as pd

from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import Column, ColumnType, DataType
from ._pandas_exception import InvalidColumnTypeError, InvalidIndexError

UNSUPPORTED_PANDAS_INT_TYPES = ["int8", "int16"]
"""List of unsupported pandas integer types for conversion to `DataType`."""

UNSUPPORTED_PANDAS_FLOAT_TYPES = ["float16"]
"""List of unsupported pandas float types for conversion to `DataType`."""

SUPPORTED_INDEX_DATA_TYPE = [DataType.Int32, DataType.Int64, DataType.Timestamp]
"""List of supported index data types for table creation.

Only these `DataType` values are allowed for the index column of the table.
"""
SUPPORTED_PANDAS_DATATYPE_MAPPING = {
    "bool": DataType.Bool,
    "int32": DataType.Int32,
    "int64": DataType.Int64,
    "float32": DataType.Float32,
    "float64": DataType.Float64,
    "object": DataType.String,
    "datetime64[ns]": DataType.Timestamp,
}
"""Mapping of pandas data types to `DataType`.

This dictionary maps commonly used pandas data types to the corresponding `DataType` used in table creation.
"""


def _pandas_dtype_to_data_type(dtype: str) -> Optional[DataType]:
    """Convert pandas data type to `DataType`.

    Args:
        dtype (str): Pandas data type.

    Returns:
        Optional[DataType]: `DataType`or `None` if match not found.
    """
    if dtype in SUPPORTED_PANDAS_DATATYPE_MAPPING:
        return SUPPORTED_PANDAS_DATATYPE_MAPPING[dtype]
    return None


def _type_cast_column_datatype(
    data: Union[pd.Index, pd.Series]
) -> Union[pd.Index, pd.Series]:
    """Process data to convert to supported type if necessary.

    Args:
        data (Union[pd.Index, pd.Series]): Data to be processed.

    Returns:
        Union[pd.Index, pd.Series]: Processed data.
    """
    if pd.api.types.is_unsigned_integer_dtype(data):
        data = pd.to_numeric(data, downcast="integer")
        pd_dtype = data.dtype

    if pd_dtype in UNSUPPORTED_PANDAS_INT_TYPES:
        data = data.astype("int32")

    elif pd_dtype in UNSUPPORTED_PANDAS_FLOAT_TYPES:
        data = data.astype("float32")

    return data


def _infer_index_column(self, df: pd.DataFrame) -> Column:
    """Infer the index column for table creation.

    Args:
        df (pd.DataFrame): Pandas Dataframe.

    Raises:
        InvalidIndexError: If multiple index present or index is of unsupported type.

    Returns:
        Column: Valid `Column` to the table.
    """
    index = df.index.name

    if not index:
        raise InvalidIndexError(index_name=index)
    
    pd_dtype = df.index.dtype
    if (
        pd.api.types.is_any_real_numeric_dtype(df.index)
        and pd_dtype not in SUPPORTED_PANDAS_DATATYPE_MAPPING
    ):
        df.index = _type_cast_column_datatype(df.index)
        pd_dtype = df.index.dtype
        
    data_type = _pandas_dtype_to_data_type(pd_dtype)

    if data_type not in SUPPORTED_INDEX_DATA_TYPE:
        raise InvalidIndexError(index_name=index)
    
    return Column(name=index, data_type=data_type, column_type=ColumnType.Index)


def _infer_dataframe_columns(
    self, df: pd.DataFrame, nullable_columns: bool
) -> List[Column]:
    """Infer the columns for table creation.

    Args:
        df (pd.DataFrame): Pandas Dataframe.
        nullable_columns (bool): Make the columns nullable.

    Raises:
        InvalidColumnTypeError: If data type of the column is unsupported.

    Returns:
        List[Column]: Columns to the table.
    """
    columns = []

    column_type = ColumnType.Nullable if nullable_columns else ColumnType.Normal

    for column_name in df.columns:
        pd_dtype = df[column_name].dtype
        if (
            pd.api.types.is_any_real_numeric_dtype(pd_dtype)
            and pd_dtype not in SUPPORTED_PANDAS_DATATYPE_MAPPING
        ):
            df[column_name] = _type_cast_column_datatype(df[column_name])
            pd_dtype = df[column_name].dtype

        data_type = _pandas_dtype_to_data_type(pd_dtype)
        if data_type is None:
            raise InvalidColumnTypeError(column_name, pd_dtype)
        
        columns.append(
            Column(name=column_name, data_type=data_type, column_type=column_type)
        )
    return columns


def _get_table_index_name(client: DataFrameClient, table_id: str) -> str:
    """Get the index name from the table columns.

    Args:
        client (DataFrameClient): Instance of the `DataFrameclient`.
        table_id (str): ID of the table.

    Returns:
        str: Name of the index column
    """
    columns = client.get_table_metadata(table_id).columns
    for column in columns:
        if column.column_type == ColumnType.Index:
            return column.name
    return None
