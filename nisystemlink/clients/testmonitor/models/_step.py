from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._named_value import NamedValue
from nisystemlink.clients.testmonitor.models._status import Status
from nisystemlink.clients.testmonitor.models._step_data import StepData


class Step(JsonModel):
    name: str | None = None
    """The name of the step."""

    step_type: str | None = None
    """The type of the step."""

    step_id: str | None = None
    """The ID of the step."""

    parent_id: str | None = None
    """The ID of the parent step."""

    result_id: str | None = None
    """The ID of the result associated with the step."""

    path: str | None = None
    """The path of the step."""

    path_ids: List[str] | None = None
    """The IDs of the steps in the path."""

    status: Status | None = None
    """The status of the step."""

    total_time_in_seconds: float | None = None
    """The total time in seconds the step took to execute."""

    started_at: datetime | None = None
    """The ISO-8601 formatted timestamp indicating when the step started."""

    updated_at: datetime | None = None
    """The ISO-8601 formatted timestamp indicating when the step was last updated."""

    inputs: List[NamedValue] | None = None
    """Inputs and their values passed to the test."""

    outputs: List[NamedValue] | None = None
    """Outputs and their values logged by the test."""

    data_model: str | None = None
    """Custom string defining the model of the data object."""

    data: StepData | None = None
    """Data returned by the test step."""

    has_children: bool | None = None
    """Indicates if the step has child steps."""

    workspace: str | None = None
    """The workspace the test step belongs to."""

    keywords: List[str] | None = None
    """Words or phrases associated with the test step."""

    properties: Dict[str, str] | None = None
    """Test step properties."""
