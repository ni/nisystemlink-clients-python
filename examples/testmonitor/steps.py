from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateStepRequest,
    CreateStepsRequest,
    QueryStepsRequest,
    StepIdResultIdPair,
)
from nisystemlink.clients.testmonitor.models._query_steps_request import (
    QueryStepValuesRequest,
    StepField,
)
from nisystemlink.clients.testmonitor.models._step import NamedValueObject
from nisystemlink.clients.testmonitor.models._update_steps_request import (
    UpdateStepRequest,
    UpdateStepsRequest,
)

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = TestMonitorClient(configuration=server_configuration)

# Create the step requests
result_id = "4bef8c3c-afbf-400a-9d30-065dfb0b8d24"
step_requests = [
    CreateStepRequest(
        step_id="step1",
        name="step1",
        result_id=result_id,
        inputs=[
            NamedValueObject(name="Temperature", value="35"),
            NamedValueObject(name="Voltage", value="5"),
        ],
    ),
    CreateStepRequest(
        step_id="step2",
        name="step2",
        result_id=result_id,
    ),
]

# Create the steps
create_response = client.create_steps(CreateStepsRequest(steps=step_requests))
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

# update the name of a step
update_response = client.update_steps(
    UpdateStepsRequest(
        steps=[
            UpdateStepRequest(
                step_id=step.step_id,
                result_id=step.result_id,
                name="updated name",
            )
            for step in created_steps
        ]
    )
)

# delete all steps at once
delete_response = client.delete_steps(
    steps=[
        StepIdResultIdPair(step_id=step.step_id, result_id=step.result_id)
        for step in queried_steps
    ]
)

create_response = client.create_steps(CreateStepsRequest(steps=step_requests))
created_steps = create_response.steps

# delete steps one by one
for step in created_steps:
    if step.step_id and step.result_id:
        client.delete_step(result_id=step.result_id, step_id=step.step_id)
