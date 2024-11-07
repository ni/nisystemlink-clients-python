from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.product import ProductClient
from nisystemlink.clients.product.models import (
    Product,
    ProductField,
    QueryProductsRequest,
    QueryProductValuesRequest,
)

name = "Example Name"
family = "Example Family"


def create_some_products():
    """Create two example products on your server."""
    new_products = [
        Product(
            part_number="Example 123 AA",
            name=name,
            family=family,
            keywords=["original keyword"],
            properties={"original property key": "yes"},
        ),
        Product(
            part_number="Example 123 AA1",
            name=name,
            family=family,
            keywords=["original keyword"],
            properties={"original property key": "original"},
        ),
    ]
    create_response = client.create_products(new_products)
    return create_response


# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = ProductClient(configuration=server_configuration)

# Get all the products using the continuation token in batches of 100 at a time.
response = client.get_products(take=100, return_count=True)
all_products = response.products
while response.continuation_token:
    response = client.get_products(
        take=100, continuation_token=response.continuation_token, return_count=True
    )
    all_products.extend(response.products)

create_response = create_some_products()

# use get for first product created
created_product = client.get_product(create_response.products[0].id)

# Query products without continuation
query_request = QueryProductsRequest(
    filter=f'family="{family}" && name="{name}"',
    return_count=True,
    order_by=ProductField.FAMILY,
)
response = client.query_products_paged(query_request)

# Update the first product that you just created and replace the keywords
updated_product = create_response.products[0]
updated_product.keywords = ["new keyword"]
updated_product.properties = {"new property key": "new value"}
update_response = client.update_products([create_response.products[0]], replace=True)

# Query for just the ids of products that match the family
values_query = QueryProductValuesRequest(
    filter=f'family="{family}"', field=ProductField.ID
)
values_response = client.query_product_values(query=values_query)

# delete each created product individually by id
for product in create_response.products:
    client.delete_product(product.id)

# Create some more and delete them with a single call to delete.
create_response = create_some_products()
client.delete_products([product.id for product in create_response.products])
