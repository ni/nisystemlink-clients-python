from __future__ import annotations

from typing import List, Optional

from nisystemlink.clients.core._uplink._with_paging import WithPaging

from ._webapp_models import WebApp


class PagedWebApps(WithPaging):
    """The response for a WebApp query containing the matched WebApps."""

    webapps: Optional[List[WebApp]] = None
    """
    List of webapps.
    """
