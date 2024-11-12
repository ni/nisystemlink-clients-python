import pandas as pd
import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe.models import (
    ColumnOrderBy,
    ColumnType,
    DecimationMethod,
    DecimationOptions,
    QueryDecimatedDataRequest,
    QueryTableDataRequest,
)
from nisystemlink.clients.dataframe.utilities import (
    append_pandas_df_to_table,
    create_table_from_pandas_df,
    InvalidIndexError,
    query_decimated_table_data_as_pandas_df,
    query_table_data_as_pandas_df,
)


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a DataFrameClient instance."""
    return DataFrameClient(enterprise_config)


@pytest.fixture(scope="class")
def sample_dataframe():
    """Fixture for a sample pandas DataFrame."""
    frame = pd.DataFrame(
        columns=["index", "value", "ignore_me"],
        data=[[1, "3.3", "True"], [2, "6", "False"], [3, "1.1", "True"]],
    )
    frame.set_index("index", inplace=True)
    return frame


@pytest.fixture(scope="class")
def create_table(client: DataFrameClient):
    """Fixture to create and delete tables in the test class."""
    tables = []  # List to keep track of created table IDs

    def _create_table(df: pd.DataFrame, table_name: str, nullable_columns: bool) -> str:
        """Factory method to create tables and add to the tables list."""
        table_id = create_table_from_pandas_df(
            client, df=df, table_name=table_name, nullable_columns=nullable_columns
        )
        tables.append(table_id)
        return table_id

    yield _create_table

    if tables:
        client.delete_tables(tables)


@pytest.mark.enterprise
@pytest.mark.integration
class TestPandasUtility:
    def test_create_table_from_pandas_df(
        self, client: DataFrameClient, sample_dataframe: pd.DataFrame, create_table
    ):
        table_name = "TestTable"
        nullable_columns = True
        table_id = create_table(
            df=sample_dataframe,
            table_name=table_name,
            nullable_columns=nullable_columns,
        )

        index = None
        table_columns = client.get_table_metadata(table_id).columns
        for column in table_columns:
            if column.column_type == ColumnType.Index:
                index = column.name
                break

        assert table_id is not None
        assert index is not None
        assert index == "index"

    def test__append_data__works(
        self, client: DataFrameClient, sample_dataframe, create_table
    ):

        id = create_table(
            df=sample_dataframe, table_name="Test", nullable_columns=False
        )

        append_pandas_df_to_table(client=client, table_id=id, df=sample_dataframe)

        response = client.get_table_data(id)

        assert response.total_row_count == 3

    def test__write_invalid_data__raises(
        client: DataFrameClient, sample_dataframe, create_table
    ):
        id = create_table(
            df=sample_dataframe, table_name="TestTable", nullable_columns=True
        )

        frame = pd.DataFrame(
            columns=["index", "non_existent_column"],
            data=[["1", "2"], ["2", "2"], ["3", "3"]],
        )

        with pytest.raises(ApiException, match="400 Bad Request"):
            append_pandas_df_to_table(client=client, table_id=id, df=frame)

    def test__create_table_with_missing_index__raises(
        self, client: DataFrameClient, create_table
    ):

        frame = pd.DataFrame(
            columns=["index", "value", "ignore_me"],
            data=[["1", "3.3", "True"], ["2", "6", "False"], ["3", "1.1", "True"]],
        )

        with pytest.raises(
            InvalidIndexError, match="Data frame must contain one index."
        ):
            create_table(df=frame, table_name="TestTable", nullable_columns=True)

    def test__query_table_data__sorts(
        self, client: DataFrameClient, sample_dataframe, create_table
    ):
        table_name = "TestTable"
        nullable_columns = True
        id = create_table(
            sample_dataframe, table_name, nullable_columns=nullable_columns
        )

        frame = pd.DataFrame(
            data=[[1, "2.5", "True"], [2, "1.5", "False"], [3, "2.5", "True"]],
            columns=["index", "value", "ignore_me"],
        )

        append_pandas_df_to_table(client, table_id=id, df=frame)

        response = query_table_data_as_pandas_df(
            client,
            table_id=id,
            query=QueryTableDataRequest(
                order_by=[
                    ColumnOrderBy(column="value", descending=True),
                    ColumnOrderBy(column="ignore_me"),
                ]
            ),
            index=True,
        )
        expected_df = pd.DataFrame(
            data=[[2, "1.5", "False"], [3, "2.5", "True"], [1, "2.5", "True"]],
            columns=["index", "value", "ignore_me"],
        )
        expected_df.set_index("index", inplace=True)

        assert response == expected_df

    def test__query_decimated_data__works(self, client: DataFrameClient, create_table):
        table_name = "TestTable"
        nullable_columns = True

        frame = pd.DataFrame(
            data=[
                [1, 1.5, 3.5],
                [2, 2.5, 2.5],
                [3, 3.5, 1.5],
                [4, 4.5, 4.5],
            ],
            columns=["index", "col1", "col2"],
        )
        frame.set_index("index", inplace=True)
        id = create_table(
            df=frame, table_name=table_name, nullable_columns=nullable_columns
        )

        append_pandas_df_to_table(client, table_id=id, df=frame)

        response = query_decimated_table_data_as_pandas_df(
            client,
            table_id=id,
            query=QueryDecimatedDataRequest(
                decimation=DecimationOptions(
                    x_column="index",
                    y_columns=["col1"],
                    intervals=1,
                    method=DecimationMethod.MaxMin,
                )
            ),
            index=True,
        )

        assert response == pd.DataFrame(
            data=[[1.5, 3.5], [4.5, 4.5]], columns=frame.columns, index=[1, 4]
        )
