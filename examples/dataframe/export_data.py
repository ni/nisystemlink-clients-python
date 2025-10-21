from shutil import copyfileobj

from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    ColumnFilter,
    ColumnOrderBy,
    ColumnType,
    DataType,
    ExportFormat,
    ExportTableDataRequest,
    FilterOperation,
)

client = DataFrameClient()

# List a table
response = client.list_tables(take=1)
table = response.tables[0]
index_column = next(
    (col for col in table.columns if col.column_type == ColumnType.Index)
)
order_column = next(
    (col for col in table.columns if col.name != index_column.name), index_column
)
filter_value = (
    "0001-01-01T00:00:00Z" if index_column.data_type == DataType.Timestamp else "0"
)

# Export table data with query options
request = ExportTableDataRequest(
    columns=[index_column.name],
    order_by=[ColumnOrderBy(column=order_column.name, descending=True)],
    filters=[
        ColumnFilter(
            column=index_column.name,
            operation=FilterOperation.NotEquals,
            value=filter_value,
        )
    ],
    response_format=ExportFormat.CSV,
)

data = client.export_table_data(id=table.id, query=request)

# Write the export data to a file
with open(f"{table.name}.csv", "wb") as f:
    copyfileobj(data, f)

# Alternatively, load the export data into a pandas dataframe
# import pandas as pd
# df = pd.read_csv(data)
