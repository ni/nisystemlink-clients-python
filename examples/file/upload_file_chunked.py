"""Example comparing synchronous and asynchronous chunked file upload to SystemLink.

This example demonstrates:
1. Synchronous chunk upload (one chunk at a time)
2. Asynchronous chunk upload (multiple chunks concurrently)
3. Performance comparison between both approaches
"""

import asyncio
import io
import os
import tempfile
import time

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
with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as temp_file:
    temp_file.write(file_content)
    temp_file_path = temp_file.name


def upload_chunk(
    session_id: str, chunk_index: int, chunk_data: bytes, is_last: bool
) -> int:
    """Upload a single chunk."""
    chunk_file = io.BytesIO(chunk_data)
    client.append_to_upload_session(
        session_id=session_id, chunk_index=chunk_index, file=chunk_file, close=is_last
    )
    return chunk_index


async def upload_chunk_async(
    session_id: str, chunk_index: int, chunk_data: bytes, is_last: bool
) -> int:
    """Upload a single chunk asynchronously."""
    # Run the synchronous upload in a thread pool to avoid blocking
    return await asyncio.to_thread(
        upload_chunk, session_id, chunk_index, chunk_data, is_last
    )


def upload_synchronous():
    """Upload file chunks synchronously (one at a time)."""
    print("\nSynchronous Upload:")

    # Start upload session
    session_response = client.start_upload_session(workspace=None)
    session_id = session_response.session_id
    print(f"Started upload session: {session_id}\n")

    file_id = None
    start_time = time.time()

    try:
        # Read and upload chunks sequentially using iter() with sentinel
        with open(temp_file_path, "rb") as f:
            chunks = list(enumerate(iter(lambda: f.read(CHUNK_SIZE), b""), start=1))
            num_chunks = len(chunks)

            for i, chunk_data in chunks:
                is_last_chunk = i == num_chunks

                chunk_start = time.time()
                upload_chunk(session_id, i, chunk_data, is_last_chunk)
                chunk_time = time.time() - chunk_start

                print(f"  Chunk {i}/{num_chunks} uploaded in {chunk_time:.2f}s")

        # Finish the upload session
        file_id = client.finish_upload_session(
            session_id=session_id,
            name="sync_upload_example.bin",
            properties={"Type": "Synchronous", "FileSize": str(FILE_SIZE)},
        )

        total_time = time.time() - start_time
        print(f"\nUpload completed in {total_time:.2f}s")
        print(f"File ID: {file_id}\n")

        return file_id, total_time

    except Exception as e:
        print(f"✗ Error: {e}")
        if not file_id:
            file_id = client.finish_upload_session(
                session_id=session_id,
                name="incomplete_sync.bin",
                properties={"Status": "Failed"},
            )
        return file_id, None


async def upload_asynchronous():
    """Upload file chunks asynchronously (concurrently)."""
    print("\nAsynchronous Upload (Concurrent):")

    # Start upload session
    session_response = client.start_upload_session(workspace=None)
    session_id = session_response.session_id
    print(f"Started upload session: {session_id}\n")

    file_id = None
    start_time = time.time()

    try:
        # Read all chunks using iter() with sentinel for cleaner iteration
        with open(temp_file_path, "rb") as f:
            chunks = list(enumerate(iter(lambda: f.read(CHUNK_SIZE), b""), start=1))
            num_chunks = len(chunks)
            chunks = [(i, data, i == num_chunks) for i, data in chunks]

        # Upload chunks concurrently
        print(f"Uploading {num_chunks} chunks concurrently\n")

        tasks = [
            upload_chunk_async(session_id, idx, data, is_last)
            for idx, data, is_last in chunks
        ]

        # Run all upload tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check for errors
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"  Chunk {i + 1} failed: {result}")
                raise result
            else:
                print(f"  Chunk {result}/{num_chunks} uploaded")

        # Finish the upload session
        file_id = client.finish_upload_session(
            session_id=session_id,
            name="async_upload_example.bin",
            properties={"Type": "Asynchronous", "FileSize": str(FILE_SIZE)},
        )

        total_time = time.time() - start_time
        print(f"\nUpload completed in {total_time:.2f}s")
        print(f"  File ID: {file_id}\n")

        return file_id, total_time

    except Exception as e:
        print(f"✗ Error: {e}")
        if not file_id:
            file_id = client.finish_upload_session(
                session_id=session_id,
                name="incomplete_async.bin",
                properties={"Status": "Failed"},
            )
        return file_id, None


# Run both upload methods and compare
async def main():
    """Main function to run both upload methods."""
    # Synchronous upload
    sync_file_id, sync_time = upload_synchronous()

    # Asynchronous upload
    async_file_id, async_time = await upload_asynchronous()

    # Performance comparison
    if sync_time and async_time:
        print("\nPerformance Comparison:")
        print(f"Synchronous:  {sync_time:.2f}s")
        print(f"Asynchronous: {async_time:.2f}s")

    return sync_file_id, async_file_id


try:
    # Run the async main function
    sync_file_id, async_file_id = asyncio.run(main())

finally:
    # Clean up: Delete uploaded files
    print("Cleaning up...")
    for file_id in [sync_file_id, async_file_id]:
        if file_id:
            try:
                client.delete_file(id=file_id)
                print(f"  Deleted file: {file_id}")
            except Exception as e:
                print(f"  Failed to delete {file_id}: {e}")

    os.unlink(temp_file_path)
    print(f"  Deleted temp file: {temp_file_path}")

    print("\nCleanup complete")
