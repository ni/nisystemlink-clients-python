# -*- coding: utf-8 -*-
import csv
import io
import re
import time
import warnings
from datetime import datetime, timezone
from typing import Callable, List, TypedDict

import pytest  # type: ignore
import responses
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core.helpers._iterator_file_like import IteratorFileLike
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    AppendTableDataRequest,
    Column,
    ColumnFilter,
    ColumnMetadataPatch,
    ColumnOrderBy,
    ColumnType,
    CreateTableRequest,
    DataFrame,
    DataType,
    DecimationMethod,
    DecimationOptions,
    ExportFormat,
    ExportTableDataRequest,
    FilterOperation,
    ModifyTableRequest,
    ModifyTablesRequest,
    QueryDecimatedDataRequest,
    QueryTableDataRequest,
    QueryTablesRequest,
    TableMetadataModification,
)

_DataElement = str | float | int | bool | datetime | None
_DataFrameData = List[List[_DataElement]]
_TestResultIdArg = TypedDict(
    "_TestResultIdArg", {"test_result_id": str | None}, total=False
)

int_index_column = Column(
    name="index", data_type=DataType.Int32, column_type=ColumnType.Index
)

table_with_data_columns = [
    int_index_column,
    Column(name="float", data_type=DataType.Float64),
    Column(
        name="int",
        data_type=DataType.Int64,
        column_type=ColumnType.Nullable,
    ),
    Column(name="bool", data_type=DataType.Bool),
    Column(name="string", data_type=DataType.String),
]

