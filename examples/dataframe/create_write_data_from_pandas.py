import pandas as pd

from nisystemlink.clients.dataframe.pandas_utils import (
    append_pandas_df,
    create_table_from_pandas_df,
)
from nisystemlink.clients.dataframe.pandas_utils import (
    InvalidIndexError,
    InvalidColumnTypeError,
)

from nisystemlink.clients.dataframe import DataFrameClient

client = DataFrameClient()

# df = pd.read_csv("data/data.csv")

# try:
#     table_id = create_table_from_pandas_df(client, df, "Example Table")
# except InvalidColumnTypeError or InvalidIndexError as e:
#     print(e)

# append_pandas_df(table_id, df)
