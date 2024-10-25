"""Example to download a file from SystemLink."""

from shutil import copyfileobj

from nisystemlink.clients.file import FileClient

client = FileClient()

file_id = "a55adc7f-5068-4202-9d70-70ca6a06bee9"

# Fetch the file metadata to get the name
files = client.get_files(ids=[file_id])

if not files.available_files:
    raise Exception(f"File ID {file_id} not found.")


file_name = "Untitled"

file_properties = files.available_files[0].properties

if file_properties:
    file_name = file_properties["Name"]

# Download the file using FileId with content inline
content = client.download_file(id=file_id)

# Write the content to a file
with open(file_name, "wb") as f:
    copyfileobj(content, f)
