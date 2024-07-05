"""Example to download a file from SystemLink."""

from shutil import copyfileobj

from nisystemlink.clients.file import FileClient

client = FileClient()

file_id = "<Id of file to download>"

# Fetch the file metadata to get the name
files = client.get_files(file_ids=[file_id])

if not files.available_files:
    raise Exception(f"File ID {file_id} not found.")

file_name = files.available_files[0].properties.get("Name", "Untitled")

# Download the file using FileId with content inline
content = client.download_file(file_id=file_id)

# Write the content to a file
with open(file_name, "wb") as f:
    copyfileobj(content, f)
