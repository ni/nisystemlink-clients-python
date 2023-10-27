import pytest  # type: ignore
from typing import List
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.webapp import WebappClient
from nisystemlink.clients.webapp.models import WebAppsAdvancedQuery


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a WebappClient instance."""
    return WebappClient(enterprise_config)


@pytest.fixture(scope="class")
def test_webapps(client: WebappClient) -> List[str]:
    """Fixture to return the pre-created WebApp IDs for testing."""
    webapp_ids = [
        "0c5b1fab-1c21-4559-89d9-9f3b02e301f4",  # 'ADC' dataspace
        "8c5e4eb0-4f24-4704-a886-7e7352637322",  # 'CS_STDF_T2KFT' dataspace
    ]
    return webapp_ids


@pytest.mark.enterprise
@pytest.mark.integration
class TestAuth:
    def test__get_content__invalid_id_raises(self, client: WebappClient):
        with pytest.raises(ApiException, match="Not Found"):
            client.get_content(id="invalid id")

    def test__get_content__returns(self, client: WebappClient, test_webapps):
        content = client.get_content(id=test_webapps[0])  # check for only one webapp
        assert content is not None

    def test__query_webapps__returns(self, client: WebappClient, test_webapps):
        id_fitler = " || ".join([f'id == "{webapp_id}"' for webapp_id in test_webapps])

        query = WebAppsAdvancedQuery(
            filter=id_fitler, take=1
        )  # test continuation tokens
        webapps = []

        while True:
            resp = client.query_webapps(query=query)
            webapps += resp.webapps
            query.continuation_token = resp.continuation_token
            if resp.continuation_token is None:
                break

        assert len(webapps) == len(test_webapps)
