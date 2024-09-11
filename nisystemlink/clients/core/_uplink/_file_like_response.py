from nisystemlink.clients.core.helpers import IteratorFileLike
from requests.models import Response


def file_like_response_handler(response: Response) -> IteratorFileLike:
    """Response handler for File-Like content."""
    return IteratorFileLike(response.iter_content(chunk_size=4096))
