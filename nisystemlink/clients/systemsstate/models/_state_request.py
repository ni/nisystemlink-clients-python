from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.systemsstate.models._state import (
    AdditionalStateInformation,
    State,
)
from nisystemlink.clients.systemsstate.models._state_id_version_pair import (
    StateIDVersionPair,
)


class StateRequest(State, AdditionalStateInformation):
    """Model for system state object."""


class ExportStateRequest(JsonModel):
    """Contains identifying information of the state to export."""

    inline: Optional[bool] = None
    """Gets or sets whether to return the state data inline or as an attachment.

    When the inline is true, the Content-Disposition header is set to 'inline'.
    When the inline is not specified or is false, the state contents are handled as a download.

    The Content-Disposition header is set to 'attachment' and the MIME type is set to text/x-yaml; charset=UTF-8.
    """

    state: StateIDVersionPair
    """Contains the stateID and state_version"""


class ExportStateFromSystemRequest(JsonModel):
    """Contains the system id from which to export the state."""

    inline: Optional[bool] = None
    """Gets or sets whether to return the state data inline or as an attachment.

    When the inline is true, the Content-Disposition header is set to 'inline'.
    When the inline is not specified or is false, the state contents are handled as a download.

    The Content-Disposition header is set to 'attachment' and the MIME type is set to text/x-yaml; charset=UTF-8.
    """

    systemID: Optional[str] = None
    """Gets or sets system ID."""
