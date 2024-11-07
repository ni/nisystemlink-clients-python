from __future__ import annotations

from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._feed import Feed


class QueryFeedsResponse(JsonModel):
    """Query Feeds response."""

    feeds: Optional[List[Feed]] = None
    """A collection of feeds"""
