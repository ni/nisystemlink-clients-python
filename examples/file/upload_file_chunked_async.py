"""Example of asynchronous chunked file upload to SystemLink.

This example demonstrates uploading a large file in chunks concurrently,
without loading the entire file into memory at once. Multiple chunks are
uploaded simultaneously for better performance.
"""

import asyncio
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


async def upload_chunk_async(
    session_id: str, chunk_index: int, chunk_data: bytes, is_last: bool
) -> int:
    """Upload a single chunk asynchronously."""
    # Run the synchronous upload in a thread pool to avoid blocking
    await asyncio.to_thread(
        client.append_to_upload_session,
        session_id=session_id,
        chunk_index=chunk_index,
        chunk=BytesIO(chunk_data),
        close=is_last,
    )
    return chunk_index


# Create a temporary file to mimic file-on-disk behavior
with tempfile.NamedTemporaryFile(delete=True, suffix=".bin") as temp_file:
    temp_file.write(file_content)
    temp_file_path = temp_file.name
    temp_file.flush()  # Ensure data is written to disk

    async def main():
        """Main async function to upload file chunks concurrently."""
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
            chunks = []
            temp_file.seek(0)

            read_chunk = partial(temp_file.read, CHUNK_SIZE)

            chunk_iterator = iter(read_chunk, b"")

            chunk_index = 1
            for chunk_data in chunk_iterator:
                chunks.append((chunk_index, chunk_data))
                chunk_index += 1

            total_chunks = len(chunks)
            print(f"Uploading {total_chunks} chunks concurrently...\n")

            # Upload chunks concurrently
            tasks = [
                upload_chunk_async(session_id, idx, data, idx == total_chunks)
                for idx, data in chunks
            ]

            # Run all upload tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Check for errors
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Chunk {i + 1} failed: {result}")
                    raise result
                else:
                    print(f"Chunk {result}/{total_chunks} uploaded")

            # Finish the upload session
            file_id = client.finish_upload_session(
                session_id=session_id,
                name="async_chunked_upload_example.bin",
                properties={"Type": "Asynchronous Chunked", "FileSize": str(FILE_SIZE)},
            )

            total_time = time.time() - start_time
            print("\nUpload completed successfully!")
            print(f"File ID: {file_id}")
            print(f"Total time: {total_time:.2f}s")

            return file_id

        except Exception as e:
            print(f"Error during upload: {e}")
            if not file_id:
                try:
                    file_id = client.finish_upload_session(
                        session_id=session_id,
                        name="incomplete_async_upload.bin",
                        properties={"Status": "Failed"},
                    )
                except Exception as finish_error:
                    print(f"Failed to finish session: {finish_error}")
            return file_id

    # Run the async main function
    try:
        file_id = asyncio.run(main())

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
