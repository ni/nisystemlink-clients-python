from nisystemlink.clients.dataframe import DataFrameClient

client = DataFrameClient()

# List a table
client.list_tables(take=1)

# Get table metadata by table id
client.get_table_metadata("639126ad256e5501f9a3cca5")

# Get table data by table id
client.get_table_data("639126ad256e5501f9a3cca5")
