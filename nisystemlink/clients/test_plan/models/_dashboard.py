from typing import Dict, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Dashboard(JsonModel):
    """Represents a dashboard reference."""

    id: Optional[str] = None
    """ID of the dashboard"""

    variables: Optional[Dict[str, str]] = None
    """Variables for the dashboard"""


class DashboardUrl(Dashboard):
    """Definition and URL of the dashboard reference associated with this test plan."""

    url: Optional[str] = None
    """URL of the dashboard reference associated with this test plan."""
