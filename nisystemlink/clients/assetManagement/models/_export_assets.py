from enum import Enum
from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class ResponseFormat(Enum):
    """Gets or sets the return type. Valid option is "CSV"."""

    CSV = "CSV"


class Destination(Enum):
    """Gets or sets the destination of the request."""

    DOWNLOAD = "DOWNLOAD"
    """Returns the list of resources as the body of the response and it should be downloaded as a file."""

    FILE_SERVICE = "FILE_SERVICE"
    """Sends the list of resources to the file ingestion service and returns the ID of the file in a JSON object."""


class ExportAssetsRequest(JsonModel):

    filter: Optional[str] = None
    """Gets or sets the filter criteria for assets. Consists of a string of queries composed using AND/OR operators."""

    response_format: ResponseFormat
    """Gets or sets the return type. Valid option is "CSV"."""

    destination: Destination
    """Gets or sets the destination of the request."""

    file_ingestion_workspace: Optional[str] = None
    """Gets or sets the ID of the workspace to put the file into, if the destination is "FILE_SERVICE"."""


class ExportAssetsResponse(JsonModel):

    file_id: Optional[str] = None
    """Gets or sets file identifier in the file ingestion service."""
