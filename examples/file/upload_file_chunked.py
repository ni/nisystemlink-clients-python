"""Example to upload a large file to SystemLink using chunked upload (upload sessions).

This example demonstrates how to upload a file in chunks using upload sessions.
This is useful for large files that need to be uploaded in multiple parts.
"""

import io

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.file import FileClient

# Configure connection to SystemLink server
server_configuration = HttpConfiguration(
    server_uri="https://test-api.lifecyclesolutions.ni.com/",
    api_key="zr7fUQj3R2zSBt6b46LGquPkPZJ8wll_wg6oqRLQn2",
)

client = FileClient(configuration=server_configuration)

# Generate example file content (20 MB for demonstration)
CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB chunks
file_content = b"X" * (20 * 1024 * 1024)  # 20 MB file

# Step 1: Start an upload session
session_response = client.start_upload_session(workspace=None)
session_id = session_response.session_id
print(f"Started upload session with ID: {session_id}")

# Step 2: Upload chunks
# Split the file content into chunks and upload them
file_id = None
try:
    num_chunks = (len(file_content) + CHUNK_SIZE - 1) // CHUNK_SIZE

    for i in range(num_chunks):
        start = i * CHUNK_SIZE
        end = min(start + CHUNK_SIZE, len(file_content))
        chunk_data = file_content[start:end]

        # Create a file-like object for the chunk
        chunk_file = io.BytesIO(chunk_data)

        # Determine if this is the last chunk
        is_last_chunk = i == num_chunks - 1

        # Upload the chunk (chunk_index is 0-based)
        client.append_to_upload_session(
            session_id=session_id,
            chunk_index=i + 1,
            file=chunk_file,
            close=is_last_chunk,
        )
        print(f"Uploaded chunk {i + 1}/{num_chunks} ({len(chunk_data)} bytes)")

    # Step 3: Finish the upload session
    file_name = "large_file_example.bin"
    properties = {
        "Description": "Example file uploaded using chunked upload",
        "FileSize": str(len(file_content)),
    }

    file_id = client.finish_upload_session(
        session_id=session_id, name=file_name, properties=properties
    )

    print(f"\nSuccessfully uploaded file '{file_name}' with FileID: {file_id}")

except Exception as e:
    print(f"Error during chunked upload: {e}")
    # Attempt to finish the session to clean up resources on the server
    try:
        print("Attempting to clean up upload session...")
        file_id = client.finish_upload_session(
            session_id=session_id,
            name=f"incomplete_{file_name}",
            properties={"Status": "Incomplete", "Error": str(e)},
        )
        print(f"Session cleaned up. Partial file saved with FileID: {file_id}")
    except Exception as cleanup_error:
        print(f"Failed to clean up session: {cleanup_error}")
        print(f"Upload session {session_id} may need manual cleanup")

finally:
    # Clean up: Delete the uploaded file (whether complete or incomplete)
    if file_id:
        try:
            client.delete_file(id=file_id)
            print(f"Deleted file (FileID: {file_id})")
        except Exception as delete_error:
            print(f"Failed to delete file: {delete_error}")
