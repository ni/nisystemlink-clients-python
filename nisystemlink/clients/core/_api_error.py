# -*- coding: utf-8 -*-

"""Implementation of ApiError."""

from typing import List, Optional

from ._uplink._json_model import JsonModel


class ApiError(JsonModel):
    """Represents the standard error structure for SystemLink API responses."""

    name: Optional[str] = None
    """String error code."""

    code: Optional[int] = None
    """Numeric error code."""

    message: Optional[str] = None
    """Complete error message."""

    args: List[str] = []
    """Positional arguments for the error code."""

    resource_type: Optional[str] = None
    """Type of resource associated with the error."""

    resource_id: Optional[str] = None
    """Identifier of the resource associated with the error."""

    inner_errors: List["ApiError"] = []
    """Inner errors when the top-level error represents more than one error."""
