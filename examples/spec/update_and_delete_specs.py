from typing import cast

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    MeasurementMappingItem,
    QuerySpecificationsRequest,
    SpecificationType,
    UpdateSpecificationsRequest,
    UpdateSpecificationsRequestObject,
)

# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = SpecClient(configuration=server_configuration)

# The query and delete examples assume you have created the specs from the query_specs example
product = "Amplifier"

# update spec1 to change the block to "modifiedBlock" and spec2 to set a measurement mapping,
# both in a single request
# query the original specs
spec_filter = 'specId == "spec1" || specId == "spec2"'
response = client.query_specs(
    QuerySpecificationsRequest(product_ids=[product], filter=spec_filter)
)
original_specs = {spec.spec_id: spec for spec in response.specs or []}
if "spec1" in original_specs and "spec2" in original_specs:
    original_spec1 = original_specs["spec1"]
    original_spec2 = original_specs["spec2"]
    print(f"Original spec1 block: {original_spec1.block}")
    print(f"Original spec1 version: {original_spec1.version}")

    # make the modifications
    modified_spec1 = UpdateSpecificationsRequestObject(
        id=cast(str, original_spec1.id),
        product_id=cast(str, original_spec1.product_id),
        spec_id=cast(str, original_spec1.spec_id),
        type=SpecificationType.FUNCTIONAL,
        keywords=["work", "reviewed"],
        block="modifiedBlock",
        version=cast(int, original_spec1.version),
        workspace=cast(str, original_spec1.workspace),
    )
    modified_spec2 = UpdateSpecificationsRequestObject(
        id=cast(str, original_spec2.id),
        product_id=cast(str, original_spec2.product_id),
        spec_id=cast(str, original_spec2.spec_id),
        type=SpecificationType.PARAMETRIC,
        measurement_mapping=[
            MeasurementMappingItem(
                filter='data.parameters.Any(it["name"] == "Input Voltage")',
                result_filter='partNumber == "VR5678"',
            )
        ],
        version=cast(int, original_spec2.version),
        workspace=cast(str, original_spec2.workspace),
    )
    update_response = client.update_specs(
        specs=UpdateSpecificationsRequest(specs=[modified_spec1, modified_spec2])
    )
    if update_response and update_response.updated_specs:
        for updated_spec in update_response.updated_specs:
            print(f"New {updated_spec.spec_id} version: {updated_spec.version}")

# query again to see the new versions
response = client.query_specs(
    QuerySpecificationsRequest(product_ids=[product], filter=spec_filter)
)
modified_specs = {spec.spec_id: spec for spec in response.specs or []}
if "spec1" in modified_specs and "spec2" in modified_specs:
    print(f"Modified spec1 block: {modified_specs['spec1'].block}")
    print(
        "Modified spec2 measurement mapping: "
        f"{modified_specs['spec2'].measurement_mapping}"
    )

# delete all the specs for the product
# query all specs
response = client.query_specs(QuerySpecificationsRequest(product_ids=[product]))
if response.specs:
    client.delete_specs(ids=[spec.id for spec in response.specs if spec.id])
