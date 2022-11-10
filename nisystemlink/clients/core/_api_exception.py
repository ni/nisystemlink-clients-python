# -*- coding: utf-8 -*-

"""Implementation of ApiException."""

import typing
from typing import Optional

from nisystemlink.clients import core


class ApiException(Exception):
    """Represents errors that occur when calling SystemLink APIs."""

    def __init__(
        self,
        message: Optional[str] = None,
        error: Optional[core.ApiError] = None,
        http_status_code: Optional[int] = None,
        inner: Optional[Exception] = None,
    ) -> None:
        """Initialize an exception.

        Args:
            message: The message describing the error.
            error: The error returned by the API.
            http_status_code: The HTTP status code, if this exception was the result of
                an HTTP error.
            inner: The inner exception that caused the error.
        """
        self._message = message
        self._error = error
        self._http_status_code = http_status_code
        self._inner = inner

    @property
    def message(self) -> Optional[str]:  # noqa:D401
        """The error message."""
        return self._message

    @property
    def error(self) -> Optional[core.ApiError]:  # noqa: D401
        """The error information returned by the SystemLink API, or None if the API did
        not return one or the error occurred trying to call the API.
        """
        if self._error is None:
            return None
        else:
            return self._error.copy()

    @property
    def http_status_code(self) -> Optional[int]:  # noqa: D401
        """The HTTP status code, if this exception was the result of an HTTP error."""
        return self._http_status_code

    @property
    def inner_exception(self) -> Optional[Exception]:  # noqa: D401
        """The exception that caused this failure, if any."""
        return self._inner

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
            )
        )

    def __hash__(self) -> int:
        return hash((self._message, self._error, self._inner))
