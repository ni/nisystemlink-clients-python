from typing import Any, Iterator


class IteratorFileLike:
    """A file-like object adapter that wraps a python iterator, providing a way to
    read from the iterator as if it was a file.
    """

    def __init__(self, iterator: Iterator[Any]):
        self._iterator = iterator
        self._buffer = b""

    def read(self, size: int = -1) -> bytes:
        """Read at most `size` bytes from the file-like object. If `size` is not
        specified or is negative, read until the iterator is exhausted and
        returns all bytes or characters read.
        """
        while size < 0 or len(self._buffer) < size:
            try:
                chunk = next(self._iterator)
                self._buffer += chunk
            except StopIteration:
                break
        if size < 0:
            data = self._buffer
            self._buffer = b""
        else:
            data = self._buffer[:size]
            self._buffer = self._buffer[size:]
        return data
