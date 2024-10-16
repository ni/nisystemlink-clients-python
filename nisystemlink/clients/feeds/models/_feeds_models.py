"""Models utilized for Feeds in SystemLink."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class Platform(Enum):
    """Platform."""

    WINDOWS = "WINDOWS"
    NI_LINUX_RT = "NI_LINUX_RT"


class CreateFeedRequest(JsonModel):
    """Create Feed Request."""

    name: str
    description: Optional[str] = None
    platform: Platform
    workspace: Optional[str] = None


class CreateOrUpdateFeedResponse(JsonModel):
    """Create or Update Feed Response."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    platform: Platform
    workspace: Optional[str] = None
    updated_at: str = Field(alias="updatedAt")
    created_at: str = Field(alias="createdAt")
    package_sources: Optional[List[str]] = Field(default=None, alias="packageSources")
    deleted: bool


class FeedsQueryResponse(JsonModel):
    """Query Feeds response."""

    feeds: List[CreateOrUpdateFeedResponse]


class PackageMetadata(JsonModel):
    """Package Meta data."""

    package_name: Optional[str] = Field(default=None, alias="packageName")
    version: Optional[str] = None
    architecture: Optional[str] = None
    breaks: Optional[List[str]] = None
    conflicts: Optional[List[str]] = None
    depends: Optional[List[str]] = None
    description: Optional[str] = None
    enhances: Optional[List[str]] = None
    essential: Optional[bool] = None
    file_name: Optional[str] = Field(default=None, alias="fileName")
    homepage: Optional[str] = None
    installed_size: Optional[int] = Field(default=None, alias="installedSize")
    maintainer: Optional[str] = None
    predepends: Optional[List[str]] = None
    priority: int
    provides: Optional[List[str]] = None
    recommends: Optional[List[str]] = None
    release_notes: Optional[str] = Field(default=None, alias="releaseNotes")
    replaces: Optional[List[str]] = None
    section: Optional[str] = None
    size: Optional[int] = None
    source: Optional[str] = None
    suggests: Optional[List[str]] = None
    tags: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None


class UploadPackageResponse(JsonModel):
    """Upload package response."""

    id: Optional[str] = None
    file_name: Optional[str] = Field(default=None, alias="fileName")
    feed_id: Optional[str] = Field(default=None, alias="feedId")
    workspace: Optional[str] = None
    updated_at: str = Field(alias="updatedAt")
    created_at: str = Field(alias="createdAt")
    metadata: Optional[PackageMetadata] = None
