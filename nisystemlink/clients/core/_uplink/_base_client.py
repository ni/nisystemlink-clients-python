# mypy: disable-error-code = misc

from typing import Callable, cast, NoReturn, Optional

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
    try:
        content = response.json()
        if isinstance(content, dict) and "error" in content:
            error = core.ApiError.from_json_dict(content["error"])
            raise core.ApiException(error=error, http_status_code=response.status_code)
        else:
            cast(Callable[[], NoReturn], response.raise_for_status)()
    except JSONDecodeError:
        cast(Callable[[], NoReturn], response.raise_for_status)()


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
