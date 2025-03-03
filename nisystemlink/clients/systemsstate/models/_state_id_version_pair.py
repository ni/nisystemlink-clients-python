from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class StateIDVersionPair(JsonModel):

    stateID: Optional[str] = None
    """Gets or sets the ID of the state."""

    state_version: Optional[str] = None
    """Gets or sets the version of the state.

    The latest package/feed set of the state will be used if the version is not specified.
    """
