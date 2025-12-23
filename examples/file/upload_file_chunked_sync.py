"""Example of synchronous chunked file upload to SystemLink.

This example demonstrates uploading a large file in chunks without loading
the entire file into memory at once. Each chunk is read and uploaded sequentially.
"""

import tempfile
import time
from functools import partial
from io import BytesIO

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.file import FileClient

# Configure connection to SystemLink server
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)

client = FileClient(configuration=server_configuration)

# Generate example file content (50 MB for demonstration)
CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB chunks
FILE_SIZE = 50 * 1024 * 1024  # 50 MB file
# Generate test file content by repeating a simple message
test_data = b"This is test data for chunked file upload example.\n"
file_content = test_data * (FILE_SIZE // len(test_data))

# Create a temporary file to mimic file-on-disk behavior
# delete=True ensures automatic cleanup when the with block exits
with tempfile.NamedTemporaryFile(delete=True, suffix=".bin") as temp_file:
    temp_file.write(file_content)
    temp_file_path = temp_file.name
    temp_file.flush()  # Ensure data is written to disk

    print(f"Created temporary file: {temp_file_path}")
    print(f"File size: {FILE_SIZE / (1024 * 1024):.1f} MB")
    print(f"Chunk size: {CHUNK_SIZE / (1024 * 1024):.1f} MB\n")

    # Start upload session
    session_response = client.start_upload_session(workspace=None)
    session_id = session_response.session_id
    print(f"Started upload session: {session_id}\n")

    file_id = None
    start_time = time.time()

    try:
        # Read and upload chunks sequentially using iter() with sentinel
        # This approach only loads one chunk into memory at a time
        temp_file.seek(0)  # Seek back to the beginning of the file

        # Create a partial function for reading chunks
        read_chunk = partial(temp_file.read, CHUNK_SIZE)

        # Create an iterator that yields chunks until an empty bytes object is returned
        chunk_iterator = iter(read_chunk, b"")

        # Process chunks one at a time
        chunk_index = 1
        total_chunks = (
            FILE_SIZE + CHUNK_SIZE - 1
        ) // CHUNK_SIZE  # Calculate total chunks

        for chunk_data in chunk_iterator:
            is_last_chunk = len(chunk_data) < CHUNK_SIZE or chunk_index == total_chunks

            chunk_start = time.time()

            # Upload chunk directly (wrap in BytesIO for type compatibility)
            client.append_to_upload_session(
                session_id=session_id,
                chunk_index=chunk_index,
                chunk=BytesIO(chunk_data),
                close=is_last_chunk,
            )

            chunk_time = time.time() - chunk_start
            chunk_size_mb = len(chunk_data) / (1024 * 1024)
            print(
                f"Chunk {chunk_index}/{total_chunks} uploaded "
                f"({chunk_size_mb:.1f} MB) in {chunk_time:.2f}s"
            )

            chunk_index += 1

        # Finish the upload session
        file_id = client.finish_upload_session(
            session_id=session_id,
            name="chunked_upload_example.bin",
            properties={"Type": "Synchronous Chunked", "FileSize": str(FILE_SIZE)},
        )

        total_time = time.time() - start_time
        print("\nUpload completed successfully!")
        print(f"File ID: {file_id}")
        print(f"Total time: {total_time:.2f}s")

    except Exception as e:
        print(f"Error during upload: {e}")
        if not file_id:
            try:
                file_id = client.finish_upload_session(
                    session_id=session_id,
                    name="incomplete_upload.bin",
                    properties={"Status": "Failed"},
                )
            except Exception as finish_error:
                print(f"Failed to finish session: {finish_error}")

    finally:
        # Clean up: Delete uploaded file
        print("\nCleaning up...")
        if file_id:
            try:
                client.delete_file(id=file_id)
                print(f"Deleted uploaded file: {file_id}")
            except Exception as e:
                print(f"Failed to delete file {file_id}: {e}")

        print(f"Temporary file will be automatically deleted: {temp_file_path}")
        print("Cleanup complete")
