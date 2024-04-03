from typing import List


from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteSpecificationsRequest(JsonModel):
    """The request to delete a specification."""

    ids: List[str]
    """Global IDs of the specifications to delete."""


class DeleteSpecificationsPartialSuccess(JsonModel):
    """The results of deleting multiple specs when one or more of the specs could not be deleted."""

    deleted_spec_ids: List[str]
    """Global IDs of the deleted specifications."""

    failed_spec_ids: List[str]
    """Global IDs of the specifications that could not be deleted."""

    error: ApiError
