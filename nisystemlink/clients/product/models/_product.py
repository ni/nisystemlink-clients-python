from datetime import datetime
from typing import Dict, List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel


class Product(JsonModel):
    """Contains information about a product."""

    id: Optional[str]
    """The globally unique id of the product."""

    part_number: Optional[str]
    """The part number is the unique identifier of a product within a single org.

    Usually the part number refers to a specific revision or version of a given product."""

    name: Optional[str]
    """The name of the product.

    Usually the name is used to refer to several part numbers that all have the same name but
    different revisions or versions.
    """

    family: Optional[str]
    """The family that that this product belongs to.

    Usually the family is a grouping above product name. A family usually has multiple product
    names within it.
    """

    updated_at: Optional[datetime]
    """The last time that this product was updated."""

    file_ids: Optional[List[str]]
    """A list of file ids that are attached to this product."""

    keywords: Optional[List[str]]
    """A list of keywords that categorize this product."""

    properties: Optional[Dict[str, str]]
    """A list of custom properties for this product."""

    workspace: Optional[str]
    """The id of the workspace that this product belongs to."""
