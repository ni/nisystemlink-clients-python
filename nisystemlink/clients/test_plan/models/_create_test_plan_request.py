from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import Dashboard
from ._execution_definition import ExecutionDefinition


class CreateTestPlanRequest(JsonModel):
    """Represents the request body content for creating a test plan."""

    name: str | None = None
    """The name of the test plan."""

    state: str | None = None
    """The state of the test plan."""

    template_id: str | None = None
    """The ID of the template to use for the test plan."""

    description: str | None = None
    """A description of the test plan."""

    assigned_to: str | None = None
    """The user or group assigned to the test plan."""

    part_number: str | None = None
    """The part number associated with the test plan."""

    dut_id: str | None = None
    """The Device Under Test (DUT) ID."""

    dut_serial_number: str | None = None
    """The Device Under Test (DUT) serial number."""

    test_program: str | None = None
    """The test program associated with the test plan."""

    work_order_id: str | None = None
    """The work order ID associated with the test plan."""

    estimated_duration_in_seconds: int | None = None
    """The estimated duration of the test plan in seconds."""

    system_filter: str | None = None
    """The system filter to apply."""

    dut_filter: str | None = None
    """The DUT filter to apply."""

    execution_actions: List[ExecutionDefinition] | None = None
    """List of execution actions for the test plan."""

    file_ids_from_template: List[str] | None = None
    """List of file IDs from the template."""

    workspace: str | None = None
    """The workspace associated with the test plan."""

    properties: Dict[str, str] | None = None
    """Additional properties for the test plan."""

    dashboard: Dashboard | None = None
    """The dashboard associated with the test plan."""
