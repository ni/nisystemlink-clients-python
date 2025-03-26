"""Example to demonstrate disabling TLS/SSL certificate verification for connections"""

from nisystemlink.clients.core import HttpConfigurationManager
from nisystemlink.clients.file import FileClient

# explicitly get the http config and set the verify option
http_config = HttpConfigurationManager.get_configuration()
http_config.verify = False

client = FileClient(configuration=http_config)
print(client.api_info())
