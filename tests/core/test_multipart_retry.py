import io

from requests import Response
from nisystemlink.clients.core._uplink._multipart_retry import (
    _RetryableMultipartRequestTemplate,
)
from uplink.clients.io import state as uplink_state


class _NonSeekableStream:
    def seekable(self) -> bool:
        return False

    def seek(self, offset: int) -> None:
        raise AssertionError("seek should not be called for non-seekable streams")


class _FailingSeekStream:
    def seek(self, offset: int) -> None:
        raise OSError("cannot rewind")


class TestRetryableMultipartRequestTemplate:
    def test__before_request_on_initial_attempt__does_not_rewind_parts(self):
        direct_part = io.BytesIO(b"direct")
        direct_part.seek(3)
        tuple_part = io.BytesIO(b"tuple")
        tuple_part.seek(2)
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "direct": direct_part,
                    "tuple": ("tuple.bin", tuple_part, "application/octet-stream"),
                }
            },
        )

        _RetryableMultipartRequestTemplate().before_request(request)

        assert direct_part.tell() == 3
        assert tuple_part.tell() == 2

    def test__before_request_on_retry__rewinds_parts(self):
        direct_part = io.BytesIO(b"direct")
        direct_part.seek(3)
        tuple_part = io.BytesIO(b"tuple")
        tuple_part.seek(2)
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "direct": direct_part,
                    "tuple": ("tuple.bin", tuple_part, "application/octet-stream"),
                }
            },
        )
        template = _RetryableMultipartRequestTemplate()

        template.before_request(request)
        direct_part.read()
        tuple_part.read()
        template.before_request(request)

        assert direct_part.tell() == 0
        assert tuple_part.tell() == 0

    def test__before_request_with_non_seekable_parts__does_not_raise(self):
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "non_seekable": _NonSeekableStream(),
                    "failing_seek": _FailingSeekStream(),
                }
            },
        )
        template = _RetryableMultipartRequestTemplate()

        template.before_request(request)
        template.before_request(request)

    def test__before_request_when_rewind_fails_after_response__finishes_with_saved_response(
        self,
    ):
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "failing_seek": _FailingSeekStream(),
                }
            },
        )
        response = Response()
        response.status_code = 429
        response.url = "https://example.com/upload"
        template = _RetryableMultipartRequestTemplate()

        template.before_request(request)
        template.after_response(request, response)
        action = template.before_request(request)

        assert action is not None
        next_state = action(uplink_state.BeforeRequest(request))
        assert isinstance(next_state, uplink_state.Finish)
        assert next_state.response is response

    def test__before_request_on_retry_with_string_only_parts__allows_retry(self):
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "workspace": "workspace-id",
                    "metadata": (None, '{"name": "example"}'),
                }
            },
        )
        response = Response()
        response.status_code = 429
        response.url = "https://example.com/upload"
        template = _RetryableMultipartRequestTemplate()

        template.before_request(request)
        template.after_response(request, response)
        action = template.before_request(request)

        assert action is None