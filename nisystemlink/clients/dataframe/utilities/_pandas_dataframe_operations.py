import pandas as pd

from ._pandas_utils import (
    _infer_index_column,
    _infer_dataframe_columns,
    _get_table_index_name,
)
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    AppendTableDataRequest,
    CreateTableRequest,
    DataFrame,
    QueryTableDataRequest,
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


def append_pandas_df_to_table(client: DataFrameClient, table_id: str, df: pd.DataFrame) -> None:
    """Append `df` to table.

    Args:
        client: Instance of `DataFrameClient`.
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


def query_decimated_table_data_as_pandas_df(
    client: DataFrameClient,
    table_id: str,
    query: QueryDecimatedDataRequest,
    index: bool,
) -> pd.DataFrame:
    """Query data from the table.

    Args:
        client (DataFrameClient): Instance of DataFrameClient.
        table_id (str): ID of the table.
        query (QueryDecimatedDataRequest): Request to query decimated data.
        index (bool, optional): Whether index column to be included.

    Returns:
        pd.DataFrame: Table data in pandas dataframe format.
    """
    index_name: str = None
    if index:
        index_name = _get_table_index_name(client=client, table_id=table_id)
        if query and (index_name not in query.columns):
            query.columns.append(index_name)
    response = client.query_decimated_data(table_id, query)
    return response.frame.to_pandas(index_name)


def query_table_data_as_pandas_df(
    client: DataFrameClient,
    table_id: str,
    query: QueryTableDataRequest,
    index: bool = False,
) -> pd.DataFrame:
    """Query data from the table.

    Args:
        client (DataFrameClient): Instance of  `DataFrameClient`.
        table_id (str): ID of the table.
        query (QueryTableDataRequest): Request to query data.
        index (bool, optional): Whether index column to be included.

    Returns:
        pd.DataFrame: Table data in pandas dataframe format.
    """
    continuation_token = None
    all_rows = []
    index_name: str = None

    if index:
        index_name = _get_table_index_name(client=client, table_id=table_id)
        if query and (index_name not in query.columns):
            query.columns.append(index_name)

    while True:
        response = client.query_table_data(table_id, query)
        all_rows.append(response.frame.to_pandas(index_name))
        continuation_token = response.continuation_token
        
        if continuation_token:
            query.continuation_token=continuation_token
        else:
            break
    
    return pd.concat(all_rows, ignore_index=not(index))