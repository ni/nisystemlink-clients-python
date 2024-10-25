from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import QueryTablesRequest

client = DataFrameClient()

# List all tables with more than 100k rows
query = QueryTablesRequest(
    filter="rowCount > 100000", order_by="CREATED_AT", order_by_descending=True
)

# Print the query results
for table in client.query_tables_generator(query):
    print(f"{table.created_at} \t {table.name} \t Rows={table.row_count}")
