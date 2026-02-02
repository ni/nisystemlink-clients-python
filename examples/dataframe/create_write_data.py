import random
from datetime import datetime

try:
    import pyarrow as pa  # type: ignore
except Exception:
    pa = None
try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None
from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    AppendTableDataRequest,
    Column,
    ColumnType,
    CreateTableRequest,
    DataFrame,
    DataType,
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


print(f"Created table with ID: {table_id}")

print("Appending data to table...")

# Append via explicit AppendTableDataRequest (JSON)
frame_request = DataFrame(
    data=[[str(i), str(random.random()), datetime.now().isoformat()] for i in range(3)]
)
client.append_table_data(table_id, AppendTableDataRequest(frame=frame_request))

# Append via DataFrame model directly (JSON)
frame_direct = DataFrame(
    data=[
        [str(i + 3), str(random.random()), datetime.now().isoformat()] for i in range(3)
    ]
)
client.append_table_data(table_id, frame_direct)

if pa is not None:
    print("Appending data to table via Arrow RecordBatches...")
    # Append via single RecordBatch (Arrow)
    batch_single = pa.record_batch(
        [
            pa.array([6, 7, 8], type=pa.int32()),
            pa.array([0.1, 0.2, 0.3], type=pa.float32()),
            pa.array([datetime.now() for _ in range(3)], pa.timestamp("ms")),
        ],
        names=["ix", "Float_Column", "Timestamp_Column"],
    )
    client.append_table_data(table_id, batch_single)

    # Append via iterable of RecordBatches (Arrow)
    batch_list = [
        pa.record_batch(
            [
                pa.array([9, 10], type=pa.int32()),
                pa.array([0.4, 0.5], type=pa.float32()),
                pa.array([datetime.now() for _ in range(2)], pa.timestamp("ms")),
            ],
            names=["ix", "Float_Column", "Timestamp_Column"],
        )
    ]
    client.append_table_data(table_id, batch_list)

    if pd is not None:
        print("Appending data to table via Pandas DataFrame...")
        # Append via DataFrame (Pandas)
        df = pd.DataFrame(
            {
                "ix": [11, 12, 13],
                "Float_Column": [0.6, 0.7, 0.8],
                "Timestamp_Column": [datetime.now() for _ in range(3)],
            }
        )

        # Optional - coerce df types to the dataframe table schema
        df = df.astype(
            {
                "ix": "Int32",
                "Float_Column": "float32",
                "Timestamp_Column": "datetime64[ns]",
            }
        )

        # convert Pandas DataFrame to Arrow RecordBatch
        batch_single = pa.record_batch(df)

        client.append_table_data(table_id, batch_single)

# Mark end_of_data for the table
# Supply `None` and `end_of_data=True`
print("Finished appending data.")
client.append_table_data(table_id, None, end_of_data=True)
