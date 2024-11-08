import pandas as pd

from nisystemlink.clients.dataframe.utilities import (
    append_pandas_df,
    create_table_from_pandas_df,
)
from nisystemlink.clients.dataframe.utilities import (
    InvalidIndexError,
    InvalidColumnTypeError,
)

from nisystemlink.clients.dataframe import DataFrameClient

client = DataFrameClient()

df = pd.DataFrame(data=[[1,2,3],[4,5,6],[7,8,9]], columns=["a","b","c"])

try:
    table_id = create_table_from_pandas_df(client, df, "Example Table")
except InvalidColumnTypeError or InvalidIndexError as e:
    print(e)

append_pandas_df(table_id, df)
