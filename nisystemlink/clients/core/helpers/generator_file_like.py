"""A file-like object adapter that wraps a python generator, providing a way to
iterate over the generator as if it was a file.
"""


class GeneratorFileLike:
    def __init__(self, generator):
        self._generator = generator
        self._buffer = b""

    def read(self, size=-1):
        """Read at most `size` bytes from the file-like object. If `size` is not
        specified or is negative, read until the generator is exhausted and
        returns all bytes or characters read.
        """
        while size < 0 or len(self._buffer) < size:
            try:
                chunk = next(self._generator)
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
