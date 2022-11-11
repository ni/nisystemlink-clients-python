# -*- coding: utf-8 -*-

import pytest  # type: ignore
from nisystemlink.clients.dataframe import DataFrameClient


@pytest.mark.enterprise
@pytest.mark.integration
class TestDataFrame:
    def test__api_info__returns(self, enterprise_config):
        client = DataFrameClient(enterprise_config)

        response = client.api_info()

        assert len(response) != 0
