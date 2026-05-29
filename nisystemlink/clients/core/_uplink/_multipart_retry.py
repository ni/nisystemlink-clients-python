"""Helpers for multipart requests that need retry-safe stream handling.

The decorator exported by this module is intended for multipart requests that may
be retried by Uplink. It preserves the caller's stream position on the initial
send, rewinds seekable multipart parts only on retry attempts, and aborts the
retry if any part cannot be rewound.

When a retry is aborted because a part cannot be rewound, the original response
or exception that triggered the retry is surfaced back through Uplink's normal
response and error handling pipeline instead of sending a malformed follow-up
request.
"""

import io
from enum import auto, Enum
from typing import Any, Callable, cast, TypeVar

from requests import Response
from uplink import decorators
from uplink.clients.io import transitions
from uplink.clients.io.interfaces import RequestTemplate

F = TypeVar("F", bound=Callable[..., Any])


class _RewindResult(Enum):
    REWOUND = auto()
    FAILED = auto()
    NOT_NEEDED = auto()


def _rewind_retryable_part(part: object) -> _RewindResult:
    """Rewind the first seekable multipart payload contained in ``part``.

    Returns ``_RewindResult.REWOUND`` when a multipart payload was successfully
    rewound to the start of the stream. Returns
    ``_RewindResult.FAILED`` when a stream payload appears to need rewinding but
    rejects it. Returns ``_RewindResult.NOT_NEEDED`` when the part contains no
    stream payload that requires rewinding, such as simple string fields.
    """
    if hasattr(part, "seek"):
        seekable = getattr(part, "seekable", None)
        if callable(seekable):
            try:
                if not cast(Any, seekable)():
                    return _RewindResult.FAILED
            except (OSError, io.UnsupportedOperation):
                return _RewindResult.FAILED

        try:
            cast(Any, part).seek(0)
        except (OSError, io.UnsupportedOperation):
            return _RewindResult.FAILED
        return _RewindResult.REWOUND

    if isinstance(part, tuple):
        for item in part:
            rewind_result = _rewind_retryable_part(item)
            if rewind_result is not _RewindResult.NOT_NEEDED:
                return rewind_result

    return _RewindResult.NOT_NEEDED


def _get_saved_retry_action(
    response: Response | None,
    exception_info: tuple[type[BaseException], BaseException, Any] | None,
) -> Any:
    """Return the original retry-triggering failure as an Uplink transition."""
    if response is not None:
        return transitions.finish(response)

    if exception_info is not None:
        return transitions.fail(*exception_info)

    return None


class _RetryableMultipartRequestTemplate(RequestTemplate):
    """Track multipart retry state and rewind streams only for retry sends.

    The first request attempt is left untouched so callers can intentionally
    provide streams positioned away from offset 0. On later attempts, each file
    part must be rewound to the beginning before the request is sent again.

    If rewinding fails for any part, the retry is cancelled and the original
    response or exception that caused the retry is returned to Uplink so normal
    error handling can surface it to the caller.
    """

    def __init__(self) -> None:
        self._attempted_request_ids: set[int] = set()
        self._responses_by_request_id: dict[int, Response] = {}
        self._exceptions_by_request_id: dict[
            int, tuple[type[BaseException], BaseException, Any]
        ] = {}

    def _clear_request_state(self, request_id: int) -> None:
        self._attempted_request_ids.discard(request_id)
        self._responses_by_request_id.pop(request_id, None)
        self._exceptions_by_request_id.pop(request_id, None)

    def before_request(self, request: tuple[str, str, dict[str, Any]]) -> Any:
        _, _, extras = request
        request_id = id(request)
        if request_id not in self._attempted_request_ids:
            self._attempted_request_ids.add(request_id)
            return None

        for part in extras.get("files", {}).values():
            if _rewind_retryable_part(part) is _RewindResult.FAILED:
                retry_action = _get_saved_retry_action(
                    self._responses_by_request_id.get(request_id),
                    self._exceptions_by_request_id.get(request_id),
                )
                self._clear_request_state(request_id)
                return retry_action
        return None

    def after_response(
        self, request: tuple[str, str, dict[str, Any]], response: Response
    ) -> None:
        request_id = id(request)
        self._responses_by_request_id[request_id] = response
        self._exceptions_by_request_id.pop(request_id, None)
        return None

    def after_exception(
        self,
        request: tuple[str, str, dict[str, Any]],
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: Any,
    ) -> None:
        request_id = id(request)
        self._exceptions_by_request_id[request_id] = (exc_type, exc_val, exc_tb)
        self._responses_by_request_id.pop(request_id, None)
        return None


class _RetryableMultipartCleanupTemplate(RequestTemplate):
    def __init__(self, retry_template: _RetryableMultipartRequestTemplate) -> None:
        self._retry_template = retry_template

    def after_response(
        self, request: tuple[str, str, dict[str, Any]], response: Response
    ) -> None:
        self._retry_template._clear_request_state(id(request))
        return None

    def after_exception(
        self,
        request: tuple[str, str, dict[str, Any]],
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: Any,
    ) -> None:
        self._retry_template._clear_request_state(id(request))
        return None


class _RetryableMultipartRequest(decorators.MethodAnnotation):
    def modify_request(self, request_builder: Any) -> None:
        retryable_template = _RetryableMultipartRequestTemplate()
        # Insert ahead of Uplink's retry template so this helper can see the
        # original retry-triggering response/exception and short-circuit future
        # attempts when a multipart stream cannot be rewound safely.
        request_builder._request_templates.insert(0, retryable_template)
        request_builder._request_templates.append(
            _RetryableMultipartCleanupTemplate(retryable_template)
        )


def retryable_multipart_request() -> Callable[[F], F]:
    """Create a decorator for multipart requests with retry-safe stream handling.

    Behavior:
    - The initial send preserves the caller-provided stream position.
        - Retry attempts rewind seekable multipart payloads back to offset 0.
        - Multipart fields that do not contain streams, such as simple strings, are
            left alone and do not block retries.
    - If a retry attempt cannot rewind a payload, the retry is cancelled and the
      original retry-triggering response or exception is surfaced.
    """

    def decorator(func: F) -> F:
        return _RetryableMultipartRequest()(func)  # type: ignore[return-value]

    return decorator
