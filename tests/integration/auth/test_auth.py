import pytest  # type: ignore
from nisystemlink.clients.auth import AuthClient


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Fixture to create a AuthClient instance."""
    return AuthClient(enterprise_config)


@pytest.mark.enterprise
@pytest.mark.integration
class TestAuth:
    def test__get_auth__returns(self, client: AuthClient):
        auth_response = client.get_auth()
        assert getattr(auth_response, "error") is None
        assert len(auth_response.workspaces) >= 1
