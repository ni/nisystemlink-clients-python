from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class PackageMetadata(JsonModel):
    """Package Meta data."""

    package_name: Optional[str] = None
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
    file_name: Optional[str] = None
    """The file name of the package. Depending on the selected platform,
    the following package extensions are available:
    .nipkg for windows feeds, .ipk and .deb for ni-linux-rt feeds."""
    homepage: Optional[str] = None
    """The website of the maintainers for the package."""
    installed_size: Optional[int] = None
    """The size of the package after install."""
    maintainer: Optional[str] = None
    """The maintainer of the package (name and email address)."""
    predepends: Optional[List[str]] = None
    """Information about other packages this package predepends."""
    priority: Optional[int] = None
    """The priority of the package."""
    provides: Optional[List[str]] = None
    """Information about other packages that this package provides."""
    recommends: Optional[List[str]] = None
    """Information about other packages this package recommends."""
    release_notes: Optional[str] = None
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
    file_name: Optional[str] = None
    """The name of the file in this package."""
    feed_id: Optional[str] = None
    """The ID of the feed this package is associated with."""
    workspace: Optional[str] = None
    """The ID of the workspace this package belongs to.
    The workspace of a package is the workspace of feed this package is associated with."""
    updated_at: Optional[datetime] = None
    """The date of the latest package update."""
    created_at: Optional[datetime] = None
    """The date when the package was created at."""
    metadata: Optional[PackageMetadata] = None
    """Package meta data."""
