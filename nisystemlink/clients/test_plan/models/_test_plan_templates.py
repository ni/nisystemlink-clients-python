from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._dashboard import Dashboard
from ._execution_definition import ExecutionDefinition


class TestPlanTemplateBase(JsonModel):
    """Contains information about a test plan template."""

    name: Optional[str] = None
    """Name of the test plan template."""

    template_group: Optional[str] = None
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
    systems capable of executing test plans created from this template.
    """

    dut_filter: Optional[str] = None
    """The LINQ filter string is used to filter the potential list of
    DUTs capable of executing test plans created from this template.
    """

    execution_actions: Optional[List[ExecutionDefinition]] = None
    """Defines the executions that will be used for test plan actions
    created from this template.
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


class TestPlanTemplate(TestPlanTemplateBase):
    """Contains response information for test plan template."""

    __test__ = False

    id: Optional[str] = None
    """The globally unique id of the test plan template."""

    name: Optional[str] = None
    """Name of the test plan template."""

    created_by: Optional[str] = None
    """ID of the user who created the test plan template."""

    updated_by: Optional[str] = None
    """ID of the user who most recently updated the test plan template."""

    created_at: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the
    test plan template was created."""

    updated_at: Optional[datetime] = None
    """ISO-8601 formatted timestamp indicating when the
    test plan template was most recently updated."""
