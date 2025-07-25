from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import Dashboard
from ._execution_definition import ExecutionDefinition


class CreateTestPlanRequest(JsonModel):
    """Represents the request body content for creating a test plan."""

    name: Optional[str] = None
    """The name of the test plan."""

    state: Optional[str] = None
    """The state of the test plan."""

    template_id: Optional[str] = None
    """The ID of the template to use for the test plan."""

    description: Optional[str] = None
    """A description of the test plan."""

    assigned_to: Optional[str] = None
    """The user or group assigned to the test plan."""

    part_number: Optional[str] = None
    """The part number associated with the test plan."""

    dut_id: Optional[str] = None
    """The Device Under Test (DUT) ID."""

    dut_serial_number: Optional[str] = None
    """The Device Under Test (DUT) serial number."""

    test_program: Optional[str] = None
    """The test program associated with the test plan."""

    work_order_id: Optional[str] = None
    """The work order ID associated with the test plan."""

    estimated_duration_in_seconds: Optional[int] = None
    """The estimated duration of the test plan in seconds."""

    system_filter: Optional[str] = None
    """The system filter to apply."""

    dut_filter: Optional[str] = None
    """The DUT filter to apply."""

    execution_actions: Optional[List[ExecutionDefinition]] = None
    """List of execution actions for the test plan."""

    file_ids_from_template: Optional[List[str]] = None
    """List of file IDs from the template."""

    workspace: Optional[str] = None
    """The workspace associated with the test plan."""

    properties: Optional[Dict[str, str]] = None
    """Additional properties for the test plan."""

    dashboard: Optional[Dashboard] = None
    """The dashboard associated with the test plan."""
