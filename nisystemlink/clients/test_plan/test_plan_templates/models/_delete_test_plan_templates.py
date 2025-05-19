from typing import List, Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

class DeleteTestPlanTemplates(JsonModel):
    """Deletes one or more test plan templates identified by their IDs."""

    ids: List[str]
    """ List of test plan template IDs to delete """

class DeleteTestPlanTemplatesPartialSuccess(JsonModel):
    """The result of deleting multiple test plan templates when one or more test plan templates could not be deleted."""

    deletedTestPlanTemplateIds: List[str]
    """The IDs of the test plan template that could not be deleted."""

    failedTestPlanTemplateIds: Optional[List[str]] = None
    """The IDs of the test plan template that could not be deleted."""

    error: Optional[ApiError] = None
    """The error that occurred when deleting the test plan template."""
