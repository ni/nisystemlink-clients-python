import pandas as pd

from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (DecimationMethod,
                                                   DecimationOptions,
                                                   QueryDecimatedDataRequest,
                                                   QueryTableDataRequest)
from nisystemlink.clients.dataframe.utilities import (
    InvalidColumnTypeError, InvalidIndexError, append_pandas_df_to_table,
    create_table_from_pandas_df, query_decimated_table_data_as_pandas_df, query_table_data_as_pandas_df)

client = DataFrameClient()

df = pd.DataFrame(data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=["a", "b", "c"])
df.set_index("a", inplace=True)

try:
    table_id = create_table_from_pandas_df(
        client, df, "Example Table", nullable_columns=False
    )
    print(f"Table created with ID: {table_id}")
except (InvalidColumnTypeError, InvalidIndexError) as e:
    print(f"Error creating table: {e}")

new_df = pd.DataFrame(data=[[9, 8, 7], [7, 8, 9]], columns=["a", "b", "c"])

append_pandas_df_to_table(client, table_id, new_df)
print("Data appended to the table.")

request = QueryDecimatedDataRequest(
    decimation=DecimationOptions(
        x_column="b",
        y_columns=["c"],
        intervals=1,
        method=DecimationMethod.MaxMin,
    )
)

queried_decimated_df = query_decimated_table_data_as_pandas_df(
    client, table_id, query=request, index=False
)
print("Queried decimated data as pandas dataframe:")
print(queried_decimated_df)

query=QueryTableDataRequest(filters=["b","c"], take=3)
queried_df = query_table_data_as_pandas_df(client=client, table_id=table_id, query=query)
print("Queried table data as pandas dataframe:")
print(queried_df)


