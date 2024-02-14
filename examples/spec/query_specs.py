from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    Condition,
    ConditionRange,
    ConditionType,
    CreateSpecificationRequestObject,
    CreateSpecificationsRequest,
    NumericConditionValue,
    SpecificationLimit,
    Type,
)

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = SpecClient(configuration=server_configuration)

# Create the spec requests
product = "Amplifier"
spec_requests = [
    CreateSpecificationRequestObject(
        product_id=product,
        spec_id="spec1",
        type=Type.PARAMETRIC,
        category="Parametric Specs",
        name="output voltage",
        limit=SpecificationLimit(min=1.2, max=1.5),
        unit="mV",
    ),
    CreateSpecificationRequestObject(
        product_id=product,
        spec_id="spec2",
        type=Type.PARAMETRIC,
        category="Parametric Specs",
        name="input voltage",
        limit=SpecificationLimit(min=0.02, max=0.15),
        unit="mV",
        conditions=[
            Condition(
                name="Temperature",
                value=NumericConditionValue(
                    condition_type=ConditionType.NUMERIC,
                    range=[ConditionRange(min=-25, step=20, max=85)],
                    unit="C",
                ),
            )
        ],
    ),
    CreateSpecificationRequestObject(
        product_id=product,
        spec_id="spec3",
        type=Type.FUNCTIONAL,
        category="Noise Thresholds",
        name="noise",
    ),
]

# Create the specs on the server
response = client.create_specs(CreateSpecificationsRequest(specs=spec_requests))
