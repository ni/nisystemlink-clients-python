from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.testmonitor.models._named_value import NamedValue
from nisystemlink.clients.testmonitor.models._status import Status
from nisystemlink.clients.testmonitor.models._step_data import StepData


class Step(JsonModel):
    name: Optional[str] = None
    """The name of the step."""

    step_type: Optional[str] = None
    """The type of the step."""

    step_id: Optional[str] = None
    """The ID of the step."""

    parent_id: Optional[str] = None
    """The ID of the parent step."""

    result_id: Optional[str] = None
    """The ID of the result associated with the step."""

    path: Optional[str] = None
    """The path of the step."""

    path_ids: Optional[List[str]] = None
    """The IDs of the steps in the path."""

    status: Optional[Status] = None
    """The status of the step."""

    total_time_in_seconds: Optional[int] = None
    """The total time in seconds the step took to execute."""

    started_at: Optional[datetime] = None
    """The ISO-8601 formatted timestamp indicating when the step started."""

    updated_at: Optional[datetime] = None
    """The ISO-8601 formatted timestamp indicating when the step was last updated."""

    inputs: Optional[List[NamedValue]] = None
    """Inputs and their values passed to the test."""

    outputs: Optional[List[NamedValue]] = None
    """Outputs and their values logged by the test."""

    data_model: Optional[str] = None
    """Custom string defining the model of the data object."""

    data: Optional[StepData] = None
    """Data returned by the test step."""

    has_children: Optional[bool] = None
    """Indicates if the step has child steps."""

    workspace: Optional[str] = None
    """The workspace the test step belongs to."""

    keywords: Optional[List[str]] = None
    """Words or phrases associated with the test step."""

    properties: Optional[Dict[str, str]] = None
    """Test step properties."""
