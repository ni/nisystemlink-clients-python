import io
from typing import Any, cast

import pytest
import responses
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.core._uplink._base_client import _handle_http_status
from nisystemlink.clients.core._uplink._multipart_retry import (
    _RetryableMultipartCleanupTemplate,
    _RetryableMultipartRequestTemplate,
    retryable_multipart_request,
)
from requests import Response
from uplink import Consumer, Part, post, retry
from uplink.clients.io import CompositeRequestTemplate
from uplink.clients.io import state as uplink_state
from uplink.clients.io.interfaces import RequestTemplate


class _NonSeekableStream:
    def seekable(self) -> bool:
        return False

    def seek(self, offset: int) -> None:
        raise AssertionError("seek should not be called for non-seekable streams")


class _FailingSeekStream:
    def __init__(self, data: bytes = b"artifact") -> None:
        self._buffer = io.BytesIO(data)

    def read(self, size: int = -1) -> bytes:
        return self._buffer.read(size)

    def seek(self, offset: int) -> None:
        raise OSError("cannot rewind")


class _StaticTransitionTemplate(RequestTemplate):
    def __init__(self, response_transition=None, exception_transition=None) -> None:
        self._response_transition = response_transition
        self._exception_transition = exception_transition

    def after_response(self, request, response):
        return self._response_transition

    def after_exception(self, request, exc_type, exc_val, exc_tb):
        return self._exception_transition


@retry(
    when=retry.when.status(429),
    stop=retry.stop.after_attempt(2),
    backoff=retry.backoff.fixed(0),
)
class _MultipartRetryTestConsumer(Consumer):
    def __init__(self):
        super().__init__(
            base_url="https://example.com/",
            hooks=[_handle_http_status],
        )

    @retryable_multipart_request()
    @post("upload", args=[Part("artifact")])
    def upload(self, artifact):
        pass


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
        request_id = id(request)
        assert request_id not in template._attempted_request_ids
        assert request_id not in template._responses_by_request_id
        assert request_id not in template._exceptions_by_request_id

    def test__terminal_response_after_retry_pipeline__clears_saved_retry_state(self):
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "artifact": ("artifact.bin", io.BytesIO(b"artifact")),
                }
            },
        )
        response = Response()
        response.status_code = 200
        response.url = "https://example.com/upload"
        template = _RetryableMultipartRequestTemplate()
        composite = CompositeRequestTemplate(
            [
                template,
                _StaticTransitionTemplate(),
                _RetryableMultipartCleanupTemplate(template),
            ]
        )

        template.before_request(request)
        composite.after_response(request, response)

        request_id = id(request)
        assert request_id not in template._attempted_request_ids
        assert request_id not in template._responses_by_request_id
        assert request_id not in template._exceptions_by_request_id

    def test__retry_transition_after_response__preserves_saved_retry_state(self):
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "artifact": ("artifact.bin", io.BytesIO(b"artifact")),
                }
            },
        )
        response = Response()
        response.status_code = 503
        response.url = "https://example.com/upload"
        retry_transition = object()
        template = _RetryableMultipartRequestTemplate()
        composite = CompositeRequestTemplate(
            [
                template,
                _StaticTransitionTemplate(response_transition=retry_transition),
                _RetryableMultipartCleanupTemplate(template),
            ]
        )

        template.before_request(request)

        assert composite.after_response(request, response) is retry_transition

        request_id = id(request)
        assert request_id in template._attempted_request_ids
        assert template._responses_by_request_id[request_id] is response
        assert request_id not in template._exceptions_by_request_id

    def test__terminal_exception_after_retry_pipeline__clears_saved_retry_state(self):
        request = (
            "POST",
            "https://example.com/upload",
            {
                "files": {
                    "artifact": ("artifact.bin", io.BytesIO(b"artifact")),
                }
            },
        )
        exception = RuntimeError("boom")
        template = _RetryableMultipartRequestTemplate()
        composite = CompositeRequestTemplate(
            [
                template,
                _StaticTransitionTemplate(),
                _RetryableMultipartCleanupTemplate(template),
            ]
        )

        template.before_request(request)
        composite.after_exception(request, RuntimeError, exception, None)

        request_id = id(request)
        assert request_id not in template._attempted_request_ids
        assert request_id not in template._responses_by_request_id
        assert request_id not in template._exceptions_by_request_id

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


class TestRetryableMultipartRequestIntegration:
    @responses.activate
    def test__upload_with_unrewindable_stream_after_rate_limit__raises_original_api_exception(
        self,
    ):
        responses.post("https://example.com/upload", status=429)
        consumer = _MultipartRetryTestConsumer()

        with pytest.raises(ApiException) as exc_info:
            consumer.upload(
                artifact=(
                    "artifact.bin",
                    _FailingSeekStream(),
                    "application/octet-stream",
                )
            )

        assert exc_info.value.http_status_code == 429
        assert len(responses.calls) == 1

    @responses.activate
    def test__upload_with_rewindable_stream_after_rate_limit__retries_and_succeeds(
        self,
    ):
        request_bodies = []

        def response_callback(request):
            body = request.body
            if isinstance(body, str):
                body = body.encode("utf-8")
            request_bodies.append(body)

            if len(request_bodies) == 1:
                return (429, {}, "")
            return (200, {}, "ok")

        responses.add_callback(
            responses.POST,
            "https://example.com/upload",
            callback=response_callback,
        )
        consumer = _MultipartRetryTestConsumer()
        artifact_content = b"rewindable-artifact"

        consumer.upload(
            artifact=(
                "artifact.bin",
                io.BytesIO(artifact_content),
                "application/octet-stream",
            )
        )

        assert len(responses.calls) == 2
        last_response = cast(Any, responses.calls[-1]).response
        assert last_response is not None
        assert last_response.status_code == 200
        assert len(request_bodies) == 2
        assert artifact_content in request_bodies[0]
        assert artifact_content in request_bodies[1]
