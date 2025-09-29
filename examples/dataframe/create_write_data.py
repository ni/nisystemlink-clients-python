import random
from datetime import datetime

try:
    import pyarrow as pa  # type: ignore
except Exception:
    pa = None
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

# Append via explicit AppendTableDataRequest (JSON)
frame_request = DataFrame(
    data=[[i, random.random(), datetime.now().isoformat()] for i in range(3)]
)
client.append_table_data(table_id, AppendTableDataRequest(frame=frame_request))

# Append via DataFrame model directly (JSON)
frame_direct = DataFrame(
    data=[[i + 3, random.random(), datetime.now().isoformat()] for i in range(3)]
)
client.append_table_data(table_id, frame_direct)

if pa is not None:
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

    # Mark end_of_data for the table
    # Supply `None` and `end_of_data=True`
    client.append_table_data(table_id, None, end_of_data=True)
else:
    # If pyarrow not installed, flush via JSON path
    client.append_table_data(table_id, None, end_of_data=True)
