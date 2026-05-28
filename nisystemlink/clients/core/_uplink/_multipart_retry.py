from typing import Any, Callable, cast, TypeVar

from uplink import decorators
from uplink.clients.io.interfaces import RequestTemplate

F = TypeVar("F", bound=Callable[..., Any])


def _rewind_retryable_part(part: object) -> None:
    if hasattr(part, "seek"):
        cast(Any, part).seek(0)
        return

    if isinstance(part, tuple):
        for item in part:
            if hasattr(item, "seek"):
                cast(Any, item).seek(0)


class _RetryableMultipartRequestTemplate(RequestTemplate):
    def before_request(self, request: tuple[str, str, dict[str, Any]]) -> None:
        _, _, extras = request
        for part in extras.get("files", {}).values():
            _rewind_retryable_part(part)
        return None


class _RetryableMultipartRequest(decorators.MethodAnnotation):
    def modify_request(self, request_builder: Any) -> None:
        request_builder.add_request_template(_RetryableMultipartRequestTemplate())


def retryable_multipart_request() -> Callable[[F], F]:
    """Create a method decorator that rewinds multipart parts before each send."""

    def decorator(func: F) -> F:
        return _RetryableMultipartRequest()(func)  # type: ignore[return-value]

    return decorator
