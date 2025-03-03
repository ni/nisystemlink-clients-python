from typing import List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.systemsstate.models._state import (
    AdditionalStateInformation,
    StateMetaData,
)


class StateDescriptionListResponse(JsonModel):
    """Model for the response containing a list of state metadata."""

    error: Optional[ApiError] = None

    total_count: int
    """Gets or sets total count of states."""

    states: Optional[List[StateMetaData]] = None
    """An array of state metadata information."""


class StateResponse(StateMetaData, AdditionalStateInformation):
    """Model for system state object."""

    error: Optional[ApiError] = None

    contains_extra_operations: bool
    """Gets or sets whether the state contains extra operations in addition to feeds and packages."""
