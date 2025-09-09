import itertools
from typing import Iterable, List, Optional

from nisystemlink.clients.dataframe.models._column import Column
from nisystemlink.clients.dataframe.models._column_type import ColumnType
from nisystemlink.clients.dataframe.models._create_table_request import CreateTableRequest
from nisystemlink.clients.dataframe.models._data_type import DataType
import pytest  # type: ignore
import responses
from responses import matchers

from nisystemlink.clients.core import ApiException
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import AppendTableDataRequest, DataFrame

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

    def _create_table(table: Optional[CreateTableRequest] = None) -> str:
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
def test__append_table_data__append_request_success(
    client: DataFrameClient, test_tables: List[str]
):
    frame = DataFrame(data=[["1"], ["2"]])
    request = AppendTableDataRequest(frame=frame, end_of_data=True)
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            match=[
                matchers.json_params_matcher(
                    {"frame": {"data": [["1"], ["2"]]}, "endOfData": True}
                )
            ],
            json={},
        )
        client.append_table_data(test_tables[0], request)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__append_request_with_end_of_data_argument_disallowed(
    client: DataFrameClient, test_tables: List[str]
):
    request = AppendTableDataRequest(end_of_data=True)
    with pytest.raises(ValueError, match="end_of_data must not be provided separately when passing an AppendTableDataRequest."):
        client.append_table_data(test_tables[0], request, end_of_data=True)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__accepts_dataframe_model(client: DataFrameClient, test_tables: List[str]):
    frame = DataFrame(data=[["1"], ["2"]])
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            match=[
                matchers.json_params_matcher(
                    {"frame": {"data": [["1"], ["2"]]}, "endOfData": True}
                )
            ],
            json={},
        )
        assert (
            client.append_table_data(test_tables[0], frame, end_of_data=True) is None
        )

@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__dataframe_without_end_of_data_success(
    client: DataFrameClient, test_tables: List[str]
):
    frame = DataFrame(data=[["10"], ["11"]])
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            json={},
        )
        client.append_table_data(test_tables[0], frame)  # no end_of_data


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__none_without_end_of_data_raises(
    client: DataFrameClient, test_tables: List[str]
):
    with pytest.raises(ValueError, match="end_of_data must be provided when data is None"):
        client.append_table_data(test_tables[0], None)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__flush_only_with_none(client: DataFrameClient, test_tables: List[str]):
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            match=[matchers.json_params_matcher({"endOfData": True})],
            json={},
        )
        client.append_table_data(test_tables[0], None, end_of_data=True)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__empty_iterator_requires_end_of_data(client: DataFrameClient, test_tables: List[str]):
    # No end_of_data -> ValueError
    with pytest.raises(ValueError, match="end_of_data must be provided when data iterator is empty."):
        client.append_table_data(test_tables[0], [])

    # With end_of_data -> sends JSON flush only
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            match=[matchers.json_params_matcher({"endOfData": True})],
            json={},
        )
        client.append_table_data(test_tables[0], [], end_of_data=True)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_iterable_without_pyarrow_raises_runtime_error(
    client: DataFrameClient, test_tables: List[str], monkeypatch
):
    # Simulate pyarrow not installed by setting module-level pa to None
    import nisystemlink.clients.dataframe._data_frame_client as df_module

    monkeypatch.setattr(df_module, "pa", None)

    with pytest.raises(RuntimeError, match="pyarrow is not installed. Install to stream RecordBatches."):
        client.append_table_data(test_tables[0], [object()])


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_iterable_with_non_recordbatch_elements_raises(
    client: DataFrameClient, test_tables: List[str]
):
    pytest.importorskip("pyarrow")
    # Pass a list whose first element is not a RecordBatch -> should raise ValueError
    with pytest.raises(ValueError, match="Iterable provided to data must yield pyarrow.RecordBatch objects."):
        client.append_table_data(test_tables[0], [1, 2, 3])


