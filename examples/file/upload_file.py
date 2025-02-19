"""Example to upload a file to SystemLink."""

import io

from nisystemlink.clients.file import FileClient

client = FileClient()

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
