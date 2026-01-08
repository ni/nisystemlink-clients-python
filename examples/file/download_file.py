"""Example to download a file from SystemLink."""

from shutil import copyfileobj

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
