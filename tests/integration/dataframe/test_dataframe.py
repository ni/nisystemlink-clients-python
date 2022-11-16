# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe import models


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a DataFrameClient instance."""
    return DataFrameClient(enterprise_config)


@pytest.fixture(scope="class")
def create_table(client: DataFrameClient):
    """Fixture to return a factory that creates tables."""
    tables = []

    def _create_table(table: models.CreateTableRequest) -> str:
        id = client.create_table(table)
        print(f"Created table {id}")
        tables.append(id)
        return id

    yield _create_table

    for id in tables:
        client.delete_table(id)
        print(f"Deleted table {id}")


@pytest.fixture(scope="class")
def test_tables(create_table):
    """Fixture to create a set of test tables."""
    ids = []
    for i in range(1, 4):
        ids.append(
            create_table(
                models.CreateTableRequest(
                    columns=[
                        models.Column(
                            name="time",
                            data_type=models.DataType.Timestamp,
                            column_type=models.ColumnType.Index,
                            properties={"cat": "meow"},
                        ),
                        models.Column(name="value", data_type=models.DataType.Int32),
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
    def test__api_info__returns(self, client):
        response = client.api_info()

        assert len(response.dict()) != 0

    def test__create_table__metadata_is_corect(
        self, client: DataFrameClient, test_tables: List[str]
    ):
        table_metadata = client.get_table_metadata(test_tables[0])

        assert table_metadata.name == "Python API test table 1 (delete me)"
        assert table_metadata.properties == {"dog": "woof"}
        assert table_metadata.columns == [
            models.Column(
                name="time",
                data_type=models.DataType.Timestamp,
                column_type=models.ColumnType.Index,
                properties={"cat": "meow"},
            ),
            models.Column(
                name="value",
                data_type=models.DataType.Int32,
                column_type=models.ColumnType.Normal,
                properties={},
            ),
        ]

    def test__get_table__correct_timestamp(self, client: DataFrameClient, create_table):
        id = create_table(
            models.CreateTableRequest(
                columns=[
                    models.Column(
                        name="index",
                        data_type=models.DataType.Int32,
                        column_type=models.ColumnType.Index,
                    )
                ]
            )
        )
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
        take = len(test_tables) - 1
        first_page = client.list_tables(
            take=take,
            id=test_tables,
            order_by="NAME",
            order_by_descending=True,
        )

        assert len(first_page.tables) == take
        assert first_page.tables[0].id == test_tables[-1]  # Asserts descending order
        assert first_page.continuation_token is not None

        second_page = client.list_tables(
            id=test_tables,
            order_by="NAME",
            order_by_descending=True,
            continuation_token=first_page.continuation_token,
        )

        assert len(second_page.tables) == 1
        assert second_page.continuation_token is None
