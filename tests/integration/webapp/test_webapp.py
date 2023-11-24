from typing import List

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.webapp import WebappClient
from nisystemlink.clients.webapp.models import WebApp, WebAppsAdvancedQuery


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a WebappClient instance."""
    return WebappClient(enterprise_config)


@pytest.fixture(scope="class")
def test_webapps(client: WebappClient) -> List[str]:
    """Fixture to return the pre-created WebApp IDs for testing."""
    webapp_ids = [
        "452bc11b-6a8a-4c3e-8eb1-721270157eb8",  # 'PyAPI_Test1' dataspace
        "0345a956-3747-42e1-9296-6ed06545bd0d",  # 'PyAPI_Test2' dataspace
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
        webapps: List[WebApp] = []

        while True:
            resp = client.query_webapps(query=query)
            if resp.webapps:
                webapps += resp.webapps
            query.continuation_token = resp.continuation_token
            if resp.continuation_token is None:
                break

        assert len(webapps) == len(test_webapps)
