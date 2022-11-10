from devtools import debug
from nisystemlink.clients.core import HttpConfiguration
from nisystemlink.clients.dataframe import DataFrameClient

client = DataFrameClient(
    HttpConfiguration(
        "https://api-stratus-test.ion.ni.com/",
        "mlbKyhlWtrLiRL9ui56boz9rLrfcjE6F5D55BgsF3e",
    )
)

debug(client.api_info())
