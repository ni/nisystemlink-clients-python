from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._status import Status


class UpdateResultRequest(JsonModel):
    """Contains information about a result."""

    status: Status | None = None
    """The status of the result."""

    started_at: datetime | None = None
    """The time that the result started."""

    program_name: str | None = None
    """The name of the program that generated this result."""

    id: str
    """The globally unique id of the result."""

    system_id: str | None = None
    """The id of the system that generated this result."""

    host_name: str | None = None
    """The name of the host that generated this result."""

    part_number: str | None = None
    """The part number is the unique identifier of a product within a single org."""

    serial_number: str | None = None
    """The serial number of the system that generated this result."""

    total_time_in_seconds: float | None = None
    """The total time that the result took to run in seconds."""

    keywords: List[str] | None = None
    """A list of keywords that categorize this result."""

    properties: Dict[str, str | None] | None = None
    """A list of custom properties for this result."""

    operator: str | None = None
    """The operator that ran the result."""

    file_ids: List[str] | None = None
    """A list of file ids that are attached to this result."""

    data_table_ids: List[str] | None = None
    """A list of data table ids that are attached to this result."""

    workspace: str | None = None
    """The id of the workspace that this product belongs to."""
