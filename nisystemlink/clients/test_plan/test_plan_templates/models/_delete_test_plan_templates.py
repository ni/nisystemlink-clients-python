from typing import List, Optional
from nisystemlink.clients.core._api_error import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel

class DeleteTestPlanTemplates(JsonModel):
    """Deletes one or more test plan templates identified by their IDs."""

    ids: List[str]
    """ List of test plan template IDs to delete """

class DeleteTestPlanTemplatesResponseSuccess(JsonModel):
    deletedTestPlanTemplateIds: List[str]
    failedTestPlanTemplateIds: Optional[List[str]] = None
    error: Optional[ApiError] = None