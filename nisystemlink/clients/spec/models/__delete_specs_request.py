from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import Extra, Field

from nisystemlink.clients.core import ApiError
from nisystemlink.clients.core._uplink._json_model import JsonModel


class DeleteSpecificationsRequest(JsonModel):
    class Config:
        extra = Extra.forbid

    ids: List[str]
    """
    Global IDs of the specifications to delete.
    """


class DeleteSpecificationsPartialSuccessResponse(JsonModel):
    class Config:
        extra = Extra.forbid

    deleted_spec_ids: Optional[List[str]] = Field(None, alias="deletedSpecIds")
    """
    Global IDs of the deleted specifications.
    """
    failed_spec_ids: Optional[List[str]] = Field(None, alias="failedSpecIds")
    """
    Global IDs of the specifications that could not be deleted.
    """
    error: Optional[ApiError] = None
