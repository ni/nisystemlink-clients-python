from typing import Optional, Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel
from ._state import State
from ._workflow_definition import WorkflowDefinition
from ._execution_event import ExecutionEvent
from ...models._execution_definition import ExecutionDefinition

class TestPlan(JsonModel):
    """Contains information about a test plan."""

    id: str
    """The unique identifier of the test plan."""

    templateId: Optional[str] = None
    """The identifier of the template used to create the test plan."""
    
    name: str
    """The name of the test plan."""

    state: State
    """The current state of the test plan."""

    substate: Optional[str] = None
    """The substate of the test plan, if any."""

    description: Optional[str] = None
    """The description of the test plan."""

    assignedTo: Optional[str] = None
    """The user or group assigned to the test plan."""

    workOrderId: Optional[str] = None
    """The identifier of the associated work order."""

    workOrderName: Optional[str] = None
    """The name of the associated work order."""

    workspace: str
    """The workspace to which the test plan belongs."""

    createdBy: str
    """The user who created the test plan."""

    updatedBy: str
    """The user who last updated the test plan."""

    createdAt: str
    """The date and time when the test plan was created."""

    updatedAt: str
    """The date and time when the test plan was last updated."""

    properties: Dict[str, str]
    """Additional properties associated with the test plan."""

    partNumber: str
    """The part number associated with the test plan."""

    dutId: Optional[str] = None
    """The identifier of the device under test (DUT)."""

    testProgram: Optional[str] = None
    """The test program associated with the test plan."""

    systemId: Optional[str] = None
    """The identifier of the system used for the test plan."""

    fixtureIds: List[str] = None
    """The list of fixture identifiers associated with the test plan."""

    systemFilter: Optional[str] = None
    """The filter used to select systems for the test plan."""

    plannedStartDateTime: Optional[str] = None
    """The planned start date and time for the test plan."""

    estimatedEndDateTime: Optional[str] = None
    """The estimated end date and time for the test plan."""

    estimatedDurationInSeconds: Optional[float] = None
    """The estimated duration of the test plan in seconds."""

    fileIdsFromTemplate: List[str]
    """The list of file identifiers inherited from the template."""

    executionActions: Optional[ExecutionDefinition] = None
    """The execution actions defined for the test plan."""

    executionHistory: Optional[ExecutionEvent] = None
    """The execution history of the test plan."""

    dashboardUrl: Optional[Dict[str, str]] = None
    """The URLs for dashboards related to the test plan."""

    dashboard: Optional[Dict[str, str]] = None
    """The dashboard data related to the test plan."""

    workflow: WorkflowDefinition
    """The workflow definition associated with the test plan."""
