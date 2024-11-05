from __future__ import annotations

from typing import List

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._feed import Feed


class QueryFeedsResponse(JsonModel):
    """Query Feeds response."""

    feeds: List[Feed]
    """A collection of feeds"""
