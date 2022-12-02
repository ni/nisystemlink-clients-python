# mypy: disable-error-code = misc

from json import loads
from typing import Any, Callable, Dict, get_origin, Optional, Type, Union

from nisystemlink.clients import core
from pydantic import parse_obj_as
from requests import JSONDecodeError, Response
from uplink import commands, Consumer, converters, response_handler, utils

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
            err_obj = core.ApiError.parse_obj(content["error"])
        else:
            err_obj = None

        raise core.ApiException(
            msg, error=err_obj, http_status_code=response.status_code
        )
    except JSONDecodeError:
        if response.text:
            msg += ":\n\n" + response.text
        raise core.ApiException(msg, http_status_code=response.status_code)


class _JsonModelConverter(converters.Factory):
    def create_request_body_converter(
        self, _class: Type, _: commands.RequestDefinition
    ) -> Optional[Callable[[JsonModel], Dict]]:
        def encoder(model: JsonModel) -> Dict:
            return loads(model.json(by_alias=True, exclude_unset=True))

        if utils.is_subclass(_class, JsonModel):
            return encoder
        else:
            return None

    def create_response_body_converter(
        self, _class: Type, _: commands.RequestDefinition
    ) -> Optional[Callable[[Response], Any]]:
        def decoder(response: Response) -> Any:
            try:
                data = response.json()
            except AttributeError:
                data = response

            return parse_obj_as(_class, data)

        if get_origin(_class) is Union or utils.is_subclass(_class, JsonModel):
            return decoder
        else:
            return None


class BaseClient(Consumer):
    """Base class for SystemLink clients, built on top of `Uplink <https://github.com/prkumar/uplink>`_."""

    def __init__(self, configuration: core.HttpConfiguration, base_path: str = ""):
        """Initialize an instance.

        Args:
            configuration: Defines the web server to connect to and information about how to connect.
            base_path: The base path for all API calls.
        """
        super().__init__(
            base_url=configuration.server_uri + base_path,
            converter=_JsonModelConverter(),
            hooks=[_handle_http_status],
        )
        if configuration.api_keys:
            self.session.headers.update(configuration.api_keys)
