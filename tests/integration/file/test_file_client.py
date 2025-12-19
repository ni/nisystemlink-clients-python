"""Integration tests for FileClient."""

import io
import string
from datetime import datetime
from io import BytesIO
from random import choices, randint
from typing import BinaryIO

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.file import FileClient
from nisystemlink.clients.file.models import (
    FileLinqQueryOrderBy,
    FileLinqQueryRequest,
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

    def test__start_upload_session__with_invalid_workspace__raises(
        self, client: FileClient
    ):
        invalid_workspace_id = "invalid-workspace-id"

        with pytest.raises(ApiException):
            client.start_upload_session(workspace=invalid_workspace_id)

    def test__append_to_upload_session__uploads_file_in_chunks(
        self, client: FileClient
    ):
        # Create a test file with known content
        test_content = b"A" * 10485760 + b"B" * 5000000  # 10 MB + 5 MB
        chunk_size = 10485760  # 10 MB

        # Start upload session
        session_response = client.start_upload_session()

        # Verify session response
        assert session_response is not None
        assert session_response.id is not None
        assert isinstance(session_response.id, str)
        assert session_response.created_at is not None
        assert isinstance(session_response.created_at, datetime)

        session_id = session_response.id
        file_id = None

        try:
            # Upload first chunk
            first_chunk = BytesIO(test_content[:chunk_size])
            client.append_to_upload_session(
                session_id=session_id, chunk=1, file=first_chunk
            )

            # Upload second chunk (last chunk)
            second_chunk = BytesIO(test_content[chunk_size:])
            client.append_to_upload_session(
                session_id=session_id, chunk=2, file=second_chunk, close=True
            )

            # Finish the upload session
            file_name = f"{PREFIX}chunked_upload_test.bin"
            file_id = client.finish_upload_session(
                session_id=session_id,
                name=file_name,
                properties={
                    "Name": file_name,
                    "Test": "ChunkedUpload",
                    "Description": "Test file from chunked upload",
                },
            )

            # Verify the file was created with correct metadata
            files = client.get_files(ids=[file_id])
            assert files.total_count == 1
            assert len(files.available_files) == 1
            assert files.available_files[0].id == file_id
            assert files.available_files[0].properties is not None
            assert files.available_files[0].properties.get("Name") == file_name
            assert files.available_files[0].properties.get("Test") == "ChunkedUpload"
            assert (
                files.available_files[0].properties.get("Description")
                == "Test file from chunked upload"
            )

            # Verify file content
            downloaded_data = client.download_file(id=file_id)
            assert downloaded_data.read() == test_content
        except ApiException as api_exception:
            raise api_exception
            # Finish the upload session if it failed during chunk upload
            if not file_id:
                file_name = f"{PREFIX}chunked_upload_test.bin"
                file_id = client.finish_upload_session(
                    session_id=session_id,
                    name=file_name,
                    properties={"Name": file_name, "Test": "ChunkedUpload"},
                )
            raise api_exception
        finally:
            # Clean up
            if file_id:
                try:
                    client.delete_file(id=file_id)
                except Exception:
                    pass  # Ignore cleanup errors

    def test__finish_upload_session__invalid_session_id_raises(
        self, client: FileClient, invalid_file_id: str
    ):
        file_name = f"{PREFIX}invalid_session.txt"
        properties = {"Name": file_name}

        with pytest.raises(ApiException):
            client.finish_upload_session(
                session_id=invalid_file_id, name=file_name, properties=properties
            )
