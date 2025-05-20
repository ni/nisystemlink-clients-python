from typing import Dict, List, Optional
from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.test_plan.models._execution_definition import (
    ExecutionDefinition,
)


class Dashboard(JsonModel):
    """Contains information about a reference of a dashboard linked to test plan template."""

    id: Optional[str] = None
    """The globally unique id of the dashboard."""

    variables: Dict[str, str]
    """Dictionary of variables set on the dashboard.
    These will be appended to the URL as query parameters.
    Each key will be prefixed with "var-" and the value will be the value of the variable.
    """


class TestPlanTemplateBase(JsonModel):
    """Contains information about a test plan template."""

    name: str
    """Name of the test plan template."""

    template_group: str = None
    """The template group defined by the user."""

    product_families: Optional[List[str]] = None
    """Array of product families to which the test plan template belongs."""

    part_numbers: Optional[List[str]] = None
    """Array of part numbers of the products to which the test plan template belongs."""

    summary: Optional[str] = None
    """Summary of the test plan template."""

    description: Optional[str] = None
    """Description of the test plan created from this template."""

    test_program: Optional[str] = None
    """Test program name of the test plan created from this template."""

    estimated_duration_in_seconds: Optional[int] = None
    """The estimated time in seconds for executing the test plan created from this template."""

    system_filter: Optional[str] = None
    """The LINQ filter string is used to filter the potential list of 
    systems capable of executing test plans created from this template."""

    execution_actions: Optional[List[ExecutionDefinition]] = None
    """Defines the executions that will be used for test plan actions created from this template.
    """

    file_ids: Optional[List[str]] = None
    """Array of file IDs associated with the test plan template."""

    workspace: Optional[str] = None
    """ID of the workspace where the test plan template belongs.
    Default workspace will be taken if the value is not given.
    """

    properties: Optional[Dict[str, str]] = None
    """Properties of the test plan created from this template as key-value pairs."""

    dashboard: Optional[Dashboard] = None
    """Defines a dashboard reference for a test plan."""


class TestPlanTemplateResponse(TestPlanTemplateBase):
    """Contains response information for test plan template."""

    id: Optional[str] = None
    """The globally unique id of the test plan template."""

    name: Optional[str] = None
    """Name of the test plan template."""
