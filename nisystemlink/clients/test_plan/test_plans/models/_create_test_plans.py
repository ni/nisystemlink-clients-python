from typing import Dict, List, Optional

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel
from ...models._execution_definition import ExecutionDefinition
from ._test_plan import TestPlan


class Dashboard(JsonModel):
    """Represents a dashboard reference."""

    id: str
    """ID of the dashboard"""

    variables: Optional[Dict[str, str]] = None
    """Variables for the dashboard"""


class CreateTestPlanRequestBodyContent(JsonModel):
    """Represents the request body content for creating a test plan."""

    name: str
    """The name of the test plan."""

    templateId: Optional[str] = None
    """The ID of the template to use for the test plan."""

    state: str
    """The state of the test plan."""

    description: Optional[str] = None
    """A description of the test plan."""

    assignedTo: Optional[str] = None
    """The user or group assigned to the test plan."""

    workOrderId: Optional[str] = None
    """The work order ID associated with the test plan."""

    estimatedDurationInSeconds: Optional[int] = None
    """The estimated duration of the test plan in seconds."""

    properties: Optional[Dict[str, str]] = None
    """Additional properties for the test plan."""

    partNumber: str
    """The part number associated with the test plan."""

    dutId: Optional[str] = None
    """The Device Under Test (DUT) ID."""

    testProgram: Optional[str] = None
    """The test program associated with the test plan."""

    systemFilter: Optional[str] = None
    """The system filter to apply."""

    workspace: Optional[str] = None
    """The workspace associated with the test plan."""

    fileIdsFromTemplate: Optional[List[str]] = None
    """List of file IDs from the template."""

    dashboard: Optional[Dashboard] = None
    """The dashboard associated with the test plan."""

    executionActions: Optional[List[ExecutionDefinition]] = None
    """List of execution actions for the test plan."""


class CreateTestPlansRequest(JsonModel):
    """Represents the request body for creating multiple test plans."""

    testPlans: List[CreateTestPlanRequestBodyContent]
    """
    A list of test plan creation request bodies. Each item in the list contains 
    the content required to create an individual test plan.
    """


class CreateTestPlansResponse(JsonModel):
    """
    Represents the response from creating test plans, including successfully created,
    failed test plans, and any associated errors.
    """

    testPlans: Optional[List[TestPlan]] = None
    """List of all test plans involved in the operation."""

    createdTestPlans: Optional[List[TestPlan]] = None
    """List of test plans that were successfully created."""

    failedTestPlans: Optional[List[CreateTestPlanRequestBodyContent]] = None
    """List of test plans that failed to be created, with their request body content."""

    error: Optional[ApiError] = None
    """Error information if the operation encountered issues."""
