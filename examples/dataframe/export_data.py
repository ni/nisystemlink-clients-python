from shutil import copyfileobj

import pandas as pd
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    ColumnFilter,
    ColumnOrderBy,
    ExportFormat,
    ExportTableDataRequest,
    FilterOperation,
)

client = DataFrameClient()

# List a table
response = client.list_tables(take=1)
table = response.tables[0]

# Export table data with query options
request = ExportTableDataRequest(
    columns=["col1"],
    order_by=[ColumnOrderBy(column="col2", descending=True)],
    filters=[ColumnFilter(column="col1", operation=FilterOperation.NotEquals, value=0)],
    response_format=ExportFormat.CSV,
)

data = client.export_table_data(id=table.id, query=request)

# Write the export data to a file
with open(f"{table.name}.csv", "wb") as f:
    copyfileobj(response, f)

# Alternatively, load the export data into a pandas dataframe
df = pd.read_csv(data)
