from typing import List, Optional

from nisystemlink.clients.core import ApiError

class DeleteTestPlansRequest:
    """Represents a request to delete one or more test plans."""

    ids: List[str]
    """List of test plan IDS of test plans to be deleted"""

class DeleteTestPlansResponse:
    """Response fields for delete test plans operation."""

    deletedTestPlanIds: Optional[List[str]] = None
    """List of test plan IDs that were successfully deleted."""

    failedTestPlanIds: Optional[List[str]] = None
    """List of test plan IDs that failed to be deleted."""

    error: Optional[ApiError] = None
    """Error information if the delete operation encountered issues."""
