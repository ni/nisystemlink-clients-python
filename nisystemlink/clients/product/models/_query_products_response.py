from typing import Optional

from nisystemlink.clients.product.models._product import Product


class QueryProductsResponse(Product):
    """This model extends the Product model and converts any non-optional fields into optional fields.

    This is because when we are using query products' projection, user can request for any of the available
    fields. So, we are making sure that all the available fields are optional.
    """

    part_number: Optional[str]  # type: ignore[assignment]
