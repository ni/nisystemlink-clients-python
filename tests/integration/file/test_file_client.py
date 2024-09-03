"""Integration tests for FileClient."""

import io
import string
from random import choices, randint
from typing import BinaryIO

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import DeleteMutipleRequest
from nisystemlink.clients.file.utilities import get_file_id_from_uri

FILE_NOT_FOUND_ERR = "Not Found"
TEST_FILE_DATA = b"This is a test file binary content."
TEST_FILE_NAME = "Test File.bin"


@pytest.fixture(scope="class")
def client(enterprise_config) -> FileClient:
    """Fixture to create a FileClient instance."""
    return FileClient(enterprise_config)


@pytest.fixture(scope="class")
def binary_file_data() -> BinaryIO:
    """Test Binary file content."""
    return io.BytesIO(TEST_FILE_DATA)


@pytest.fixture(scope="class")
def test_file(client: FileClient):
    """Fixture to return a factory that uploads a file."""
    file_ids = []

    def _test_file(file_name: str = TEST_FILE_NAME, cleanup: bool = True) -> str:
        test_file = io.BytesIO(TEST_FILE_DATA)
        test_file.name = file_name
        file_info = client.upload_file(file=test_file)
        file_id = get_file_id_from_uri(file_info.uri)
        if cleanup:
            file_ids.append(file_id)
        return file_id

    yield _test_file

    if file_ids:
        _delete_files = DeleteMutipleRequest(ids=file_ids)
        client.delete_files(files=_delete_files, force=True)


@pytest.fixture(scope="class")
def invalid_file_id(client: FileClient) -> str:
    """Generate a invalid file id."""
    MAX_RETRIES = 10
    attempts = 0

    while attempts < MAX_RETRIES:
        file_id = f"Invalid-File-Id-{randint(1000,9999)}"
        files = client.get_files(file_ids=file_id)
        if files.total_count == 0:
            return file_id

    raise Exception(f"Failed to generate a invalid-file-id in {MAX_RETRIES} attemps.")


@pytest.mark.enterprise
@pytest.mark.integration
class TestFileClient:
    def test__api_info__returns(self, client: FileClient):
        api_info = client.api_info()
        assert len(api_info.dict()) != 0

    def test__upload_get_delete_files__succeeds(self, client: FileClient, test_file):
        # upload a file
        file_id = test_file(cleanup=False)
        assert file_id != ""

        files = client.get_files(file_ids=file_id)
        assert files.total_count == 1
        assert len(files.available_files) == 1
        assert files.available_files[0].id == file_id

        client.delete_file(file_id=file_id, force=True)

        # confirm that file was deleted
        files = client.get_files(file_ids=file_id)
        assert files.total_count == 0

    def test__delete_file__invalid_id_raises(
        self, client: FileClient, invalid_file_id: str
    ):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.delete_file(file_id=invalid_file_id, force=True)

    def test__delete_files__succeeds(self, client: FileClient, test_file):
        # upload 5 files and delete them
        NUM_FILES = 5

        file_ids = [test_file(cleanup=False) for _ in range(NUM_FILES)]

        file_ids_str = ",".join(file_ids)

        # confirm that files exist
        files = client.get_files(file_ids=file_ids_str)
        assert files.total_count == NUM_FILES

        _delete_files = DeleteMutipleRequest(ids=file_ids)
        client.delete_files(files=_delete_files, force=True)

        # confirm that files were deleted
        files = client.get_files(file_ids=file_ids_str)
        assert files.total_count == 0

    def test__download_file__invalid_id_raises(
        self, client: FileClient, invalid_file_id: str
    ):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.download_file(file_id=invalid_file_id)

    def test__download_file__succeeds(
        self, client: FileClient, test_file, binary_file_data
    ):
        # generate a random file name and extension
        rand_file_name = "".join(choices(string.ascii_letters + string.digits, k=10))
        rand_file_extn = "".join(choices(string.ascii_letters, k=3))

        full_file_name = f"{rand_file_name}.{rand_file_extn}"

        # Upload the test file with random name
        file_id = test_file(file_name=full_file_name)

        # verify the File Name and extension
        files = client.get_files(file_ids=file_id)
        assert len(files.available_files) == 1
        assert files.available_files[0].properties is not None
        assert files.available_files[0].properties["Name"] == full_file_name

        # verify the file content
        data = client.download_file(file_id=file_id)
        file_content = data.read()
        assert file_content == binary_file_data.read()
