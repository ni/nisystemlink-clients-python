# -*- coding: utf-8 -*-

"""Implementation of ApiException."""

import typing
from typing import Any, Dict

from nisystemlink.clients import core


class ApiException(Exception):
    """Represents errors that occur when calling SystemLink APIs."""

    def __init__(
        self,
        message: str | None = None,
        error: core.ApiError | None = None,
        http_status_code: int | None = None,
        inner: Exception | None = None,
        response_data: Dict[str, Any] | None = None,
    ) -> None:
        """Initialize an exception.

        Args:
            message: The message describing the error.
            error: The error returned by the API.
            http_status_code: The HTTP status code, if this exception was the result of
                an HTTP error.
            inner: The inner exception that caused the error.
            response_data: The full parsed JSON response body, if the server returned
                one. Useful when an error response still contains actionable data.
        """
        self._message = message
        self._error = error
        self._http_status_code = http_status_code
        self._inner = inner
        self._response_data = response_data

    @property
    def message(self) -> str | None:  # noqa:D401
        """The error message."""
        return self._message

    @property
    def error(self) -> core.ApiError | None:  # noqa: D401
        """The error information returned by the SystemLink API, or None if the API did
        not return one or the error occurred trying to call the API.
        """
        if self._error is None:
            return None
        else:
            return self._error.model_copy()

    @property
    def http_status_code(self) -> int | None:  # noqa: D401
        """The HTTP status code, if this exception was the result of an HTTP error."""
        return self._http_status_code

    @property
    def inner_exception(self) -> Exception | None:  # noqa: D401
        """The exception that caused this failure, if any."""
        return self._inner

    @property
    def response_data(self) -> Dict[str, Any] | None:  # noqa: D401
        """The full parsed JSON response body returned by the server, or None.

        This is populated for HTTP error responses that include a JSON body.
        It allows callers to recover structured data from error responses — for
        example, a partial-failure response may contain result data alongside the error details.
        """
        return dict(self._response_data) if self._response_data is not None else None

    def __str__(self) -> str:
        txt = self._message or "API exception occurred"
        if self._error:
            txt += "\n\n" + str(self._error)
        return txt

    def __eq__(self, other: object) -> bool:
        other_ = typing.cast(ApiException, other)
        return all(
            (
                isinstance(other, ApiException),
                self._message == other_._message,
                self._error == other_._error,
                self._http_status_code == other_._http_status_code,
                self._inner == other_._inner,
                self._response_data == other_._response_data,
            )
        )

    def __hash__(self) -> int:
        return hash((self._message, self._error, self._inner))
