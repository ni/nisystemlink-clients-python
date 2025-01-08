from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.systemsstate.models._architecture_enum import Architecture
from nisystemlink.clients.systemsstate.models._distribution_enum import Distribution
from nisystemlink.clients.systemsstate.models._feed import Feed
from nisystemlink.clients.systemsstate.models._package import Package
from nisystemlink.clients.systemsstate.models._system_image import SystemImage


class State(JsonModel):
    """Basic State entities that can be extended further"""

    name: Optional[str] = None
    """Gets or sets the name of the state."""

    description: Optional[str] = None
    """Gets or sets the description of the state."""

    distribution: Distribution
    """Gets or sets supported distribution by a state."""

    architecture: Architecture
    "Gets or sets supported architecture by a state."

    properties: Optional[Dict[str, Optional[str]]] = None
    """Gets or sets the custom properties for a state."""

    workspace: Optional[str]
    """Gets or sets the ID of the workspace.

    This property is available starting with version 3 of the getStates operation.
    """


class StateMetaData(State):
    """Model for state metadata information."""

    id: Optional[str] = None
    """Gets or sets the ID of the state."""

    createdTimestamp: datetime
    """Gets or sets ISO-8601 formatted timestamp specifying the state creation date."""

    lastUpdatedTimestamp: datetime
    """Gets or sets ISO-8601 formatted timestamp specifying the last date that the state was updated."""


class AdditionalStateInformation(JsonModel):
    """Encompasses the feeds, systemImage and packages associated with a particular state"""

    feeds: Optional[List[Feed]] = None
    """List of all feeds associated with the particular state"""

    systemImage: SystemImage
    """Object defining a system image containing the name and version"""

    packages: Optional[List[Package]] = None
    """List of all packages associated with the particular state"""
