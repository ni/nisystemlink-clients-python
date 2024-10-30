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
    """The name of the feed."""
    description: Optional[str] = None
    """The description of the feed."""
    platform: Platform
    """The platform of the feed, the following package extensions are available: .nipkg for
    windows feeds, .ipk and .deb for ni-linux-rt feeds."""
    workspace: Optional[str] = None
    """The ID of the workspace this feed belongs to. If the workspace is not defined,
    the default workspace is used."""


class Feed(JsonModel):
    """Feed model."""

    id: Optional[str] = None
    """The auto-generated ID of the feed."""
    name: Optional[str] = None
    """The name of the feed."""
    description: Optional[str] = None
    """The description of the feed."""
    platform: Platform
    """The platform of the feed, the following package extensions are available: .nipkg for
    windows feeds, .ipk and .deb for ni-linux-rt feeds.
    """
    workspace: Optional[str] = None
    """The ID of the workspace this feed belongs to."""
    updated_at: str = Field(alias="updatedAt")
    """The date of the latest feed update"""
    created_at: str = Field(alias="createdAt")
    """The date when the feed was created at."""
    package_sources: Optional[List[str]] = Field(default=None, alias="packageSources")
    """The package sources list of the feed."""
    deleted: bool
    """Whether the feed deletion was requested."""


class QueryFeedsResponse(JsonModel):
    """Query Feeds response."""

    feeds: List[Feed]
    """A collection of feeds"""


class PackageMetadata(JsonModel):
    """Package Meta data."""

    package_name: Optional[str] = Field(default=None, alias="packageName")
    """The name of the package."""
    version: Optional[str] = None
    """The version number of the package."""
    architecture: Optional[str] = None
    """The architecture of the package."""
    breaks: Optional[List[str]] = None
    """Information about other packages this package breaks."""
    conflicts: Optional[List[str]] = None
    """Information about other packages this package conflicts with."""
    depends: Optional[List[str]] = None
    """Information about other packages this package depends on."""
    description: Optional[str] = None
    """The description of the package."""
    enhances: Optional[List[str]] = None
    """Information about other packages this package enchances."""
    essential: Optional[bool] = None
    """True if the package is essential."""
    file_name: Optional[str] = Field(default=None, alias="fileName")
    """The file name of the package. Depending on the selected platform,
    the following package extensions are available:
    .nipkg for windows feeds, .ipk and .deb for ni-linux-rt feeds."""
    homepage: Optional[str] = None
    """The website of the maintainers for the package."""
    installed_size: Optional[int] = Field(default=None, alias="installedSize")
    """The size of the package after install."""
    maintainer: Optional[str] = None
    """The maintainer of the package (name and email address)."""
    predepends: Optional[List[str]] = None
    """Information about other packages this package predepends."""
    priority: int
    """The priority of the package."""
    provides: Optional[List[str]] = None
    """Information about other packages that this package provides."""
    recommends: Optional[List[str]] = None
    """Information about other packages this package recommends."""
    release_notes: Optional[str] = Field(default=None, alias="releaseNotes")
    """The release notes of the package."""
    replaces: Optional[List[str]] = None
    """Information about other packages this package replaces."""
    section: Optional[str] = None
    """The application area of the package."""
    size: Optional[int] = None
    """The size (in bytes) of the package."""
    source: Optional[str] = None
    """The source of the package."""
    suggests: Optional[List[str]] = None
    """Information about other packages this package suggests."""
    tags: Optional[str] = None
    """The tags of the package."""
    attributes: Optional[Dict[str, str]] = None
    """The attributes of the package."""


class Package(JsonModel):
    """Package model."""

    id: Optional[str] = None
    """Gets or sets the ID of this package. This is used to reference this package in the service."""
    file_name: Optional[str] = Field(default=None, alias="fileName")
    """The name of the file in this package."""
    feed_id: Optional[str] = Field(default=None, alias="feedId")
    """The ID of the feed this package is associated with."""
    workspace: Optional[str] = None
    """The ID of the workspace this package belongs to.
    The workspace of a package is the workspace of feed this package is associated with."""
    updated_at: str = Field(alias="updatedAt")
    """The date of the latest package update."""
    created_at: str = Field(alias="createdAt")
    """The date when the package was created at."""
    metadata: Optional[PackageMetadata] = None
    """Package meta data."""
