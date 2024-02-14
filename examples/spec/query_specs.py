from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    CreateSpecificationRequestObject,
    CreateSpecificationsRequest,
    Type,
)

product = "TestProduct"
spec_documents = [
    {
        "specId": "spec1",
        "name": "output voltage",
        "type": Type.FUNCTIONAL,
        "category": "ParametricSpecs",
    },
    {
        "specId": "spec2",
        "name": "noise",
        "type": Type.FUNCTIONAL,
        "category": "Noise Thresholds",
    },
    {
        "specId": "spec3",
        "name": "input voltage",
        "type": Type.FUNCTIONAL,
        "category": "ParametricSpecs",
    },
]
spec_requests = []
for spec in spec_documents:
    new_spec = CreateSpecificationRequestObject(
        product_id=product,
        spec_id=spec["specId"],
        type=spec["type"],
        category=spec["category"],
        name=spec["name"],
    )
    spec_requests.append(new_spec)

client = SpecClient()

client.create_specs(CreateSpecificationsRequest(specs=spec_requests))
