from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._named_value import NamedValue
from nisystemlink.clients.testmonitor.models._step import Status
from nisystemlink.clients.testmonitor.models._step_data import StepData


class BaseStepRequest(JsonModel):
    step_id: str
    """Step ID."""

    result_id: str
    """Result ID."""

    parent_id: Optional[str] = None
    """Parent step ID."""

    data: Optional[StepData] = None
    """Data returned by the test step."""

    data_model: Optional[str] = None
    """Data model for the step."""

    started_at: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the test result began."""

    status: Optional[Status] = None
    """The status of the step."""

    step_type: Optional[str] = None
    """Step type."""

    total_time_in_seconds: Optional[float] = None
    """Total number of seconds the step took to execute."""

    inputs: Optional[List[NamedValue]] = None
    """Inputs and their values passed to the test."""

    outputs: Optional[List[NamedValue]] = None
    """Outputs and their values logged by the test."""

    keywords: Optional[List[str]] = None
    """Words or phrases associated with the step."""

    properties: Optional[Dict[str, str]] = None
    """Test step properties."""


class CreateStepRequest(BaseStepRequest):
    name: str
    """Step name."""

    children: Optional[List["CreateStepRequest"]] = None
    """Nested child steps."""
