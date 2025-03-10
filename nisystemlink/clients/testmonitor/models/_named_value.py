from typing import Any

from nisystemlink.clients.core._uplink._json_model import JsonModel


class NamedValue(JsonModel):
    name: str
    """The name of the value."""

    value: Any
    """The value."""
