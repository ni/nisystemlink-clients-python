from typing import cast

from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateResultRequest,
    CreateStepRequest,
    Measurement,
    NamedValue,
    QueryStepsRequest,
    QueryStepValuesRequest,
    Status,
    StepData,
    StepField,
    StepIdResultIdPair,
    UpdateStepRequest,
)


def create_test_result():
    """Create example result on your server."""
    new_results = [
        CreateResultRequest(
            part_number="Example 123 AA",
            program_name="Example Name",
            host_name="Example Host",
            status=Status.PASSED(),
            keywords=["original keyword"],
            properties={"original property key": "yes"},
        )
    ]
    create_response = client.create_results(new_results)
    return create_response


# Server configuration is not required when used with SystemLink Client or run through Jupyter on SystemLink
server_configuration: HttpConfiguration | None = None

# To set up the server configuration to point to your instance of SystemLink Enterprise, uncomment
# the following lines and provide your server URI and API key.
# server_configuration = HttpConfiguration(
#     server_uri="https://yourserver.yourcompany.com",
#     api_key="",
# )

client = TestMonitorClient(configuration=server_configuration)

# create a result to attach the steps to
create_response = create_test_result()

# Create the step requests
result_id = cast(str, create_response.results[0].id)
step_requests = [
    CreateStepRequest(
        step_id="step1",
        name="step1",
        result_id=result_id,
        inputs=[
            NamedValue(name="Temperature", value="35"),
            NamedValue(name="Voltage", value="5"),
        ],
    ),
    CreateStepRequest(
        step_id="step2",
        name="step2",
        result_id=result_id,
    ),
]

# Create the steps
create_response = client.create_steps(steps=step_requests)
created_steps = create_response.steps
print(create_response)

# You can query steps based on any field using DynamicLinq syntax.
# These are just some representative examples.
# Query based on result id
query_response = client.query_steps(
    QueryStepsRequest(filter=f'resultId == "{result_id}"')
)
queried_steps = query_response.steps

# query step name using query step values
query_values_response = client.query_step_values(
    QueryStepValuesRequest(
        filter=f'resultId == "{result_id}"',
        field=StepField.NAME,
    )
)

# update the data of the step
# extra properties of the measurements will be converted to string if not already a string
update_response = client.update_steps(
    steps=[
        UpdateStepRequest(
            step_id=step.step_id,
            result_id=cast(str, step.result_id),
            data=StepData(
                text="My output string",
                parameters=[
                    Measurement(
                        name="Temperature",
                        status="Passed",
                        measurement="35",
                        lowLimit="30",
                        highLimit="40",
                        units="C",
                        comparisonType="Numeric",
                        spec_id="spec1",
                    )
                ],
            ),
        )
        for step in created_steps
    ]
)

# delete all steps at once
delete_response = client.delete_steps(
    steps=[
        StepIdResultIdPair(
            step_id=cast(str, step.step_id), result_id=cast(str, step.result_id)
        )
        for step in queried_steps
    ]
)

create_response = client.create_steps(steps=step_requests)
created_steps = create_response.steps

# delete steps one by one
for step in created_steps:
    if step.step_id and step.result_id:
        client.delete_step(result_id=step.result_id, step_id=step.step_id)
