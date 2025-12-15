from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class UpdateTestPlanRequest(JsonModel):
    """Represents the content for updating a single test plan."""

    id: str
    """The unique identifier of the test plan to update."""

    name: str | None = None
    """The new name for the test plan."""

    state: str | None = None
    """The new state of the test plan."""

    description: str | None = None
    """The new description for the test plan."""

    dut_id: str | None = None
    """The device under test (DUT) identifier."""

    part_number: str | None = None
    """The part number associated with the test plan."""

    assigned_to: str | None = None
    """The user or group assigned to the test plan."""

    test_program: str | None = None
    """The test program associated with the test plan."""

    properties: Dict[str, str] | None = None
    """Additional properties for the test plan as key-value pairs."""

    workspace: str | None = None
    """The workspace to which the test plan belongs."""

    work_order_id: str | None = None
    """The work order identifier associated with the test plan."""

    file_ids_from_template: List[str] | None = None
    """List of file IDs from the template to associate with the test plan."""
