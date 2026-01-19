"""Example to upload a file to SystemLink."""

import io

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.file import FileClient

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = FileClient(configuration=server_configuration)

workspace_id = None  # Upload to default workspace of the auth key

# Upload file from disk
file_path = "path/to/your/file"
with open(file_path, "rb") as fp:
    file_id = client.upload_file(file=fp, workspace=workspace_id)
    print(f"Uploaded file from {file_path} to SystemLink with FileID - {file_id}")

# Upload file-like object from memory
test_file = io.BytesIO(b"This is an example file content.")
test_file.name = "File_From_Memory.txt"  # assign a name to the file object
file_id = client.upload_file(file=test_file)
print(f"Uploaded file from memory to SystemLink with FileID - {file_id}")
