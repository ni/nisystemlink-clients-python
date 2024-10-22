"""Integration tests for AuthClient."""

import pytest  # type: ignore
from nisystemlink.clients.auth import AuthClient


@pytest.fixture(scope="class")
def client(enterprise_config) -> AuthClient:
    """Fixture to create a AuthClient instance."""
    return AuthClient(enterprise_config)


@pytest.mark.enterprise
@pytest.mark.integration
class TestAuthClient:
    def test__authenticate(self, client: AuthClient):
        response = client.authenticate()
        assert response is not None
