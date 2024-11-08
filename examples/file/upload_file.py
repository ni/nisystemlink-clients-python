"""Example to upload a file to SystemLink."""

from nisystemlink.clients.file import FileClient

client = FileClient()

file_path = "path/to/your/file"
workspace_id = None  # Upload to default workspace of the auth key

with open(file_path, "rb") as fp:
    file_id = client.upload_file(file=fp, workspace=workspace_id)
    print(f"Uploaded file from {file_path} to SystemLink with FileID - {file_id}")
