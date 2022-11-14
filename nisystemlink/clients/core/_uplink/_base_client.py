# mypy: disable-error-code = misc

from typing import Optional

from nisystemlink.clients import core
from requests import JSONDecodeError, Response
from uplink import Consumer, response_handler


@response_handler
def _handle_http_status(response: Response) -> Optional[Response]:
    """Checks an HTTP response's status code and raises an exception if necessary."""
    if 200 <= response.status_code < 300:
        # Return None for "204 No Content" responses.
        if response.status_code == 204:
            return None
        return response

    msg = "Server responded with <{} {}> ({}).".format(
        response.status_code, response.reason, response.url
    )

    try:
        content = response.json()
        if content and "error" in content:
            err_obj = core.ApiError.from_json_dict(content["error"])
        else:
            err_obj = None

        raise core.ApiException(
            msg, error=err_obj, http_status_code=response.status_code
        )
    except JSONDecodeError:
        if response.text:
            msg += ":\n\n" + response.text
        raise core.ApiException(msg, http_status_code=response.status_code)


class BaseClient(Consumer):
    """Base class for SystemLink clients, built on top of `Uplink <https://github.com/prkumar/uplink>`_."""

    def __init__(self, configuration: core.HttpConfiguration):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about how to connect.
        """
        super().__init__(base_url=configuration.server_uri, hooks=[_handle_http_status])
        if configuration.api_keys:
            self.session.headers.update(configuration.api_keys)
