# -*- coding: utf-8 -*-

"""Implementation of ApiError."""

from typing import List

from ._uplink._json_model import JsonModel


class ApiError(JsonModel):
    """Represents the standard error structure for SystemLink API responses."""

    name: str | None = None
    """String error code."""

    code: int | None = None
    """Numeric error code."""

    message: str | None = None
    """Complete error message."""

    args: List[str] = []
    """Positional arguments for the error code."""

    resource_type: str | None = None
    """Type of resource associated with the error."""

    resource_id: str | None = None
    """Identifier of the resource associated with the error."""

    inner_errors: List["ApiError"] = []
    """Inner errors when the top-level error represents more than one error."""
