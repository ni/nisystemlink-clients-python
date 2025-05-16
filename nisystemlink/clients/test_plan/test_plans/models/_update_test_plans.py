from typing import List, Optional, Dict, Union

from nisystemlink.clients.core._uplink._json_model import JsonModel
from nisystemlink.clients.core import ApiError
from . import TestPlan


class UpdateTestPlanRequestBodyContent(JsonModel):
    """Represents the content for updating a single test plan."""

    id: str
    """The unique identifier of the test plan to update."""

    name: Optional[str] = None
    """The new name for the test plan."""

    state: Optional[str] = None
    """The new state of the test plan."""

    description: Optional[str] = None
    """The new description for the test plan."""

    dut_id: Optional[Union[str, None]] = None
    """The device under test (DUT) identifier."""

    part_number: Optional[str] = None
    """The part number associated with the test plan."""

    assigned_to: Optional[Union[str, None]] = None
    """The user or group assigned to the test plan."""

    test_program: Optional[Union[str, None]] = None
    """The test program associated with the test plan."""

    properties: Optional[Union[Dict[str, str], None]] = None
    """Additional properties for the test plan as key-value pairs."""

    workspace: Optional[Union[str, None]] = None
    """The workspace to which the test plan belongs."""

    work_order_id: Optional[Union[str, None]] = None
    """The work order identifier associated with the test plan."""

    file_ids_from_template: Optional[List[str]] = None
    """List of file IDs from the template to associate with the test plan."""


class UpdateTestPlansRequest(JsonModel):
    """Represents the request body for updating multiple test plans."""

    test_plans: List[UpdateTestPlanRequestBodyContent]
    """A list of test plans to update."""

    replace: Optional[bool] = None
    """Whether to replace the existing test plans or update them."""


class UpdateTestPlansResponse(JsonModel):
    """Represents the response after attempting to update test plans."""

    updated_test_plans: Optional[List[TestPlan]] = None
    """List of successfully updated test plans."""

    failed_test_plans: Optional[List[UpdateTestPlanRequestBodyContent]] = None
    """List of test plans that failed to update."""

    error: Optional[ApiError] = None
    """Error information if the update operation failed."""
