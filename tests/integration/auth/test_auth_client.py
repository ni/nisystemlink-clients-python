"""Integration tests for AuthClient."""

import pytest
from nisystemlink.clients.auth import AuthClient


@pytest.fixture(scope="class")
def client(enterprise_config) -> AuthClient:
    """Fixture to create a AuthClient instance."""
    return AuthClient(enterprise_config)


@pytest.mark.enterprise
@pytest.mark.integration
class TestAuthClient:
    def test__get_auth_info__succeeds(self, client: AuthClient):
        """Test the case of getting caller information with SystemLink Credentials."""
        response = client.get_auth_info()
        assert response is not None
