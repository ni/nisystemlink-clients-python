"""Integration tests for FileClient."""

import io
import string
from random import choices, randint
from typing import BinaryIO

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import UpdateMetadataRequest
from nisystemlink.clients.file.utilities import rename_file

FILE_NOT_FOUND_ERR = "Not Found"
PREFIX = "File Client Tests-"
TEST_FILE_DATA = b"This is a test file binary content."
TEST_FILE_NAME = f"{PREFIX}Test File.bin"


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
        file_id = client.upload_file(file=test_file)
        if cleanup:
            file_ids.append(file_id)
        return file_id

    yield _test_file

    if file_ids:
        client.delete_files(ids=file_ids, force=True)


@pytest.fixture(scope="class")
def invalid_file_id(client: FileClient) -> str:
    """Generate a invalid file id."""
    MAX_RETRIES = 10
    attempts = 0

    while attempts < MAX_RETRIES:
        file_id = f"Invalid-File-Id-{randint(1000,9999)}"
        files = client.get_files(ids=[file_id])
        if files.total_count == 0:
            return file_id

    raise Exception(f"Failed to generate a invalid-file-id in {MAX_RETRIES} attemps.")


@pytest.fixture(scope="class")
def random_filename_extn() -> str:
    """Generate a random filename and extension."""
    rand_file_name = "".join(choices(string.ascii_letters + string.digits, k=10))
    rand_file_extn = "".join(choices(string.ascii_letters, k=3))

    return f"{PREFIX}{rand_file_name}.{rand_file_extn}"


@pytest.mark.enterprise
@pytest.mark.integration
class TestFileClient:
    def test__api_info__returns(self, client: FileClient):
        api_info = client.api_info()
        assert len(api_info.dict()) != 0

    def test__upload_get_delete_files__succeeds(
        self, client: FileClient, test_file, random_filename_extn
    ):
        # upload a file
        file_id = test_file(file_name=random_filename_extn, cleanup=False)
        assert file_id != ""

        files = client.get_files(ids=[file_id])
        assert files.total_count == 1
        assert len(files.available_files) == 1
        assert files.available_files[0].id == file_id
        assert files.available_files[0].properties is not None
        assert files.available_files[0].properties["Name"] == random_filename_extn

        client.delete_file(id=file_id, force=True)

        # confirm that file was deleted
        files = client.get_files(ids=[file_id])
        assert files.total_count == 0

    def test__delete_file__invalid_id_raises(
        self, client: FileClient, invalid_file_id: str
    ):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.delete_file(id=invalid_file_id, force=True)

    def test__delete_files__succeeds(self, client: FileClient, test_file):
        # upload 2 files and delete them
        NUM_FILES = 2

        file_ids = [test_file(cleanup=False) for _ in range(NUM_FILES)]

        # confirm that files exist
        files = client.get_files(ids=file_ids)
        assert files.total_count == NUM_FILES

        client.delete_files(ids=file_ids, force=True)

        # confirm that files were deleted
        files = client.get_files(ids=file_ids)
        assert files.total_count == 0

    def test__download_file__invalid_id_raises(
        self, client: FileClient, invalid_file_id: str
    ):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.download_file(id=invalid_file_id)

    def test__download_file__succeeds(
        self,
        client: FileClient,
        test_file,
        binary_file_data: BinaryIO,
        random_filename_extn: str,
    ):
        # Upload the test file with random name
        file_id = test_file(file_name=random_filename_extn)

        # verify the file content
        downloaded_data = client.download_file(id=file_id)
        assert downloaded_data.read() == binary_file_data.read()

    def test__update_metadata__rename_utility_succeeds(
        self, client: FileClient, test_file
    ):
        OLD_NAME = f"{PREFIX}oldname.xyz"
        NEW_NAME = f"{PREFIX}newname.abc"

        file_id = test_file(file_name=OLD_NAME)

        rename_file(client=client, file_id=file_id, name=NEW_NAME)

        # verify the File Name and extension
        files = client.get_files(ids=[file_id])
        assert len(files.available_files) == 1
        assert files.available_files[0].properties is not None
        assert files.available_files[0].properties["Name"] == NEW_NAME

    def test__update_metadata__append_replace_succeeds(
        self, client: FileClient, test_file
    ):
        # Upload File-> Add 2 props-> Verify-> Replace 2 props with 3 new props-> Verify
        file_id = test_file()

        new_metadata = {"Prop1": "Value1", "Prop2": "Value2"}

        append_prop_request = UpdateMetadataRequest(
            replace_existing=False, properties=new_metadata
        )
        client.update_metadata(metadata=append_prop_request, id=file_id)

        # verify appended properties
        files = client.get_files(ids=[file_id])
        assert len(files.available_files) == 1
        assert files.available_files[0].properties is not None
        assert (
            len(files.available_files[0].properties.keys()) == len(new_metadata) + 1
        )  # Name + 2 added properties

        file_props = files.available_files[0].properties

        for prop_name, value in new_metadata.items():
            assert file_props[prop_name] == value

        # replace the properties by a new one
        replace_metadata = {"Prop3": "Value3", "Prop4": "Value4", "Prop5": "Value5"}

        append_prop_request = UpdateMetadataRequest(
            replace_existing=True, properties=replace_metadata
        )
        client.update_metadata(metadata=append_prop_request, id=file_id)
        # verify replaced properties
        files = client.get_files(ids=[file_id])
        assert len(files.available_files) == 1
        assert files.available_files[0].properties is not None
        assert (
            len(files.available_files[0].properties.keys()) == len(replace_metadata) + 1
        )  # Name + 3 replaced properties

    def test__back_off_retry__works(self, client: FileClient, test_file):
        file_id = test_file()

        for i in range(20):
            rename_file(client=client, file_id=file_id, name=f"{PREFIX}{i}.abc")
