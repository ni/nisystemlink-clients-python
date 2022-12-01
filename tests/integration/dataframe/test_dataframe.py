# -*- coding: utf-8 -*-
from datetime import datetime, timezone
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
        query = models.QueryTablesRequest(
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

        client.modify_table(
            id,
            models.ModifyTableRequest(
                metadata_revision=2,
                name="Modified table",
                properties={"cow": "moo"},
                columns=[
                    models.ColumnMetadataPatch(
                        name="index", properties={"sheep": "baa"}
                    )
                ],
            ),
        )
        table = client.get_table_metadata(id)

        assert table.metadata_revision == 2
        assert table.name == "Modified table"
        assert table.properties == {"cow": "moo"}
        assert table.columns[0].properties == {"sheep": "baa"}

        client.modify_table(id, models.ModifyTableRequest(properties={"bee": "buzz"}))
        table = client.get_table_metadata(id)

        assert table.properties == {"cow": "moo", "bee": "buzz"}
        assert table.name == "Modified table"

        client.modify_table(
            id,
            models.ModifyTableRequest(
                metadata_revision=4,
                name=None,
                properties={"cow": None},
                columns=[
                    models.ColumnMetadataPatch(name="index", properties={"sheep": None})
                ],
            ),
        )
        table = client.get_table_metadata(id)

        assert table.metadata_revision == 4
        assert table.name == id
        assert table.properties == {"bee": "buzz"}
        assert table.columns[0].properties == {}

    def test__delete_table__deletes(self, client: DataFrameClient):
        id = client.create_table(  # Don't use fixture to avoid deleting the table twice
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

        assert client.delete_table(id) is None

        with pytest.raises(ApiException, match="404 Not Found"):
            client.get_table_metadata(id)

    def test__delete_tables__deletes(self, client: DataFrameClient):
        ids = [
            client.create_table(
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
            for _ in range(3)
        ]

        assert client.delete_tables(ids) is None

        assert client.list_tables(id=ids).tables == []

    def test__delete_tables__returns_partial_success(self, client: DataFrameClient):
        id = client.create_table(
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

        response = client.delete_tables([id, "invalid_id"])

        assert response is not None
        assert response.deleted_table_ids == [id]
        assert response.failed_table_ids == ["invalid_id"]
        assert len(response.error.inner_errors) == 1
