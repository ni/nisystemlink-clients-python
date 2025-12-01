from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class PackageMetadata(JsonModel):
    """Package Meta data."""

    package_name: str | None = None
    """The name of the package."""
    version: str | None = None
    """The version number of the package."""
    architecture: str | None = None
    """The architecture of the package."""
    breaks: List[str] | None = None
    """Information about other packages this package breaks."""
    conflicts: List[str] | None = None
    """Information about other packages this package conflicts with."""
    depends: List[str] | None = None
    """Information about other packages this package depends on."""
    description: str | None = None
    """The description of the package."""
    enhances: List[str] | None = None
    """Information about other packages this package enchances."""
    essential: bool | None = None
    """True if the package is essential."""
    file_name: str | None = None
    """The file name of the package. Depending on the selected platform,
    the following package extensions are available:
    .nipkg for windows feeds, .ipk and .deb for ni-linux-rt feeds."""
    homepage: str | None = None
    """The website of the maintainers for the package."""
    installed_size: int | None = None
    """The size of the package after install."""
    maintainer: str | None = None
    """The maintainer of the package (name and email address)."""
    predepends: List[str] | None = None
    """Information about other packages this package predepends."""
    priority: int | None = None
    """The priority of the package."""
    provides: List[str] | None = None
    """Information about other packages that this package provides."""
    recommends: List[str] | None = None
    """Information about other packages this package recommends."""
    release_notes: str | None = None
    """The release notes of the package."""
    replaces: List[str] | None = None
    """Information about other packages this package replaces."""
    section: str | None = None
    """The application area of the package."""
    size: int | None = None
    """The size (in bytes) of the package."""
    source: str | None = None
    """The source of the package."""
    suggests: List[str] | None = None
    """Information about other packages this package suggests."""
    tags: str | None = None
    """The tags of the package."""
    attributes: Dict[str, str] | None = None
    """The attributes of the package."""


class Package(JsonModel):
    """Package model."""

    id: str | None = None
    """Gets or sets the ID of this package. This is used to reference this package in the service."""
    file_name: str | None = None
    """The name of the file in this package."""
    feed_id: str | None = None
    """The ID of the feed this package is associated with."""
    workspace: str | None = None
    """The ID of the workspace this package belongs to.
    The workspace of a package is the workspace of feed this package is associated with."""
    updated_at: datetime | None = None
    """The date of the latest package update."""
    created_at: datetime | None = None
    """The date when the package was created at."""
    metadata: PackageMetadata | None = None
    """Package meta data."""
