from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    ColumnType,
    DecimationMethod,
    DecimationOptions,
    QueryDecimatedDataRequest,
)

client = DataFrameClient()

# List a table
response = client.list_tables(take=1)
table = response.tables[0]
y_column = next(
    (col for col in table.columns if col.column_type != ColumnType.Index),
    table.columns[0],
)

# Get table metadata by table id
client.get_table_metadata(table.id)

# Query decimated table data
request = QueryDecimatedDataRequest(
    decimation=DecimationOptions(
        x_column=None,
        y_columns=[y_column.name],
        intervals=1,
        method=DecimationMethod.MaxMin,
    )
)
rows = client.query_decimated_data(table.id, request)
print(rows.frame.model_dump())