basic_table_model = CreateTableRequest(columns=[int_index_column])


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a DataFrameClient instance."""
    return DataFrameClient(enterprise_config)


@pytest.fixture(scope="class")
def create_table(client: DataFrameClient):
    """Fixture to return a factory that creates tables."""
    tables = []

    def _create_table(table: CreateTableRequest | None = None) -> str:
        id = client.create_table(table or basic_table_model)
        tables.append(id)
        return id

    yield _create_table

    client.delete_tables(tables)


@pytest.fixture(scope="class")
def test_tables(create_table):
    """Fixture to create a set of test tables."""
    ids = []
    for i in range(1, 4):
        ids.append(
            create_table(
                CreateTableRequest(
                    columns=[
                        Column(
                            name="time",
                            data_type=DataType.Timestamp,
                            column_type=ColumnType.Index,
                            properties={"cat": "meow"},
                        ),
                        Column(name="value", data_type=DataType.Int32),
                    ],
                    name=f"Python API test table {i} (delete me)",
                    properties={"dog": "woof"},
                )
            )
        )
    return ids


@pytest.fixture(scope="class")
def supports_test_result_id(client: DataFrameClient) -> bool:
    """Fixture to determine if the server supports test result IDs."""
    api_info = client.api_info()
    result = api_info.operations.create_tables.version >= 2
    if not result:
        warnings.warn(
            (
                "The selected version of the DataFrame Service does not support test "
                "result IDs. Tests will not attempt to set a test result ID."
            )
        )
    return result


@pytest.fixture(scope="class")
def table_with_data(client: DataFrameClient, create_table) -> str:
    """Fixture to create a table with data."""
    id = create_table(CreateTableRequest(columns=table_with_data_columns))

    frame = TestDataFrame._create_data_frame(
        table_with_data_columns,
        data=[
            [1, 4.5, 30, False, "dog"],
            [2, 3.5, None, True, "cat"],
            [3, 2.5, 10, True, "bunny"],
            [4, 1.5, 40, False, "cow"],
        ],
    )
    client.append_table_data(id, AppendTableDataRequest(frame=frame, end_of_data=True))
    TestDataFrame._wait_for_table_data(client, id, minimum_row_count=len(frame.data))

    return id


@pytest.mark.enterprise
@pytest.mark.integration
class TestDataFrame:
    @staticmethod
    def _wait_for_table_data(
        client: DataFrameClient,
        table_id: str,
        minimum_row_count: int,
        index_column: str = "index",
        timeout: float = 5.0,
        sleep_duration: float = 0.2,
    ) -> int:
        """Helper function to wait for table data to be available by polling get_table_data.

        Args:
            client: The DataFrameClient to use for checking data availability
            table_id: ID of the table to check
            expected_row_count: Expected number of rows in the table
            index_column: Name of the index column to query (default: "index")
            timeout: Maximum time to wait in seconds (default: 2.0)
            sleep_duration: Sleep duration between attempts in seconds (default: 0.2)

        Returns:
            The actual number of rows found in the table
        """
        start_time = time.time()

        while True:
            response = client.get_table_data(table_id, columns=[index_column], take=1)
            actual_row_count = response.total_row_count
            if actual_row_count >= minimum_row_count:
                return actual_row_count

            elapsed_time = time.time() - start_time
            assert elapsed_time < timeout, (
                f"Failed to get expected row count {minimum_row_count} after "
                f"{elapsed_time: .2f} seconds (last count: {actual_row_count})"
            )

            time.sleep(sleep_duration)

    def _new_single_int_table(self, create_table, column_name: str = "a") -> str:
        return create_table(
            CreateTableRequest(
                columns=[
                    Column(
                        name=column_name,
                        data_type=DataType.Int64,
                        column_type=ColumnType.Index,
                    )
                ]
            )
        )

    @staticmethod
    def _create_data_frame(
        columns: List[Column],
        data: _DataFrameData,
        include_column_names: bool = False,
    ) -> DataFrame:
        column_names = [col.name for col in columns] if include_column_names else None
        converted_data = [
            [
                TestDataFrame._data_value_to_str(columns[col_idx], value)
                for col_idx, value in enumerate(row)
            ]
            for row in data
        ]
        return DataFrame(columns=column_names, data=converted_data)

    @staticmethod
    def _read_data_frame(
        columns: List[Column],
        frame: DataFrame,
    ) -> _DataFrameData:
        frame_columns = (
            frame.columns
            if frame.columns is not None
            else [col.name for col in columns]
        )
        column_map = {col.name: col for col in columns}
        return [
            [
                TestDataFrame._str_to_data_value(
                    column_map[frame_columns[col_idx]], value
                )
                for col_idx, value in enumerate(row)
            ]
            for row in frame.data
        ]

    @staticmethod
    def _data_value_to_str(column: Column, value: _DataElement) -> str | None:
        if value is None:
            assert column.column_type == ColumnType.Nullable
            return None
        if isinstance(value, bool):
            assert column.data_type == DataType.Bool
            return "true" if value else "false"
        if isinstance(value, int):
            assert column.data_type in (DataType.Int32, DataType.Int64)
            return str(value)
        if isinstance(value, float):
            if column.data_type == DataType.Float32:
                return f"{value: .9g}"
            assert column.data_type == DataType.Float64
            return f"{value: .17g}"
        if isinstance(value, datetime):
            assert column.data_type == DataType.Timestamp
            return value.isoformat()
        assert isinstance(value, str) and column.data_type == DataType.String
        return value

    @staticmethod
    def _str_to_data_value(column: Column, value: str | None) -> _DataElement:
        if value is None:
            assert column.column_type == ColumnType.Nullable
            return None
        if column.data_type == DataType.Bool:
            result = value.lower() == "true"
            assert result or value.lower() == "false"
            return result
        if column.data_type in (DataType.Int32, DataType.Int64):
            return int(value)
        if column.data_type in (DataType.Float32, DataType.Float64):
            return float(value)
        if column.data_type == DataType.Timestamp:
            return datetime.fromisoformat(value)
        assert column.data_type == DataType.String
        return value

    @staticmethod
    def _read_exported_csv(
        columns: List[Column], data: IteratorFileLike
    ) -> tuple[List[str], _DataFrameData]:
        column_map = {col.name: col for col in columns}
        csv_content = data.read().decode("utf-8")

        # The CSV reader doesn't distinguish between "" and an empty field (e.g., `,,`).
        # The server returns the former for empty strings and the latter for null values
        # (of any data type). So we replace empty fields with a placeholder value that
        # we convert back to None below.
        csv_content = re.sub(r"([,\n])([,\r])", r"\1NULL_PLACEHOLDER\2", csv_content)

        text_stream = io.StringIO(csv_content, newline="")
        reader = csv.reader(text_stream)

        # Read the column names from the header row.
        column_names = next(reader)
        csv_columns = []
        for name in column_names:
            column = column_map.get(name)
            assert column is not None, f"CSV includes unknown column {name}"
            csv_columns.append(column)

        rows = [
            [
                TestDataFrame._str_to_data_value(
                    csv_columns[col_idx],
                    value if value != "NULL_PLACEHOLDER" else None,
                )
                for col_idx, value in enumerate(row)
            ]
            for row in reader
        ]

        return (column_names, rows)

    def test__api_info__returns(self, client):
        response = client.api_info()

        assert len(response.model_dump()) != 0

    def test__create_table__metadata_is_correct(
        self, client: DataFrameClient, test_tables: List[str]
    ):
        table_metadata = client.get_table_metadata(test_tables[0])

        assert table_metadata.name == "Python API test table 1 (delete me)"
        assert table_metadata.properties == {"dog": "woof"}
        assert table_metadata.columns == [
            Column(
                name="time",
                data_type=DataType.Timestamp,
                column_type=ColumnType.Index,
                properties={"cat": "meow"},
            ),
            Column(
                name="value",
                data_type=DataType.Int32,
                column_type=ColumnType.Normal,
                properties={},
            ),
        ]
        assert table_metadata.test_result_id is None

    def test__create_table__supports_test_result(
        self,
        client: DataFrameClient,
        create_table: Callable[[CreateTableRequest], str],
        supports_test_result_id: bool,
    ):
        test_result_id = "Test result" if supports_test_result_id else None
        id = create_table(
            CreateTableRequest(
                columns=[
                    Column(
                        name="index",
                        data_type=DataType.Int32,
                        column_type=ColumnType.Index,
                    )
                ],
                name="Test table with test result ID",
                test_result_id=test_result_id,
            )
        )

        table = client.get_table_metadata(id)
        assert table.test_result_id == test_result_id

        page = client.list_tables(take=1, id=[id])
        assert len(page.tables) == 1
        assert page.tables[0].test_result_id == test_result_id
        assert page.continuation_token is None

        page = client.query_tables(
            QueryTablesRequest(filter="id == @0", substitutions=[id], take=1)
        )
        assert len(page.tables) == 1
        assert page.tables[0].test_result_id == test_result_id
        assert page.continuation_token is None

    def test__get_table__correct_timestamp(self, client: DataFrameClient, create_table):
        id = create_table(basic_table_model)
        table = client.get_table_metadata(id)

        now = datetime.now().timestamp()
        # Assert that timestamp is within 10 seconds of now
        assert table.created_at.timestamp() == pytest.approx(now, abs=10)

    def test__get_table_invalid_id__raises(self, client: DataFrameClient):
        with pytest.raises(ApiException, match="invalid table ID"):
            client.get_table_metadata("invalid_id")

    def test__list_tables__returns(
        self, client: DataFrameClient, test_tables: List[str]
    ):
        first_page = client.list_tables(
            take=2,
            id=test_tables[:3],
            order_by="NAME",
            order_by_descending=True,
        )

        assert len(first_page.tables) == 2
        assert first_page.tables[0].id == test_tables[-1]  # Asserts descending order
        assert first_page.continuation_token is not None

        second_page = client.list_tables(
            id=test_tables[:3],
            order_by="NAME",
            order_by_descending=True,
            continuation_token=first_page.continuation_token,
        )

        assert len(second_page.tables) == 1
        assert second_page.continuation_token is None

    def test__query_tables__returns(
        self, client: DataFrameClient, test_tables: List[str]
    ):
        query = QueryTablesRequest(
            filter="""(id == @0 or id == @1 or id == @2)
                and createdWithin <= RelativeTime.CurrentWeek
                and supportsAppend == @3 and rowCount < @4""",
            substitutions=[test_tables[0], test_tables[1], test_tables[2], True, 1],
            reference_time=datetime.now(tz=timezone.utc),
            take=2,
            order_by="NAME",
            order_by_descending=True,
        )
        first_page = client.query_tables(query)

        assert len(first_page.tables) == 2
        assert first_page.tables[0].id == test_tables[-1]  # Asserts descending order
        assert first_page.continuation_token is not None

        query.continuation_token = first_page.continuation_token

        second_page = client.query_tables(query)
        assert len(second_page.tables) == 1
        assert second_page.continuation_token is None

    def test__modify_table__returns(
        self, client: DataFrameClient, create_table, supports_test_result_id: bool
    ):
        id = create_table(basic_table_model)

        client.modify_table(
            id,
            ModifyTableRequest(
                metadata_revision=2,
                name="Modified table",
                properties={"cow": "moo"},
                columns=[
                    ColumnMetadataPatch(name="index", properties={"sheep": "baa"})
                ],
                **self._test_result_id_if_supported(
                    "Test result", supports_test_result_id
                ),
            ),
        )
        table = client.get_table_metadata(id)

        assert table.metadata_revision == 2
        assert table.name == "Modified table"
        assert table.test_result_id == (
            "Test result" if supports_test_result_id else None
        )
        assert table.properties == {"cow": "moo"}
        assert table.columns[0].properties == {"sheep": "baa"}

        client.modify_table(id, ModifyTableRequest(properties={"bee": "buzz"}))
        table = client.get_table_metadata(id)

        assert table.properties == {"cow": "moo", "bee": "buzz"}
        assert table.name == "Modified table"
        assert table.test_result_id == (
            "Test result" if supports_test_result_id else None
        )

        client.modify_table(
            id,
            ModifyTableRequest(
                metadata_revision=4,
                name=None,
                properties={"cow": None},
                columns=[ColumnMetadataPatch(name="index", properties={"sheep": None})],
                **self._test_result_id_if_supported(None, supports_test_result_id),
            ),
        )
        table = client.get_table_metadata(id)

        assert table.metadata_revision == 4
        assert table.name == id
        assert table.test_result_id is None
        assert table.properties == {"bee": "buzz"}
        assert table.columns[0].properties == {}

    @staticmethod
    def _test_result_id_if_supported(
        test_result_id: str | None, supports_test_result_id: bool
    ) -> _TestResultIdArg:
        return {"test_result_id": test_result_id} if supports_test_result_id else {}

    def test__delete_table__deletes(self, client: DataFrameClient):
        id = client.create_table(
            basic_table_model
        )  # Don't use fixture to avoid deleting the table twice

        assert client.delete_table(id) is None

        with pytest.raises(ApiException, match="404 Not Found"):
            client.get_table_metadata(id)

    def test__delete_tables__deletes(self, client: DataFrameClient):
        ids = [client.create_table(basic_table_model) for _ in range(3)]

        assert client.delete_tables(ids) is None

        assert client.list_tables(id=ids).tables == []

    def test__delete_tables__returns_partial_success(self, client: DataFrameClient):
        id = client.create_table(basic_table_model)

        response = client.delete_tables([id, "invalid_id"])

        assert response is not None
        assert response.deleted_table_ids == [id]
        assert response.failed_table_ids == ["invalid_id"]
        assert len(response.error.inner_errors) == 1

    def test__modify_tables__modifies_tables(
        self, client: DataFrameClient, create_table, supports_test_result_id: bool
    ):
        ids = [create_table(basic_table_model) for _ in range(3)]

        updates = [
            TableMetadataModification(
                id=id,
                name="Modified table",
                test_result_id="Test result" if supports_test_result_id else None,
                properties={"duck": "quack"},
            )
            for id in ids
        ]

        assert client.modify_tables(ModifyTablesRequest(tables=updates)) is None

        for table in client.list_tables(id=ids).tables:
            assert table.name == "Modified table"
            assert table.test_result_id == (
                "Test result" if supports_test_result_id else None
            )
            assert table.properties == {"duck": "quack"}

        updates = [
            TableMetadataModification(id=id, properties={"pig": "oink"}) for id in ids
        ]

        assert (
            client.modify_tables(ModifyTablesRequest(tables=updates, replace=True))
            is None
        )

        for table in client.list_tables(id=ids).tables:
            assert table.name == "Modified table"
            assert table.test_result_id == (
                "Test result" if supports_test_result_id else None
            )
            assert table.properties == {"pig": "oink"}

        if supports_test_result_id:
            updates = [
                TableMetadataModification(id=id, test_result_id="") for id in ids
            ]

            assert client.modify_tables(ModifyTablesRequest(tables=updates)) is None

            for table in client.list_tables(id=ids).tables:
                assert table.name == "Modified table"
                assert table.test_result_id is None

    def test__modify_tables__returns_partial_success(
        self, client: DataFrameClient, create_table, supports_test_result_id: bool
    ):
        id = create_table(basic_table_model)

        updates = [
            TableMetadataModification(
                id=id,
                name="Modified table",
                test_result_id="Test result" if supports_test_result_id else None,
            )
            for id in [id, "invalid_id"]
        ]

        response = client.modify_tables(ModifyTablesRequest(tables=updates))

        assert response is not None
        assert response.modified_table_ids == [id]
        assert response.failed_modifications == [updates[1]]
        assert len(response.error.inner_errors) == 1

    def test__get_table_data__returns_correct_data(
        self, client: DataFrameClient, table_with_data: str
    ):
        response = client.get_table_data(
            table_with_data, columns=["index", "float"], order_by=["float"]
        )

        assert response.total_row_count == 4
        assert response.frame.columns == ["index", "float"]
        assert self._read_data_frame(table_with_data_columns, response.frame) == [
            [4, 1.5],
            [3, 2.5],
            [2, 3.5],
            [1, 4.5],
        ]

    def test__write_invalid_data__raises(
        self, client: DataFrameClient, test_tables: List[str]
    ):
        id = test_tables[0]

        frame = DataFrame(
            columns=["index", "non_existent_column"],
            data=[["1", "2"], ["2", "2"], ["3", "3"]],
        )

        with pytest.raises(ApiException, match="400 Bad Request"):
            client.append_table_data(id, AppendTableDataRequest(frame=frame))

    def test__query_table_data__sorts(
        self, client: DataFrameClient, table_with_data: str
    ):
        response = client.query_table_data(
            table_with_data,
            QueryTableDataRequest(
                columns=["index", "float"],
                order_by=[
                    ColumnOrderBy(column="bool"),
                    ColumnOrderBy(column="float", descending=True),
                ],
            ),
        )

        assert response.total_row_count == 4
        assert response.frame.columns == ["index", "float"]
        assert self._read_data_frame(table_with_data_columns, response.frame) == [
            [1, 4.5],  # bool=False
            [4, 1.5],  # bool=False
            [2, 3.5],  # bool=True
            [3, 2.5],  # bool=True
        ]

    def test__query_table_data__filters(
        self, client: DataFrameClient, table_with_data: str
    ):
        response = client.query_table_data(
            table_with_data,
            QueryTableDataRequest(
                columns=["index"],
                filters=[
                    ColumnFilter(
                        column="float",
                        operation=FilterOperation.GreaterThan,
                        value="1.5",
                    ),
                    ColumnFilter(
                        column="int",
                        operation=FilterOperation.NotEquals,
                        value=None,
                    ),
                    ColumnFilter(
                        column="string",
                        operation=FilterOperation.NotContains,
                        value="bun",
                    ),
                ],
            ),
        )

        assert response.total_row_count == 1
        assert response.frame.columns == ["index"]
        assert self._read_data_frame(table_with_data_columns, response.frame) == [[1]]

    def test__query_decimated_data__works(
        self, client: DataFrameClient, table_with_data: str
    ):
        response = client.query_decimated_data(
            table_with_data,
            QueryDecimatedDataRequest(
                columns=["index", "float"],
                decimation=DecimationOptions(
                    x_column="index",
                    y_columns=["float"],
                    intervals=1,
                    method=DecimationMethod.MaxMin,
                ),
            ),
        )

        assert response.frame.columns == ["index", "float"]
        assert self._read_data_frame(table_with_data_columns, response.frame) == [
            [1, 4.5],
            [4, 1.5],
        ]

    def test__export_table_data__includes_all_rows(
        self, client: DataFrameClient, table_with_data: str
    ):
        response = client.export_table_data(
            table_with_data,
            ExportTableDataRequest(
                order_by=[ColumnOrderBy(column="index")],
                response_format=ExportFormat.CSV,
            ),
        )

        column_names, data = self._read_exported_csv(table_with_data_columns, response)
        assert column_names == ["index", "float", "int", "bool", "string"]
        assert data == [
            [1, 4.5, 30, False, "dog"],
            [2, 3.5, None, True, "cat"],
            [3, 2.5, 10, True, "bunny"],
            [4, 1.5, 40, False, "cow"],
        ]

    def test__export_table_data__limits_to_take_rows(
        self, client: DataFrameClient, table_with_data: str
    ):
        response = client.export_table_data(
            table_with_data,
            ExportTableDataRequest(
                columns=["index"],
                order_by=[ColumnOrderBy(column="index", descending=True)],
                take=2,
                response_format=ExportFormat.CSV,
            ),
        )

        column_names, data = self._read_exported_csv(table_with_data_columns, response)
        assert column_names == ["index"]
        assert data == [[4], [3]]

    def test__append_table_data__append_request_success(
        self, client: DataFrameClient, create_table
    ):
        table_id = self._new_single_int_table(create_table)
        frame = DataFrame(columns=["a"], data=[["1"], ["2"]])
        client.append_table_data(
            table_id, AppendTableDataRequest(frame=frame, end_of_data=True)
        )
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 2
        assert metadata.supports_append is False

    def test__append_table_data__append_request_with_end_of_data_argument_disallowed(
        self, client: DataFrameClient, create_table
    ):
        request = AppendTableDataRequest(end_of_data=True)
        with pytest.raises(
            ValueError,
            match="end_of_data must not be provided separately when passing an AppendTableDataRequest.",
        ):
            client.append_table_data(
                self._new_single_int_table(create_table), request, end_of_data=True
            )

    def test__append_table_data__append_request_without_end_of_data_success(
        self, client: DataFrameClient, create_table
    ):
        table_id = self._new_single_int_table(create_table)
        frame = DataFrame(columns=["a"], data=[["7"], ["8"]])
        client.append_table_data(table_id, AppendTableDataRequest(frame=frame))
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 2
        assert metadata.supports_append is True

    def test__append_table_data__accepts_dataframe_model(
        self, client: DataFrameClient, create_table
    ):
        table_id = self._new_single_int_table(create_table)
        frame = DataFrame(columns=["a"], data=[["1"], ["2"]])
        client.append_table_data(table_id, frame, end_of_data=True)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 2
        assert metadata.supports_append is False

    def test__append_table_data__dataframe_without_end_of_data_success(
        self, client: DataFrameClient, create_table
    ):
        table_id = self._new_single_int_table(create_table)
        frame = DataFrame(columns=["a"], data=[["10"], ["11"]])
        client.append_table_data(table_id, frame)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 2
        assert metadata.supports_append is True

    def test__append_table_data__none_without_end_of_data_raises(
        self, client: DataFrameClient, create_table
    ):
        table_id = create_table(basic_table_model)
        with pytest.raises(
            ValueError, match="end_of_data must be provided when data is None"
        ):
            client.append_table_data(table_id, None)

    def test__append_table_data__flush_only_with_none(
        self, client: DataFrameClient, create_table
    ):
        table_id = self._new_single_int_table(create_table)
        client.append_table_data(table_id, None, end_of_data=True)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 0
        assert metadata.supports_append is False

    def test__append_table_data__arrow_ingestion_success(
        self, client: DataFrameClient, create_table
    ):
        pa = pytest.importorskip("pyarrow")
        table_id = self._new_single_int_table(create_table)
        batch = pa.record_batch([pa.array([10, 11, 12])], names=["a"])
        client.append_table_data(table_id, [batch], end_of_data=True)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 3
        assert metadata.supports_append is False
        with pytest.raises(ApiException):
            client.append_table_data(table_id, None, end_of_data=True)

    def test__append_table_data__single_recordbatch_success(
        self, client: DataFrameClient, create_table
    ):
        pa = pytest.importorskip("pyarrow")
        table_id = self._new_single_int_table(create_table)
        batch = pa.record_batch([pa.array([1, 2, 3])], names=["a"])
        client.append_table_data(table_id, batch, end_of_data=True)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 3
        assert metadata.supports_append is False
        with pytest.raises(ApiException):
            client.append_table_data(table_id, None, end_of_data=True)

    def test__append_table_data__arrow_ingestion_with_end_of_data_query_param_false(
        self, client: DataFrameClient, create_table
    ):
        pa = pytest.importorskip("pyarrow")
        table_id = self._new_single_int_table(create_table)
        batch1 = pa.record_batch([pa.array([4, 5, 6])], names=["a"])
        client.append_table_data(table_id, [batch1], end_of_data=False)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 3
        assert metadata.supports_append is True
        batch2 = pa.record_batch([pa.array([7, 8])], names=["a"])
        client.append_table_data(table_id, [batch2], end_of_data=True)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 5
        assert metadata.supports_append is False

    def test__append_table_data__empty_iterator_requires_end_of_data(
        self, client: DataFrameClient, create_table
    ):
        table_id = create_table(basic_table_model)
        with pytest.raises(
            ValueError,
            match="end_of_data must be provided when data iterator is empty.",
        ):
            client.append_table_data(table_id, [])
        client.append_table_data(table_id, [], end_of_data=True)
        metadata = client.get_table_metadata(table_id)
        assert metadata.row_count == 0
        assert metadata.supports_append is False

    def test__append_table_data__arrow_iterable_with_non_recordbatch_elements_raises(
        self, client: DataFrameClient, create_table
    ):
        pytest.importorskip("pyarrow")
        table_id = create_table(basic_table_model)
        with pytest.raises(
            ValueError,
            match="Iterable provided to data must yield pyarrow.RecordBatch objects.",
        ):
            client.append_table_data(table_id, [1, 2, 3])

    def test__append_table_data__arrow_iterable_without_pyarrow_raises_runtime_error(
        self, client: DataFrameClient, create_table, monkeypatch
    ):
        import nisystemlink.clients.dataframe._data_frame_client as df_module

        monkeypatch.setattr(df_module, "pa", None)
        table_id = create_table(basic_table_model)
        with pytest.raises(
            RuntimeError,
            match="pyarrow is not installed. Install to stream RecordBatches.",
        ):
            client.append_table_data(table_id, [object()])

    def test__append_table_data__arrow_ingestion_400_unsupported(
        self, client: DataFrameClient
    ):
        pa = pytest.importorskip("pyarrow")
        table_id = "mock_table_id"
        bad_batch = pa.record_batch([pa.array([1, 2, 3])], names=["b"])
        api_info_json = {
            "operations": {
                "create_tables": {"available": True, "version": 1},
                "delete_tables": {"available": True, "version": 1},
                "modify_metadata": {"available": True, "version": 1},
                "list_tables": {"available": True, "version": 1},
                "read_data": {"available": True, "version": 3},
                "write_data": {"available": True, "version": 1},
            }
        }

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{client.session.base_url}",
                json=api_info_json,
            )
            rsps.add(
                responses.POST,
                f"{client.session.base_url}tables/{table_id}/data",
                status=400,
            )
            with pytest.raises(ApiException) as excinfo:
                client.append_table_data(table_id, [bad_batch], end_of_data=True)

        assert "Arrow ingestion request was rejected" in str(excinfo.value)

    def test__append_table_data__arrow_ingestion_400_supported_passthrough(
        self, client: DataFrameClient
    ):
        pa = pytest.importorskip("pyarrow")
        table_id = "mock_table_id"
        bad_batch = pa.record_batch([pa.array([1, 2, 3])], names=["b"])
        api_info_json = {
            "operations": {
                "create_tables": {"available": True, "version": 1},
                "delete_tables": {"available": True, "version": 1},
                "modify_metadata": {"available": True, "version": 1},
                "list_tables": {"available": True, "version": 1},
                "read_data": {"available": True, "version": 3},
                "write_data": {"available": True, "version": 2},
            }
        }

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{client.session.base_url}",
                json=api_info_json,
            )
            rsps.add(
                responses.POST,
                f"{client.session.base_url}tables/{table_id}/data",
                status=400,
            )
            with pytest.raises(ApiException) as excinfo:
                client.append_table_data(table_id, [bad_batch], end_of_data=True)

        assert "Arrow ingestion request was rejected" not in str(excinfo.value)

    def test__append_table_data__arrow_ingestion_non_400_passthrough(
        self, client: DataFrameClient
    ):
        pa = pytest.importorskip("pyarrow")
        batch = pa.record_batch([pa.array([1, 2, 3])], names=["a"])
        with pytest.raises(ApiException) as excinfo:
            client.append_table_data(
                "111111111111111111111111", [batch], end_of_data=True
            )
        assert "Arrow ingestion request was rejected" not in str(excinfo.value)

    def test__append_table_data__unsupported_type_raises(
        self, client: DataFrameClient, create_table
    ):
        table_id = create_table(basic_table_model)
        with pytest.raises(ValueError, match="Unsupported type"):
            client.append_table_data(table_id, 123)  # type: ignore[arg-type]
