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
    """A set of test methods to test SystemLink Auth API."""

    def test__authenticate_returns(self, client: AuthClient):
        """Test the case of getting caller information with SystemLink Credentials."""
        response = client.authenticate()
        assert response is not None
