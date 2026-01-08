from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    ColumnType,
    DecimationMethod,
    DecimationOptions,
    QueryDecimatedDataRequest,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = DataFrameClient(configuration=server_configuration)

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
