from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    DecimationMethod,
    DecimationOptions,
    QueryDecimatedDataRequest,
)

client = DataFrameClient()

# List a table
response = client.list_tables(take=1)
table = response.tables[0]

# Get table metadata by table id
client.get_table_metadata(table.id)

# Query decimated table data
request = QueryDecimatedDataRequest(
    decimation=DecimationOptions(
        x_column="index",
        y_columns=["col1"],
        intervals=1,
        method=DecimationMethod.MaxMin,
    )
)
client.query_decimated_data(table.id, request)
