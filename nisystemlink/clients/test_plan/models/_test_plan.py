from datetime import datetime
from typing import Dict, List, Optional

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

    template_id: Optional[str] = None
    """The identifier of the template used to create the test plan."""

    name: Optional[str] = None
    """The name of the test plan."""

    state: Optional[State] = None
    """The current state of the test plan."""

    substate: Optional[str] = None
    """The substate of the test plan, if any."""

    description: Optional[str] = None
    """The description of the test plan."""

    assigned_to: Optional[str] = None
    """The user or group assigned to the test plan."""

    work_order_id: Optional[str] = None
    """The identifier of the associated work order."""

    work_order_name: Optional[str] = None
    """The name of the associated work order."""

    part_number: Optional[str] = None
    """The part number associated with the test plan."""

    dut_id: Optional[str] = None
    """The identifier of the device under test (DUT)."""

    dut_serial_number: Optional[str] = None
    """The serial number of the device under test (DUT)."""

    test_program: Optional[str] = None
    """The test program associated with the test plan."""

    workspace: Optional[str] = None
    """The workspace to which the test plan belongs."""

    created_by: Optional[str] = None
    """The user who created the test plan."""

    updated_by: Optional[str] = None
    """The user who last updated the test plan."""

    system_id: Optional[str] = None
    """The identifier of the system used for the test plan."""

    fixture_ids: Optional[List[str]] = None
    """The list of fixture identifiers associated with the test plan."""

    planned_start_date_time: Optional[datetime] = None
    """The planned start date and time for the test plan."""

    estimated_end_date_time: Optional[datetime] = None
    """The estimated end date and time for the test plan."""

    estimated_duration_in_seconds: Optional[float] = None
    """The estimated duration of the test plan in seconds."""

    system_filter: Optional[str] = None
    """The filter used to select systems for the test plan."""

    dut_filter: Optional[str] = None
    """The filter used to select DUTs for the test plan."""

    created_at: Optional[datetime] = None
    """The date and time when the test plan was created."""

    updated_at: Optional[datetime] = None
    """The date and time when the test plan was last updated."""

    properties: Optional[Dict[str, str]] = None
    """Additional properties associated with the test plan."""

    file_ids_from_template: Optional[List[str]] = None
    """The list of file identifiers inherited from the template."""

    dashboard: Optional[DashboardUrl] = None
    """The dashboard data related to the test plan."""

    execution_actions: Optional[List[ExecutionDefinition]] = None
    """The execution actions defined for the test plan."""

    execution_history: Optional[List[ExecutionEvent]] = None
    """The execution history of the test plan."""

    dashboard_url: Optional[Dict[str, str]] = None
    """The URLs for dashboards related to the test plan."""
