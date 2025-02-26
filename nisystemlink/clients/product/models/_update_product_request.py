from nisystemlink.clients.product.models._product import Product


class UpdateProductRequest(Product):
    """This is the request model to update a product.

    It extends the Product model, which is generally used for creating a product. Besides, `id` is added
    as a field here. This is to infer which product to be updated.
    """

    id: str
    """The globally unique id of the product."""
