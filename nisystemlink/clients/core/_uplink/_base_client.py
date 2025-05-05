# mypy: disable-error-code = misc

from typing import Any, Callable, Dict, get_origin, Optional, Type, Union

import requests
from nisystemlink.clients import core
from pydantic import TypeAdapter
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
            err_obj = core.ApiError.model_validate(content["error"])
        else:
            err_obj = None

        raise core.ApiException(
            msg, error=err_obj, http_status_code=response.status_code
        )
    except JSONDecodeError:
        if response.text:
            msg += ":\n\n" + response.text
        raise core.ApiException(msg, http_status_code=response.status_code)


_type_adapters: Dict[Type, TypeAdapter] = dict()


class _JsonModelConverter(converters.Factory):
    """A converter that converts between JSON and Pydantic models."""

    def __init__(self) -> None:
        super().__init__()

    def create_request_body_converter(
        self, _class: Type, _: commands.RequestDefinition
    ) -> Optional[Callable[[JsonModel], Dict]]:
        def encoder(model: JsonModel) -> Dict:
            return model.model_dump(mode="json", by_alias=True, exclude_unset=True)

        if utils.is_subclass(_class, JsonModel):
            return encoder
        else:
            return None

    def create_response_body_converter(
        self, _class: Type, _: commands.RequestDefinition
    ) -> Optional[Callable[[Response], Any]]:
        def decoder(response: Union[Response, Any]) -> Any:
            if response is None:
                return None

            adapter = _type_adapters[_class]
            if isinstance(response, Response):
                if response.status_code == 204:
                    return None
                return adapter.validate_json(response.text, by_alias=True, strict=True)
            else:
                # In cases where a return_key is specified, the response will already be parsed into a dict
                return adapter.validate_python(response, by_alias=True, strict=True)

        origin = get_origin(_class)
        modelable_origin = origin is Union or origin is dict or origin is list
        if modelable_origin or utils.is_subclass(_class, JsonModel):
            if _type_adapters.get(_class) is None:
                _type_adapters[_class] = TypeAdapter(_class)
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
        session = requests.Session()
        session.verify = configuration.verify

        super().__init__(
            base_url=configuration.server_uri + base_path,
            converter=_JsonModelConverter(),
            hooks=[_handle_http_status],
            client=session,
        )
        if configuration.api_keys:
            self.session.headers.update(configuration.api_keys)
