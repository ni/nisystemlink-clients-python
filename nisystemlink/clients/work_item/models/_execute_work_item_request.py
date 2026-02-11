from nisystemlink.clients.core._uplink._json_model import JsonModel


class ExecuteWorkItemRequest(JsonModel):
    """Request for executing a work item action."""

    action: str
    """The action to execute on the work item."""
