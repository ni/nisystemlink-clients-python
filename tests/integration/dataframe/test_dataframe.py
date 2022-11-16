# -*- coding: utf-8 -*-
from typing import Iterator

import pytest  # type: ignore
from nisystemlink.clients.dataframe import DataFrameClient
from nisystemlink.clients.dataframe import models


@pytest.mark.enterprise
@pytest.mark.integration
class TestDataFrame:
    @pytest.fixture
    def client(self, enterprise_config):
        return DataFrameClient(enterprise_config)

    @pytest.fixture
    def table_id(self, client: DataFrameClient) -> Iterator[str]:
        id = client.create_table(
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
                name="Python API test table (delete me)",
                properties={"dog": "woof"},
            )
        )
        yield id
        client.delete_table(id)

    def test__api_info__returns(self, client):
        response = client.api_info()

        assert len(response.dict()) != 0

    def test__create_table__metadata_is_corect(
        self, client: DataFrameClient, table_id: str
    ):
        table_metadata = client.get_table_metadata(table_id)

        assert table_metadata.name == "Python API test table (delete me)"
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
