from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._named_value import NamedValue
from nisystemlink.clients.testmonitor.models._step import Status
from nisystemlink.clients.testmonitor.models._step_data import StepData


class BaseStepRequest(JsonModel):
    step_id: str | None
    """Step ID."""

    result_id: str
    """Result ID."""

    parent_id: str | None = None
    """Parent step ID."""

    data: StepData | None = None
    """Data returned by the test step."""

    data_model: str | None = None
    """Data model for the step."""

    started_at: datetime | None = None
    """ISO-8601 formatted timestamp indicating when the test result began."""

    status: Status | None = None
    """The status of the step."""

    step_type: str | None = None
    """Step type."""

    total_time_in_seconds: float | None = None
    """Total number of seconds the step took to execute."""

    inputs: List[NamedValue] | None = None
    """Inputs and their values passed to the test."""

    outputs: List[NamedValue] | None = None
    """Outputs and their values logged by the test."""

    keywords: List[str] | None = None
    """Words or phrases associated with the step."""

    properties: Dict[str, str] | None = None
    """Test step properties."""


class CreateStepRequest(BaseStepRequest):
    name: str
    """Step name."""

    children: List["CreateStepRequest"] | None = None
    """Nested child steps."""
