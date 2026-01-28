from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class BaseNotificationMetadata(JsonModel):
    id: str | None = None
    """Gets or sets the ID"""

    interpreting_service_name: str | None = None
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    display_name: str | None = None
    """Gets or sets the display name.

    Example: "name"
    """

    properties: Dict[str, str] | None = None
    """Gets or sets the properties.

    Example: { "property": "value" }
    """

    referencing_notification_strategies: List[str] | None = None
    """Gets or sets the referencing notification strategies."""
