# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import List

import pytest  # type: ignore
import responses
from nisystemlink.clients.core import ApiException
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
from responses import matchers

int_index_column = Column(
    name="index", data_type=DataType.Int32, column_type=ColumnType.Index
)

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


@pytest.mark.enterprise
@pytest.mark.integration
class TestDataFrame:
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

    def test__modify_table__returns(self, client: DataFrameClient, create_table):
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
            ),
        )
        table = client.get_table_metadata(id)

        assert table.metadata_revision == 2
        assert table.name == "Modified table"
        assert table.properties == {"cow": "moo"}
        assert table.columns[0].properties == {"sheep": "baa"}

        client.modify_table(id, ModifyTableRequest(properties={"bee": "buzz"}))
        table = client.get_table_metadata(id)

        assert table.properties == {"cow": "moo", "bee": "buzz"}
        assert table.name == "Modified table"

        client.modify_table(
            id,
            ModifyTableRequest(
                metadata_revision=4,
                name=None,
                properties={"cow": None},
                columns=[ColumnMetadataPatch(name="index", properties={"sheep": None})],
            ),
        )
        table = client.get_table_metadata(id)

        assert table.metadata_revision == 4
        assert table.name == id
        assert table.properties == {"bee": "buzz"}
        assert table.columns[0].properties == {}

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
        self, client: DataFrameClient, create_table
    ):
        ids = [create_table(basic_table_model) for _ in range(3)]

        updates = [
            TableMetadataModification(
                id=id, name="Modified table", properties={"duck": "quack"}
            )
            for id in ids
        ]

        assert client.modify_tables(ModifyTablesRequest(tables=updates)) is None

        for table in client.list_tables(id=ids).tables:
            assert table.name == "Modified table"
            assert table.properties == {"duck": "quack"}

        updates = [
            TableMetadataModification(id=id, properties={"pig": "oink"}) for id in ids
        ]

        assert (
            client.modify_tables(ModifyTablesRequest(tables=updates, replace=True))
            is None
        )

        for table in client.list_tables(id=ids).tables:
            assert table.properties == {"pig": "oink"}

    def test__modify_tables__returns_partial_success(
        self, client: DataFrameClient, create_table
    ):
        id = create_table(basic_table_model)

        updates = [
            TableMetadataModification(id=id, name="Modified table")
            for id in [id, "invalid_id"]
        ]

        response = client.modify_tables(ModifyTablesRequest(tables=updates))

        assert response is not None
        assert response.modified_table_ids == [id]
        assert response.failed_modifications == [updates[1]]
        assert len(response.error.inner_errors) == 1

    def test__read_and_write_data__works(self, client: DataFrameClient, create_table):
        id = create_table(
            CreateTableRequest(
                columns=[
                    int_index_column,
                    Column(
                        name="value",
                        data_type=DataType.Float64,
                        column_type=ColumnType.Nullable,
                    ),
                    Column(
                        name="ignore_me",
                        data_type=DataType.Bool,
                        column_type=ColumnType.Nullable,
                    ),
                ]
            )
        )

        frame = DataFrame(
            columns=["index", "value", "ignore_me"],
            data=[["1", "3.3", "True"], ["2", None, "False"], ["3", "1.1", "True"]],
        )

        client.append_table_data(
            id, AppendTableDataRequest(frame=frame, end_of_data=True)
        )

        # TODO: Remove mock when service supports flushing
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{client.session.base_url}tables/{id}/data",
                json={
                    "frame": {
                        "columns": ["index", "value"],
                        "data": [["3", "1.1"], ["1", "3.3"], ["2", None]],
                    },
                    "totalRowCount": 3,
                    "continuationToken": None,
                },
            )

            response = client.get_table_data(
                id, columns=["index", "value"], order_by=["value"]
            )

            assert response.total_row_count == 3
            assert response.frame == DataFrame(
                columns=["index", "value"],
                data=[["3", "1.1"], ["1", "3.3"], ["2", None]],
            )

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

    def test__query_table_data__sorts(self, client: DataFrameClient, create_table):
        id = create_table(
            CreateTableRequest(
                columns=[
                    int_index_column,
                    Column(name="col1", data_type=DataType.Float64),
                    Column(name="col2", data_type=DataType.Float64),
                ]
            )
        )

        frame = DataFrame(
            data=[["1", "2.5", "6.5"], ["2", "1.5", "5.5"], ["3", "2.5", "7.5"]],
        )

        client.append_table_data(
            id, AppendTableDataRequest(frame=frame, end_of_data=True)
        )

        # TODO: Remove mock when service supports flushing
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                f"{client.session.base_url}tables/{id}/query-data",
                json={
                    "frame": {
                        "columns": ["index", "col1", "col2"],
                        "data": [
                            ["2", "1.5", "5.5"],
                            ["3", "2.5", "7.5"],
                            ["1", "2.5", "6.5"],
                        ],
                    },
                    "totalRowCount": 3,
                    "continuationToken": None,
                },
                match=[
                    matchers.json_params_matcher(
                        {
                            "orderBy": [
                                {"column": "col1"},
                                {"column": "col2", "descending": True},
                            ]
                        }
                    )
                ],
            )

            response = client.query_table_data(
                id,
                QueryTableDataRequest(
                    order_by=[
                        ColumnOrderBy(column="col1"),
                        ColumnOrderBy(column="col2", descending=True),
                    ],
                ),
            )

            assert response.total_row_count == 3
            assert response.frame.data == [
                ["2", "1.5", "5.5"],
                ["3", "2.5", "7.5"],
                ["1", "2.5", "6.5"],
            ]

    def test__query_table_data__filters(self, client: DataFrameClient, create_table):
        id = create_table(
            CreateTableRequest(
                columns=[
                    int_index_column,
                    Column(name="float", data_type=DataType.Float64),
                    Column(
                        name="int",
                        data_type=DataType.Int64,
                        column_type=ColumnType.Nullable,
                    ),
                    Column(name="string", data_type=DataType.String),
                ]
            )
        )

        frame = DataFrame(
            data=[
                ["1", "1.5", "10", "dog"],
                ["2", "2.5", None, "cat"],
                ["3", "3.5", "30", "bunny"],
                ["4", "4.5", "40", "cow"],
            ],
        )

        client.append_table_data(
            id, AppendTableDataRequest(frame=frame, end_of_data=True)
        )

        # TODO: Remove mock when service supports flushing
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                f"{client.session.base_url}tables/{id}/query-data",
                json={
                    "frame": {
                        "columns": ["index", "float", "int", "string"],
                        "data": [["4", "4.5", "40", "cow"]],
                    },
                    "totalRowCount": 1,
                    "continuationToken": None,
                },
                match=[
                    matchers.json_params_matcher(
                        {
                            "filters": [
                                {
                                    "column": "float",
                                    "operation": "GREATER_THAN",
                                    "value": "1.5",
                                },
                                {
                                    "column": "int",
                                    "operation": "NOT_EQUALS",
                                    "value": None,
                                },
                                {
                                    "column": "string",
                                    "operation": "NOT_CONTAINS",
                                    "value": "bun",
                                },
                            ]
                        }
                    )
                ],
            )

            response = client.query_table_data(
                id,
                QueryTableDataRequest(
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
                    ]
                ),
            )

            assert response.frame.data == [["4", "4.5", "40", "cow"]]

    def test__query_decimated_data__works(self, client: DataFrameClient, create_table):
        id = create_table(
            CreateTableRequest(
                columns=[
                    int_index_column,
                    Column(name="col1", data_type=DataType.Float64),
                    Column(name="col2", data_type=DataType.Float64),
                ]
            )
        )

        frame = DataFrame(
            data=[
                ["1", "1.5", "3.5"],
                ["2", "2.5", "2.5"],
                ["3", "3.5", "1.5"],
                ["4", "4.5", "4.5"],
            ],
        )

        client.append_table_data(
            id, AppendTableDataRequest(frame=frame, end_of_data=True)
        )

        # TODO: Remove mock when service supports flushing
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                f"{client.session.base_url}tables/{id}/query-decimated-data",
                json={
                    "frame": {
                        "columns": ["index", "col1", "col2"],
                        "data": [["1", "1.5", "3.5"], ["4", "4.5", "4.5"]],
                    },
                },
                match=[
                    matchers.json_params_matcher(
                        {
                            "decimation": {
                                "xColumn": "index",
                                "yColumns": ["col1"],
                                "intervals": 1,
                                "method": "MAX_MIN",
                            }
                        }
                    )
                ],
            )

            response = client.query_decimated_data(
                id,
                QueryDecimatedDataRequest(
                    decimation=DecimationOptions(
                        x_column="index",
                        y_columns=["col1"],
                        intervals=1,
                        method=DecimationMethod.MaxMin,
                    )
                ),
            )

            assert response.frame.data == [["1", "1.5", "3.5"], ["4", "4.5", "4.5"]]

    def test__export_table_data__works(self, client: DataFrameClient, create_table):
        id = create_table(
            CreateTableRequest(
                columns=[
                    int_index_column,
                    Column(name="col1", data_type=DataType.Float64),
                    Column(name="col2", data_type=DataType.Float64),
                ]
            )
        )

        frame = DataFrame(
            data=[["1", "2.5", "6.5"], ["2", "1.5", "5.5"], ["3", "2.5", "7.5"]],
        )

        client.append_table_data(
            id, AppendTableDataRequest(frame=frame, end_of_data=True)
        )

        # TODO: Remove mock when service supports flushing
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                f"{client.session.base_url}tables/{id}/export-data",
                body=b'"col1","col2","col3"\r\n1,2.5,6.5\r\n2,1.5,5.5\r\n3,2.5,7.5',
                match=[matchers.json_params_matcher({"responseFormat": "CSV"})],
            )

            response = client.export_table_data(
                id,
                ExportTableDataRequest(response_format=ExportFormat.CSV),
            )

            assert (
                response.read()
                == b'"col1","col2","col3"\r\n1,2.5,6.5\r\n2,1.5,5.5\r\n3,2.5,7.5'
            )

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
