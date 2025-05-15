from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement.models import QueryAssetRequest
from nisystemlink.clients.core._http_configuration import HttpConfiguration

server_configuration = HttpConfiguration(
    server_uri="https://yourserver.yourcompany.com",
    api_key="YourAPIKeyGeneratedFromSystemLink",
)
client = AssetManagementClient(configuration=server_configuration)

# Query assets using id.
queryRequest = QueryAssetRequest(
    ids=["asset_ids"],
    skip=0,
    take=1,
    descending=False,
    calibratable_only=False,
    returnCount=False,
)
queryResponse = client.query_assets(queryRequest)
