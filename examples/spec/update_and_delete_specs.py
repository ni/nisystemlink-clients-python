from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    QuerySpecificationsRequest,
    SpecificationDefinition,
    SpecificationType,
    UpdateSpecificationsRequest,
)

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = SpecClient(configuration=server_configuration)

# The query and delete examples assume you have created the specs from the query_specs example
product = "Amplifier"

# update spec1 to change the block to "modifiedBlock"
# query the original spec
response = client.query_specs(
    QuerySpecificationsRequest(product_ids=[product], filter='specId == "spec1"')
)
if response.specs:
    original_spec1 = response.specs[0]
    print(f"Original spec1 block: {original_spec1.block}")
    print(f"Original spec1 version: {original_spec1.version}")

# make the modifications
modified_spec = SpecificationDefinition(
    id=original_spec1.id,
    product_id=original_spec1.product_id,
    spec_id=original_spec1.spec_id,
    type=SpecificationType.FUNCTIONAL,
    keywords=["work", "reviewed"],
    block="modifiedBlock",
    version=original_spec1.version,
    workspace=original_spec1.workspace,
)
update_response = client.update_specs(
    specs=UpdateSpecificationsRequest(specs=[modified_spec])
)
if update_response and update_response.updated_specs:
    print(f"New spec1 version: {update_response.updated_specs[0].version}")

# query again to see new version
response = client.query_specs(
    QuerySpecificationsRequest(product_ids=[product], filter='specId == "spec1"')
)
if response.specs:
    original_spec1 = response.specs[0]
    print(f"Modified spec1 block: {original_spec1.block}")

# delete all the specs for the product
# query all specs
response = client.query_specs(QuerySpecificationsRequest(product_ids=[product]))
if response.specs:
    client.delete_specs(ids=[spec.id for spec in response.specs if spec.id])
