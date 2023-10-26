from copy import copy

import pytest  # type: ignore
from nisystemlink.clients.auth import AuthClient


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a AuthClient instance."""
    return AuthClient(enterprise_config)


@pytest.fixture(scope="class")
def invalid_client(enterprise_config):
    """Fixture to create a invalid AuthClient instance (invalid API Key)."""
    invalid_enterprise_config = copy(enterprise_config)
    invalid_enterprise_config.api_key = "abcdef1234"
    return AuthClient(invalid_enterprise_config)


@pytest.mark.enterprise
@pytest.mark.integration
class TestAuth:
    def test__get_auth__returns(self, client: AuthClient):
        auth_response = client.get_auth()
        assert getattr(auth_response, "error") is None
        assert len(auth_response.workspaces) >= 1

    def test__get_auth__errors(self, invalid_client: AuthClient):
        auth_response = invalid_client.get_auth()
        assert getattr(auth_response, "workspaces") is None
        assert getattr(auth_response, "error") is not None
