from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import DashboardUrl
from ._execution_definition import ExecutionDefinition
from ._execution_event import ExecutionEvent
from ._state import State


class TestPlan(JsonModel):
    """Contains information about a test plan."""

    __test__ = False

    id: str
    """The unique identifier of the test plan."""

    template_id: str | None = None
    """The identifier of the template used to create the test plan."""

    name: str | None = None
    """The name of the test plan."""

    state: State | None = None
    """The current state of the test plan."""

    substate: str | None = None
    """The substate of the test plan, if any."""

    description: str | None = None
    """The description of the test plan."""

    assigned_to: str | None = None
    """The user or group assigned to the test plan."""

    work_order_id: str | None = None
    """The identifier of the associated work order."""

    work_order_name: str | None = None
    """The name of the associated work order."""

    part_number: str | None = None
    """The part number associated with the test plan."""

    dut_id: str | None = None
    """The identifier of the device under test (DUT)."""

    dut_serial_number: str | None = None
    """The serial number of the device under test (DUT)."""

    test_program: str | None = None
    """The test program associated with the test plan."""

    workspace: str | None = None
    """The workspace to which the test plan belongs."""

    created_by: str | None = None
    """The user who created the test plan."""

    updated_by: str | None = None
    """The user who last updated the test plan."""

    system_id: str | None = None
    """The identifier of the system used for the test plan."""

    fixture_ids: List[str] | None = None
    """The list of fixture identifiers associated with the test plan."""

    planned_start_date_time: datetime | None = None
    """The planned start date and time for the test plan."""

    estimated_end_date_time: datetime | None = None
    """The estimated end date and time for the test plan."""

    estimated_duration_in_seconds: float | None = None
    """The estimated duration of the test plan in seconds."""

    system_filter: str | None = None
    """The filter used to select systems for the test plan."""

    dut_filter: str | None = None
    """The filter used to select DUTs for the test plan."""

    created_at: datetime | None = None
    """The date and time when the test plan was created."""

    updated_at: datetime | None = None
    """The date and time when the test plan was last updated."""

    properties: Dict[str, str] | None = None
    """Additional properties associated with the test plan."""

    file_ids_from_template: List[str] | None = None
    """The list of file identifiers inherited from the template."""

    dashboard: DashboardUrl | None = None
    """The dashboard data related to the test plan."""

    execution_actions: List[ExecutionDefinition] | None = None
    """The execution actions defined for the test plan."""

    execution_history: List[ExecutionEvent] | None = None
    """The execution history of the test plan."""

    dashboard_url: Dict[str, str] | None = None
    """The URLs for dashboards related to the test plan."""
