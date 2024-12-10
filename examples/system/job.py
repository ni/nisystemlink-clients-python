from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.system import SystemClient
from nisystemlink.clients.system.models import (
    CancelJobRequest,
    CreateJobRequest,
    JobState,
    QueryJobsRequest,
)

# Setup the server configuration to point to your instance of SystemLink Enterprise
server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = SystemClient(configuration=server_configuration)

# Get all jobs that have succeeded
jobs = client.list_jobs(
    system_id="system_id",
    jid="jid",
    state=JobState.SUCCEEDED,
    function="function",
    skip=0,
    take=10,
)

# Create a job
arg = [["A description"]]
tgt = ["HVM_domU--SN-ec200972-eeca-062e-5bf5-017a25451b39--MAC-0A-E1-20-D6-96-2B"]
fun = ["system.set_computer_desc"]
metadata = {"queued": True, "refresh_minion_cache": {"grains": True}}
job = CreateJobRequest(
    arguments=arg,
    target_systems=tgt,
    functions=fun,
    metadata=metadata,
)

create_job_response = client.create_job(job)

# Get job summary
job_summary = client.get_job_summary()

# Query jobs
query_job = QueryJobsRequest(
    skip=0,
    take=1000,
    filter="result.success.Contains(false)",
    projection="new(id,jid,state,lastUpdatedTimestamp,metadata.queued as queued)",
    orderBy="createdTimestamp descending",
)
query_jobs_response = client.query_jobs(query_job)


# Cancel a job
cancel_job_request = CancelJobRequest(id=create_job_response.id, tgt=tgt[0])
cancel_job_response = client.cancel_jobs([cancel_job_request])
