# from shutil import copyfileobj
# from tempfile import TemporaryFile
# from typing import Optional

import pytest  # type: ignore
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.file import FileClient

# from nisystemlink.clients.file.models import FileMetadata

INVALID_FILE_ID = "Invalid-File-Id"
FILE_NOT_FOUND_ERR = "Not Found"


@pytest.fixture(scope="class")
def client(enterprise_config) -> FileClient:
    """Fixture to create a FileClient instance."""
    return FileClient(enterprise_config)


# @pytest.fixture(scope="class")
# def binary_file() -> io.BytesIO:
#     """Fixture to create a binary file as file pointer object."""
#     fake_file = io.BytesIO(b"123abc")
#     fake_file.name = "Fake File.bin"
#     return fake_file


# @pytest.fixture(scope="class")
# def upload_file(client: FileClient):
#     """Fixture to return a factory that uploads a file."""
#     file_ids = []

#     def _upload_file(file) -> str:
#         id = client.upload_file(file=file)
#         file_ids.append(id)
#         return id

#     yield _upload_file

#     _delete_files = DeleteMutipleRequest(ids=file_ids)
#     client.delete_files(files=_delete_files, force=True)


# @pytest.fixture(scope="class")
# def test_file(upload_file, binary_file) -> str:
#     """Fixture to create, upload a test file."""
#     id = upload_file(binary_file)
#     return id


# @pytest.fixture(scope="class")
# def test_download_file(client: FileClient) -> FileMetadata:
#     """Get the MetaData of a File to download."""
#     files = client.get_files(take=1)

#     if files.available_files:
#         return files.available_files[0]
#     else:
#         raise Exception("Require at least 1 File to download.")


@pytest.mark.enterprise
@pytest.mark.integration
class TestFileClient:
    def test__api_info__returns(self, client: FileClient):
        api_info = client.api_info()
        assert len(api_info.dict()) != 0

    def test__get_files__succeeds(self, client: FileClient):
        take_count = 1
        files = client.get_files(take=take_count)

        assert len(files.available_files) == take_count
        assert files.total_count >= take_count

    def test__delete_file__invalid_id_raises(self, client: FileClient):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.delete_file(file_id=INVALID_FILE_ID, force=True)

    # def test__delete_file__succeeds(self, client: FileClient):
    #     client.delete_file(file_id="7729547d-95af-4beb-a7a8-a913c0a23de4", force=True)

    def test__download_file__invalid_id_raises(self, client: FileClient):
        with pytest.raises(ApiException, match=FILE_NOT_FOUND_ERR):
            client.download_file(file_id=INVALID_FILE_ID)

    # def test__download_file__succeeds(self, client: FileClient, test_download_file: FileMetadata):
    #     file_id = test_download_file.id
    #     data = client.download_file(file_id=file_id)
    #     with open(f"downloaded_file", "wb") as f:
    #         copyfileobj(data, f)
