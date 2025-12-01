from typing import Dict

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Dashboard(JsonModel):
    """Represents a dashboard reference."""

    id: str | None = None
    """ID of the dashboard"""

    variables: Dict[str, str] | None = None
    """Variables for the dashboard"""


class DashboardUrl(Dashboard):
    """Definition and URL of the dashboard reference associated with this test plan."""

    url: str | None = None
    """URL of the dashboard reference associated with this test plan."""
