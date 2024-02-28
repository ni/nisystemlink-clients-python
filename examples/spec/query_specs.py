from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    Condition,
    ConditionRange,
    ConditionType,
    CreateSpecificationRequestObject,
    CreateSpecificationsRequest,
    NumericConditionValue,
    QuerySpecificationsRequest,
    SpecificationLimit,
    SpecificationType,
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
        type=SpecificationType.PARAMETRIC,
        category="Parametric Specs",
        name="output voltage",
        limit=SpecificationLimit(min=1.2, max=1.5),
        unit="mV",
    ),
    CreateSpecificationRequestObject(
        product_id=product,
        spec_id="spec2",
        type=SpecificationType.PARAMETRIC,
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
            ),
            Condition(
                name="Supply Voltage",
                value=NumericConditionValue(
                    condition_type=ConditionType.NUMERIC,
                    discrete=[1.3, 1.5, 1.7],
                    unit="mV",
                ),
            ),
        ],
    ),
    CreateSpecificationRequestObject(
        product_id=product,
        spec_id="spec3",
        type=SpecificationType.FUNCTIONAL,
        category="Noise Thresholds",
        name="noise",
    ),
]

# Create the specs on the server
client.create_specs(CreateSpecificationsRequest(specs=spec_requests))

# You can query specs based on any field using DynamicLinq syntax.
# These are just some representative examples.

response = client.query_specs(QuerySpecificationsRequest(productIds=[product]))
all_product_specs = response.specs

# Query based on spec id
response = client.query_specs(
    QuerySpecificationsRequest(product_ids=[product], filter='specId == "spec2"')
)
if response.specs:
    spec2 = response.specs[0]

# Query based on name
response = client.query_specs(
    QuerySpecificationsRequest(product_ids=[product], filter='name.Contains("voltage")')
)
voltage_specs = response.specs

# Query based on Category
response = client.query_specs(
    QuerySpecificationsRequest(
        product_ids=[product], filter='category == "Noise Thresholds"'
    )
)
noise_category = response.specs
print(noise_category)