def _arrow_record_batches() -> Iterable["pa.RecordBatch"]:  # type: ignore[name-defined]
    import pyarrow as pa  # type: ignore

    batch = pa.record_batch([pa.array([1, 2, 3])], names=["a"])
    return [batch]


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_ingestion_400_wrapped_error(client: DataFrameClient, test_tables: List[str]):
    pa = pytest.importorskip("pyarrow")  # noqa: F841

    with responses.RequestsMock() as rsps:
        # Mock api_info indicating writeData version 1 (no Arrow support)
        rsps.add(
            responses.GET,
            f"{client.session.base_url}",
            json={
                "operations": {
                    "createTables": {"available": True, "version": 1},
                    "deleteTables": {"available": True, "version": 1},
                    "modifyMetadata": {"available": True, "version": 1},
                    "listTables": {"available": True, "version": 1},
                    "readData": {"available": True, "version": 1},
                    "writeData": {"available": True, "version": 1},
                }
            },
        )
        def _callback(request):  # type: ignore
            return (400, {}, "")

        rsps.add_callback(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            callback=_callback,
            content_type="application/vnd.apache.arrow.stream",
        )

        with pytest.raises(ApiException, match="Arrow ingestion request was rejected"):
            client.append_table_data(test_tables[0], _arrow_record_batches())


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_ingestion_400_not_wrapped_when_version2(
    client: DataFrameClient, test_tables: List[str]
):
    pa = pytest.importorskip("pyarrow")  # noqa: F841

    with responses.RequestsMock() as rsps:
        # Mock api_info indicating writeData version 2 (Arrow support); expect original 400 (no friendly message)
        rsps.add(
            responses.GET,
            f"{client.session.base_url}",
            json={
                "operations": {
                    "createTables": {"available": True, "version": 1},
                    "deleteTables": {"available": True, "version": 1},
                    "modifyMetadata": {"available": True, "version": 1},
                    "listTables": {"available": True, "version": 1},
                    "readData": {"available": True, "version": 1},
                    "writeData": {"available": True, "version": 2},
                }
            },
        )

        def _callback(request):  # type: ignore
            return (400, {}, "")

        rsps.add_callback(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            callback=_callback,
            content_type="application/vnd.apache.arrow.stream",
        )

        with pytest.raises(ApiException) as excinfo:
            client.append_table_data(test_tables[0], _arrow_record_batches())
        # Ensure friendly message NOT used
        assert "doesn't support Arrow streaming" not in str(excinfo.value)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_ingestion_400_api_info_failure_wrapped(
    client: DataFrameClient, test_tables: List[str]
):
    pa = pytest.importorskip("pyarrow")  # noqa: F841

    with responses.RequestsMock() as rsps:
        # Simulate api_info failure (500) so fallback wrapping should occur
        rsps.add(
            responses.GET,
            f"{client.session.base_url}",
            status=500,
            json={"error": "server error"},
        )

        def _callback(request):  # type: ignore
            return (400, {}, "")

        rsps.add_callback(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            callback=_callback,
            content_type="application/vnd.apache.arrow.stream",
        )

        with pytest.raises(ApiException, match="Arrow ingestion request was rejected"):
            client.append_table_data(test_tables[0], _arrow_record_batches())


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_ingestion_non_400_error_passthrough(
    client: DataFrameClient, test_tables: List[str]
):
    pa = pytest.importorskip("pyarrow")  # noqa: F841

    with responses.RequestsMock() as rsps:
        def _callback(request):  # type: ignore
            return (415, {}, "")  # Unsupported Media Type

        rsps.add_callback(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            callback=_callback,
            content_type="application/vnd.apache.arrow.stream",
        )

        with pytest.raises(ApiException) as excinfo:
            client.append_table_data(test_tables[0], _arrow_record_batches())
        assert "doesn't support Arrow streaming" not in str(excinfo.value)
        assert "415" in str(excinfo.value)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_ingestion_with_end_of_data_query_param(
    client: DataFrameClient, test_tables: List[str]
):
    pa = pytest.importorskip("pyarrow")  # noqa: F841

    with responses.RequestsMock() as rsps:
        def _callback(request):  # type: ignore
            url = request.url.lower()
            # Allow either endOfData or end_of_data just in case
            assert ("endofdata=true" in url) or ("end_of_data=true" in url)
            return (200, {}, "")

        rsps.add_callback(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            callback=_callback,
            content_type="application/vnd.apache.arrow.stream",
        )

        client.append_table_data(test_tables[0], _arrow_record_batches(), end_of_data=True)


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__arrow_ingestion_success(client: DataFrameClient, test_tables: List[str]):
    pa = pytest.importorskip("pyarrow")  # noqa: F841

    with responses.RequestsMock() as rsps:
        # Use callback to assert content-type header (can't easily JSON match binary stream)
        def _callback(request):  # type: ignore
            assert (
                request.headers.get("Content-Type")
                == "application/vnd.apache.arrow.stream"
            )
            return (200, {}, "")

        rsps.add_callback(
            responses.POST,
            f"{client.session.base_url}tables/{test_tables[0]}/data",
            callback=_callback,
            content_type="application/vnd.apache.arrow.stream",
        )

        # Provide iterator of record batches
        client.append_table_data(test_tables[0], _arrow_record_batches())


@pytest.mark.enterprise
@pytest.mark.integration
def test__append_table_data__unsupported_type_raises(client: DataFrameClient, test_tables: List[str]):
    with pytest.raises(ValueError, match="Unsupported type"):
        client.append_table_data(test_tables[0], 123)  # type: ignore[arg-type]
