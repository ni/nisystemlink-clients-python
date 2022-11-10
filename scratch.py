from systemlink.clients import core, dataframe

config = core.HttpConfiguration("https://api-stratus-test.ion.ni.com/", "mlbKyhlWtrLiRL9ui56boz9rLrfcjE6F5D55BgsF3e")
client = dataframe.DataFrameClient(config)
print(client.api_info())