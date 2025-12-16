"""Integration tests for FileClient."""

import io
import string
from datetime import datetime
from random import choices, randint
from typing import BinaryIO

import backoff  # type: ignore
import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import (
    FileLinqQueryOrderBy,
    FileLinqQueryRequest,
    SearchFilesRequest,
    UpdateMetadataRequest,
)
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
        client.delete_files(ids=file_ids)


@pytest.fixture(scope="class")
def invalid_file_id(client: FileClient) -> str:
    """Generate a invalid file id."""
    MAX_RETRIES = 10
    attempts = 0

    while attempts < MAX_RETRIES:
        file_id = f"Invalid-File-Id-{randint(1000, 9999)}"
        files = client.get_files(ids=[file_id])
        if files.total_count == 0:
            return file_id

    raise Exception(f"Failed to generate a invalid-file-id in {MAX_RETRIES} attempts.")


@pytest.fixture
def random_filename_extension() -> str:
    """Generate a random filename and extension."""
    rand_file_name = "".join(choices(string.ascii_letters + string.digits, k=10))
    rand_file_extension = "".join(choices(string.ascii_letters, k=3))

    return f"{PREFIX}{rand_file_name}.{rand_file_extension}"


@pytest.mark.enterprise
@pytest.mark.integration
class TestFileClient:
    def test__api_info__returns(self, client: FileClient):
        api_info = client.api_info()
        assert len(api_info.model_dump()) != 0

    def test__upload_get_delete_files__succeeds(
        self, client: FileClient, test_file, random_filename_extension
    ):
        # upload a file
        file_id = test_file(file_name=random_filename_extension, cleanup=False)
        assert file_id != ""

        files = client.get_files(ids=[file_id])
        assert files.total_count == 1
        assert len(files.available_files) == 1
        assert files.available_files[0].id == file_id
        assert files.available_files[0].properties is not None
        assert files.available_files[0].properties["Name"] == random_filename_extension

        client.delete_file(id=file_id)

        # confirm that file was deleted
        files = client.get_files(ids=[file_id])
        assert files.total_count == 0

    def test__delete_file__invalid_id_raises(
        self, client: FileClient, invalid_file_id: str
    ):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.delete_file(id=invalid_file_id)

    def test__delete_files__succeeds(self, client: FileClient, test_file):
        # upload 2 files and delete them
        NUM_FILES = 2

        file_ids = [test_file(cleanup=False) for _ in range(NUM_FILES)]

        # confirm that files exist
        files = client.get_files(ids=file_ids)
        assert files.total_count == NUM_FILES

        client.delete_files(ids=file_ids)

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
        random_filename_extension: str,
    ):
        # Upload the test file with random name
        file_id = test_file(file_name=random_filename_extension)

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

    def test__query_files_linq__filter_by_name_succeeds(
        self, client: FileClient, test_file, random_filename_extension: str
    ):
        file_id = test_file(file_name=random_filename_extension)

        query_request = FileLinqQueryRequest(
            filter=f'name == "{random_filename_extension}"',
            order_by=FileLinqQueryOrderBy.CREATED,
            order_by_descending=True,
            take=1,
        )
        response = client.query_files_linq(query=query_request)

        assert response.available_files is not None
        assert response.total_count is not None
        assert response.total_count.value == 1
        assert response.total_count.relation == "eq"
        assert len(response.available_files) == 1
        assert response.available_files[0].id == file_id
        assert response.available_files[0].created is not None
        assert isinstance(response.available_files[0].created, datetime)
        assert response.available_files[0].updated is not None
        assert isinstance(response.available_files[0].updated, datetime)
        assert response.available_files[0].workspace is not None
        assert response.available_files[0].size is not None
        assert response.available_files[0].size64 is not None
        assert response.available_files[0].properties is not None
        assert (
            response.available_files[0].properties["Name"] == random_filename_extension
        )

    def test__query_files_linq__invalid_filter_raises(self, client: FileClient):
        query_request = FileLinqQueryRequest(filter="invalid filter syntax:")

        with pytest.raises(ApiException):
            client.query_files_linq(query=query_request)

    def test__query_files_linq__filter_returns_no_results(self, client: FileClient):
        unique_nonexistent_name = (
            f"{PREFIX}nonexistent_file_{randint(100000, 999999)}.random_extension"
        )

        query_request = FileLinqQueryRequest(
            filter=f'name == "{unique_nonexistent_name}"'
        )
        response = client.query_files_linq(query=query_request)

        assert response.available_files is not None
        assert len(response.available_files) == 0
        assert response.total_count is not None
        assert response.total_count.value == 0
        assert response.total_count.relation == "eq"

    @backoff.on_exception(
        backoff.expo,
        AssertionError,
        max_tries=5,
        max_time=5,
    )
    def test__search_files__succeeds(
        self, client: FileClient, test_file, random_filename_extension: str
    ):
        """Test search_files with filtering, pagination, and ordering."""
        # Upload 5 files to test various scenarios
        NUM_FILES = 5
        file_ids = []
        file_prefix = f"{PREFIX}search_test_{randint(1000, 9999)}"
        
        for i in range(NUM_FILES):
            file_name = f"{file_prefix}_{i}.bin"
            file_id = test_file(file_name=file_name)
            file_ids.append(file_id)

        # Search with filter (by name pattern), pagination, and ordering
        search_request = SearchFilesRequest(
            filter=f'(name:("{file_prefix}*"))',
            skip=1,
            take=3,
            order_by="name",
            order_by_descending=True,
        )
        response = client.search_files(request=search_request)
        
        assert response.available_files is not None
        assert response.total_count is not None
        assert response.total_count.value == 5
        assert response.total_count.relation is not None
        assert len(response.available_files) == 3  # skip=1, take=3
        
        # Verify all fields in response
        for file_metadata in response.available_files:
            assert file_metadata.id in file_ids
            assert file_metadata.name is not None
            assert file_metadata.name.startswith(file_prefix)
            assert file_metadata.created is not None
            assert isinstance(file_metadata.created, datetime)
            assert file_metadata.updated is not None
            assert isinstance(file_metadata.updated, datetime)
            assert file_metadata.workspace is not None
            assert file_metadata.size is not None
            assert file_metadata.properties is not None
            assert "Name" in file_metadata.properties
        
        # Verify descending order by name
        returned_names = [f.name for f in response.available_files]
        assert returned_names == sorted(returned_names, reverse=True)

    def test__search_files__no_filter_succeeds(self, client: FileClient, test_file):
        file_id = test_file()

        search_request = SearchFilesRequest(skip=0, take=10)
        response = client.search_files(request=search_request)

        assert response.available_files is not None
        assert response.total_count is not None
        assert response.total_count.value >= 1
        assert len(response.available_files) >= 1

    def test__search_files__invalid_filter_raises(self, client: FileClient):
        search_request = SearchFilesRequest(filter="invalid filter syntax")

        with pytest.raises(ApiException):
            client.search_files(request=search_request)

    def test__search_files__filter_returns_no_results(self, client: FileClient):
        unique_nonexistent_name = (
            f"{PREFIX}nonexistent_search_file_{randint(100000, 999999)}.random_ext"
        )

        search_request = SearchFilesRequest(
            filter=f'(name:("{unique_nonexistent_name}"))', skip=0, take=10
        )
        response = client.search_files(request=search_request)

        assert response.available_files is not None
        assert len(response.available_files) == 0
        assert response.total_count is not None
        assert response.total_count.value == 0
