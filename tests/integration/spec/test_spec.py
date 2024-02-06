import pytest

from nisystemlink.clients.core._http_configuration import HttpConfiguration
from nisystemlink.clients.spec import SpecClient


@pytest.fixture(scope="class")
def client(enterprise_config: HttpConfiguration):
    """Fixture ot create a SpecClient instance."""
    return SpecClient(enterprise_config)


@pytest.mark.integration
@pytest.mark.enterprise
class TestSpec:
    def test__api_info__returns(self, client):
        response = client.api_info()
        assert len(response.dict()) != 0
