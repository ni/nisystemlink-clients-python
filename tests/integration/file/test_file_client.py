import io

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.file import FileClient


@pytest.fixture(scope="class")
def client(enterprise_config) -> FileClient:
    """Fixture to create a FileClient instance."""
    return FileClient(enterprise_config)


@pytest.fixture(scope="class")
def binary_file() -> io.BytesIO:
    """Fixture to create a binary file as file pointer object."""
    return io.BytesIO(b"123abc")


@pytest.mark.enterprise
@pytest.mark.integration
class TestFileClient:
    def test__api_info__returns(self, client: FileClient):
        api_info = client.api_info()
        assert len(api_info.dict()) != 0

    def test__download_file__succeeds(self, client: FileClient):
        client.download_file(id="45ab28ba-29a7-4d0e-9522-cc4c6cf100bf")
        # with open(f"test_file.pdf", "wb") as f:
        #     copyfileobj(data, f)

    def test__download_file__invalid_id_raises(self, client: FileClient):
        with pytest.raises(ApiException, match="Not Found"):
            client.download_file(id="Invalid ID")
