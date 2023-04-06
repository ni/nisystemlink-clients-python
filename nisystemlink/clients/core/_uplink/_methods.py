"""Wrappers around uplink HTTP decorators with proper type annotations."""

from typing import Any, Callable, Optional, Sequence, Tuple, TypeVar, Union

from uplink import (
    Body,
    commands,
    json,
    response_handler as uplink_response_handler,
    returns,
)

F = TypeVar("F", bound=Callable[..., Any])


def get(path: str, args: Optional[Sequence[Any]] = None) -> Callable[[F], F]:
    """Annotation for a GET request."""

    def decorator(func: F) -> F:
        return commands.get(path, args=args)(func)  # type: ignore

    return decorator


def post(
    path: str,
    args: Optional[Sequence[Any]] = None,
    return_key: Optional[Union[str, Tuple[str, ...]]] = None,
) -> Callable[[F], F]:
    """Annotation for a POST request with a JSON request body. If args is not
    specified, defaults to a single argument that represents the request body.
    """

    def decorator(func: F) -> F:
        result = json(commands.post(path, args=args or (Body,))(func))
        if return_key:
            result = returns.json(key=return_key)(result)
        return result  # type: ignore

    return decorator


def patch(path: str, args: Optional[Sequence[Any]] = None) -> Callable[[F], F]:
    """Annotation for a PATCH request with a JSON request body."""

    def decorator(func: F) -> F:
        return json(commands.patch(path, args=args)(func))  # type: ignore

    return decorator


def delete(path: str, args: Optional[Sequence[Any]] = None) -> Callable[[F], F]:
    """Annotation for a DELETE request."""

    def decorator(func: F) -> F:
        return commands.delete(path, args=args)(func)  # type: ignore

    return decorator


def response_handler(
    handler: Any, requires_consumer: Optional[bool] = False
) -> Callable[[F], F]:
    """Annotation for creating custom response handlers."""

    def decorator(func: F) -> F:
        return uplink_response_handler(handler, requires_consumer)(func)  # type: ignore

    return decorator
