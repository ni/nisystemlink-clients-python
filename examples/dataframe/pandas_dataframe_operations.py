import pandas as pd
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    ColumnOrderBy,
    DecimationMethod,
    DecimationOptions,
    QueryDecimatedDataRequest,
    QueryTableDataRequest,
)
from nisystemlink.clients.dataframe.utilities import (
    append_pandas_df_to_table,
    create_table_from_pandas_df,
    create_table_with_data_from_pandas_df,
    InvalidColumnTypeError,
    InvalidIndexError,
    query_decimated_table_data_as_pandas_df,
    query_table_data_as_pandas_df,
)

client = DataFrameClient()
df: pd.DataFrame = pd.DataFrame(
    data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=["a", "b", "c"]
)
df.set_index("a", inplace=True)
print(df)

try:
    table_id = create_table_from_pandas_df(
        client, df, "Example Table", nullable_columns=False
    )
    print(f"\nTable created with ID: {table_id}")
except (InvalidColumnTypeError, InvalidIndexError) as e:
    print(f"Error creating table: {e}")

append_pandas_df_to_table(client, table_id, df)
print("\nData appended to the table.")

request = QueryDecimatedDataRequest(
    decimation=DecimationOptions(
        x_column="a",
        y_columns=["b"],
        intervals=1,
        method=DecimationMethod.MaxMin,
    )
)

queried_decimated_df = query_decimated_table_data_as_pandas_df(
    client, table_id, query=request, index=True
)
print("\nQueried decimated data as pandas dataframe:")
print(queried_decimated_df.columns)
query = QueryTableDataRequest(
    columns=["b", "c"], order_by=[ColumnOrderBy(column="b", descending=True)]
)
queried_df = query_table_data_as_pandas_df(
    client=client, table_id=table_id, query=query, index=True
)
print("\nQueried table data as pandas dataframe:")
print(queried_df)

client.delete_table(table_id)
print(f"\nTable {table_id} deleted successfully.")

try:
    table_id = create_table_with_data_from_pandas_df(client, df, "Example Table")
    print(f"\nTable created with ID: {table_id}")
except (InvalidColumnTypeError, InvalidIndexError) as e:
    print(f"Error creating table: {e}")

query = QueryTableDataRequest()
table_data = query_table_data_as_pandas_df(
    client=client, table_id=table_id, query=query, index=True
)

print("\nTable data as pandas DataFrame:")
print(table_data)

client.delete_table(table_id)
print(f"\nTable {table_id} deleted successfully.\n")
