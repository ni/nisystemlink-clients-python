# -*- coding: utf-8 -*-
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
    columns = ["index", "value", "ignore_me"]
    data = [
        [1, "3.3", "True"],
        [2, "6", "False"],
        [3, "1.1", "True"],
    ]

    frame = pd.DataFrame(columns=columns, data=data)
    frame.set_index("index", inplace=True)

    return frame


@pytest.fixture(scope="class")
def create_table(client: DataFrameClient):
    """Fixture to create and delete tables in the test class."""
    tables = []

    def _create_table(df: pd.DataFrame, table_name: str, nullable_columns: bool) -> str:
        """Factory method to create tables and add to the tables list."""
        table_id = create_table_from_pandas_df(
            client, df=df, table_name=table_name, nullable_columns=nullable_columns
        )
        tables.append(table_id)
        return table_id

    yield _create_table

    client.delete_tables(tables)


@pytest.mark.enterprise
@pytest.mark.integration
class TestPandasUtility:
    def test__create_table_from_pandas_df__succeeds(
        self, client: DataFrameClient, sample_dataframe: pd.DataFrame, create_table
    ):
        table_name = "TestTable1"
        nullable_columns = True

        table_id = create_table(
            df=sample_dataframe,
            table_name=table_name,
            nullable_columns=nullable_columns,
        )

        index = None
        table_data = client.get_table_metadata(table_id)
        table_columns = table_data.columns

        for column in table_columns:
            if column.column_type == ColumnType.Index:
                index = column.name
                break

        assert table_id is not None
        assert index == "index"
        assert table_data.row_count == 0

    def test__create_table_from_pandas_df__missing_index_raises(
        self, client: DataFrameClient, create_table
    ):
        columns = ["index", "value", "ignore_me"]
        data = [
            ["1", "3.3", "True"],
            ["2", "6", "False"],
            ["3", "1.1", "True"],
        ]
        frame = pd.DataFrame(columns=columns, data=data)

        with pytest.raises(
            InvalidIndexError, match="Data frame must contain one index."
        ):
            create_table(df=frame, table_name="TestTable2", nullable_columns=True)

    def test__append_pandas_df_to_table__succeeds(
        self, client: DataFrameClient, sample_dataframe, create_table
    ):

        id = create_table(
            df=sample_dataframe, table_name="TestTable3", nullable_columns=False
        )

        append_pandas_df_to_table(client=client, table_id=id, df=sample_dataframe)

        response = client.get_table_data(id)

        assert response.total_row_count == 3

    def test__append_pandas_df_to_table__raises(
        self, client: DataFrameClient, sample_dataframe, create_table
    ):
        id = create_table(
            df=sample_dataframe, table_name="TestTable3", nullable_columns=True
        )

        frame = pd.DataFrame(
            columns=["index", "non_existent_column"],
            data=[["1", "2"], ["2", "2"], ["3", "3"]],
        )

        with pytest.raises(ApiException, match="400 Bad Request"):
            append_pandas_df_to_table(client=client, table_id=id, df=frame)

    def test__query_table_data_as_pandas_df__sorted_query_succeeds(
        self, client: DataFrameClient, sample_dataframe, create_table
    ):
        table_name = "TestTable4"
        nullable_columns = True
        id = create_table(
            sample_dataframe, table_name, nullable_columns=nullable_columns
        )
        append_pandas_df_to_table(client, table_id=id, df=sample_dataframe)
        client.get_table_metadata(id=id)

        response = query_table_data_as_pandas_df(
            client,
            table_id=id,
            query=QueryTableDataRequest(
                columns=["value", "ignore_me"],
                order_by=[ColumnOrderBy(column="value", descending=True)],
            ),
            index=True,
        )

        data = [
            [2, "6", "False"],
            [1, "3.3", "True"],
            [3, "1.1", "True"],
        ]
        columns = ["index", "value", "ignore_me"]
        expected_df = pd.DataFrame(columns=columns, data=data)
        expected_df.set_index("index", inplace=True)

        assert (
            (response.reset_index(drop=True) == expected_df.reset_index(drop=True))
            .all()
            .all()
        )

    def test__query_decimated_table_data_as_pandas_df__succeeds(
        self, client: DataFrameClient, create_table
    ):
        table_name = "TestTable5"
        nullable_columns = True

        data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        columns = ["a", "b", "c"]
        frame = pd.DataFrame(data=data, columns=columns)
        frame.set_index("a", inplace=True)

        id = create_table(
            df=frame, table_name=table_name, nullable_columns=nullable_columns
        )

        append_pandas_df_to_table(client, table_id=id, df=frame)

        response: pd.DataFrame = query_decimated_table_data_as_pandas_df(
            client,
            table_id=id,
            query=QueryDecimatedDataRequest(
                decimation=DecimationOptions(
                    x_column="a",
                    y_columns=["b"],
                    intervals=1,
                    method=DecimationMethod.MaxMin,
                )
            ),
            index=True,
        )
        data = [
            ["1", "2", "3"],
            ["7", "8", "9"],
        ]
        columns = ["a", "b", "c"]
        expected_df = pd.DataFrame(data=data, columns=columns)
        expected_df.set_index("a", inplace=True)

        assert (response.values == expected_df.values).all()
