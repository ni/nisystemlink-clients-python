# mypy: disable-error-code = misc

from typing import Dict, Optional, Type

from nisystemlink.clients import core
from requests import JSONDecodeError, Response
from uplink import Consumer, dumps, response_handler

from ._json_model import JsonModel


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


@dumps.to_json(JsonModel)
def _deserialize_model(model_cls: Type[JsonModel], model_instance: JsonModel) -> Dict:
    """Turns a :class:`.JsonModel` instance into a dictionary for serialization."""
    return model_instance.dict(by_alias=True, exclude_unset=True)


class BaseClient(Consumer):
    """Base class for SystemLink clients, built on top of `Uplink <https://github.com/prkumar/uplink>`_."""

    def __init__(self, configuration: core.HttpConfiguration):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about how to connect.
        """
        super().__init__(
            base_url=configuration.server_uri,
            converter=_deserialize_model,
            hooks=[_handle_http_status],
        )
        if configuration.api_keys:
            self.session.headers.update(configuration.api_keys)
