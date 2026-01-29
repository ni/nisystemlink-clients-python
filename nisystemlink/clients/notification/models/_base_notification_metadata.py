from typing import Dict, List

from nisystemlink.clients.core._uplink._json_model import JsonModel


class BaseNotificationMetadata(JsonModel):
    id: str | None = None
    """identifier of this notification metadata"""

    interpreting_service_name: str
    """Gets or sets the name of the interpreting service.

    Example: "smtp"
    """

    display_name: str | None = None
    """Display name of the object.

    Example: "name"
    """

    properties: Dict[str, str] | None = None
    """Additional properties for the base metadata.

    Example: { "property": "value" }
    """

    referencing_notification_strategies: List[str] | None = None
    """List of strategies used for referencing,"""
