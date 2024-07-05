"""Example to download a file from SystemLink."""

from shutil import copyfileobj

from nisystemlink.clients.file import FileClient

client = FileClient()

file_id = "<Id of file to download>"

file_name = f"{file_id}.extension"

# Download the file using FileId with content inline
content = client.download_file(file_id=file_id)

# Write the content to a file
with open(file_name, "wb") as f:
    copyfileobj(content, f)
