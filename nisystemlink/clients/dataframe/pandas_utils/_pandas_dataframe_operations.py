from typing import List, Optional, Union, Tuple

import pandas as pd

from ._helper import _infer_index_column, _infer_dataframe_columns
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    AppendTableDataRequest,
    ColumnType,
    CreateTableRequest,
    DataFrame,
    QueryDecimatedDataRequest,
)
def create_table_from_pandas_df(
    client: DataFrameClient, df: pd.DataFrame, table_name: str, nullable_columns: bool
) -> str:
    """Create a table from a pandas DataFrame.

    Args:
        client (DataFrameClient): Instance of DataFrameClient.
        df (pd.DataFrame): Pandas dataframe.
        table_name (str): Name of the table.
        nullable_columns (bool): Make the columns nullable.

    Returns:
        str: ID of the table.
    """
    index = _infer_index_column(df)
    table_columns = [index]

    dataframe_columns = _infer_dataframe_columns(df, nullable_columns)
    table_columns += dataframe_columns

    table_id = client.create_table(
        CreateTableRequest(name=table_name, columns=table_columns)
    )
    return table_id


def append_pandas_df(client: DataFrameClient, table_id: str, df: pd.DataFrame) -> None:
    """Append `df` to table.

    Args:
        client: Instance of DataFrameClient.
        table_id: ID of the table.
        df: Pandas DataFrame containing the data to append.

    Returns:
        None
    """
    frame = DataFrame()
    frame.from_pandas(df)
    client.append_table_data(
        table_id, data=AppendTableDataRequest(frame=frame, endOfData=True)
    )


def query_decimated_pandas_df(
    client: DataFrameClient,
    table_id: str,
    request: QueryDecimatedDataRequest,
    index: bool,
) -> pd.DataFrame:
    """Query data from the table.

    Args:
        client (DataFrameClient): Instance of DataFrameClient.
        table_id (str): ID of the table.
        request (QueryDecimatedDataRequest): Request to query decimated data.

    Returns:
        pd.DataFrame: Data in pandas dataframe.
    """
    index_name: str = None
    if index:
        columns = client.get_table_metadata(table_id).columns
        for column in columns:
            if column.column_type == ColumnType.Index:
                index_name = column.name
                if request:
                    request.columns.append(index_name)
                break
    response = client.query_decimated_data(table_id, request)
    return response.frame.to_pandas(index_name)