from typing import Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class QuerySystemsRequest(JsonModel):
    """Model for query systems request."""

    skip: Optional[int] = None
    """Gets or sets the number of systems to skip."""

    take: Optional[int] = None
    """Gets or sets number of systems to return maximum value is 1000."""

    filter: Optional[str] = None
    """The systems query filter is dynamic LINQ format.

    `id` : String representing the ID of the system.
    `createdTimestamp`: ISO-8601 formatted timestamp string specifying the
    date when the system was registered.
    `lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system was updated.
    `alias`: String representing the alias of the system.
    `activation.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system activation was updated.
    `activation.data.activated`: Boolean representing whether the system is
    activated or not.
    `activation.data.licenseName`: String representing the name of the license.
    `activation.data.licenseVersion`: String representing the license version.
    `connected.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system connection was updated.
    `connected.data.state`: String representing the state of the system.
    `grains.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system grains were updated.
    `grains.data`: Dictionary of string to object representing general
    information about the system. Example: grains.data.os == "Windows"
    `packages.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system installed packages were updated.
    `packages.data`: Dictionary representing software packages installed on the
    system.
    Example: packages.data.ni-package-manager-upgrader.version: String
    representing the installed version of ni-package-manager-upgrader package.
    `feeds.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system configured feeds were updated.
    `feeds.data`: Dictionary representing the feeds configured on the system.
    `keywords.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system keywords were updated.
    `keywords.data`: Array of strings representing the keywords of the system.
    Example: keywords.data.Contains("test")
    `properties.lastUpdatedTimestamp`: ISO-8601 formatted timestamp string
    specifying the last date the system properties were updated.
    `properties.data`: Dictionary of string to string representing metadata
    information about a system. Example: properties.data.owner == "admin"
    `status.data.http_connected`: Boolean representing the status of the http
    connection to the master.

    See [Dynamic Linq](https://github.com/ni/systemlink-OpenAPI-documents/wiki/Dynamic-Linq-Query-Language)
    documentation for more details.

    `"@0"`, `"@1"` etc. can be used in conjunction with the `substitutions` parameter to keep this
    query string more simple and reusable."""

    projection: Optional[str] = None
    """Gets or sets specifies the projection for resources.
    Use this field to receive specific properties of the model."""

    order_by: Optional[str] = None
    """Gets or sets the order in which data returns."""
