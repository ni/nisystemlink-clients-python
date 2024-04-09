import random
from datetime import datetime

from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    AppendTableDataRequest,
    Column,
    ColumnType,
    CreateTableRequest,
    DataFrame,
    DataType,
)

client = DataFrameClient()

# Create table
table_id = client.create_table(
    CreateTableRequest(
        name="Example Table",
        columns=[
            Column(name="ix", data_type=DataType.Int32, column_type=ColumnType.Index),
            Column(name="Float_Column", data_type=DataType.Float32),
            Column(name="Timestamp_Column", data_type=DataType.Timestamp),
        ],
    )
)

# Generate example data
frame = DataFrame(
    data=[[i, random.random(), datetime.now().isoformat()] for i in range(100)]
)

# Write example data to table
client.append_table_data(
    table_id, data=AppendTableDataRequest(frame=frame, endOfData=True)
)
