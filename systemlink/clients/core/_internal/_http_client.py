# -*- coding: utf-8 -*-

"""Implementation of HttpClient."""

import json.decoder
import sys
import threading
import typing
import urllib.parse
from typing import Any, Awaitable, Dict, Iterable, Optional, Tuple, Union

from systemlink.clients import core

if sys.version_info >= (3, 6):
    from httpx import AsyncClient, Client, Response as HttpResponse
else:
    from requests import Session as Client, Response as HttpResponse

    AsyncClient = None  # type: Any


class HttpClient:
    """Base client for HTTP connections."""

    def __init__(self, configuration: core.HttpConfiguration) -> None:
        self._server = configuration.server_uri.rstrip("/")

        self._kwargs = {}  # type: Dict[str, Any]
        self._kwargs["headers"] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if configuration.api_keys is not None:
            self._kwargs["headers"].update(configuration.api_keys)
        elif configuration.username is not None and configuration.password is not None:
            self._kwargs["auth"] = (configuration.username, configuration.password)
        if configuration.cert_path:
            self._kwargs["verify"] = str(configuration.cert_path)

        # Keep a client per thread
        # - https://toolbelt.readthedocs.io/en/latest/threading.html
        # - "there are still a couple corner cases where it isn't perfectly threadsafe"
        self._clients = {}  # type: Dict[int, Client]
        self._aclients = {}  # type: Dict[int, AsyncClient]

    def at_uri(self, uri: str) -> "_HttpClientAtUri":
        """Get a client interface for which all queries are relative to ``uri``."""
        return _HttpClientAtUri(self, self._server + uri)

    @property
    def _client(self) -> Client:
        thread_id = threading.get_ident()
        if thread_id not in self._clients:
            if sys.version_info >= (3, 6):
                client = Client(**self._kwargs)
            else:
                client = Client()
                for k, v in self._kwargs.items():
                    setattr(client, k, v)
            self._clients[thread_id] = client
        return self._clients[thread_id]

    @property
    def _async_client(self) -> AsyncClient:
        thread_id = threading.get_ident()
        if thread_id not in self._clients:
            if sys.version_info < (3, 6):
                raise RuntimeError("async support is only available for python 3.6+")
            self._aclients[thread_id] = AsyncClient(**self._kwargs)
        return self._aclients[thread_id]


class _HttpClientAtUri:
    """Interface to HttpClient for while all queries are relative to a given uri."""

    def __init__(self, client: HttpClient, uri: str) -> None:
        self._client = client
        self._base_uri = uri

    @property
    def as_async(self) -> "_AsyncHttpClientAtUri":
        """An async version of the client."""
        if sys.version_info < (3, 6):
            raise RuntimeError("async support is only available for python 3.6+")
        return _AsyncHttpClientAtUri(self._client, self._base_uri)

    def _request(
        self,
        method: str,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Tuple[Any, HttpResponse]:
        client = self._client._client
        uri, params2 = _expand_uri_params(uri, params)
        response = client.request(method, uri, json=data, params=params2)
        return _handle_response(response, method, uri), response

    def get(
        self, uri: str, *, params: Optional[Dict[str, Optional[str]]] = None
    ) -> Tuple[Any, HttpResponse]:
        """Perform a GET request."""
        return self._request("GET", self._base_uri + uri, params=params)

    def head(
        self, uri: str, *, params: Optional[Dict[str, Optional[str]]] = None
    ) -> Tuple[Any, HttpResponse]:
        """Perform a HEAD request."""
        return self._request("HEAD", self._base_uri + uri, params=params)

    def delete(
        self, uri: str, *, params: Optional[Dict[str, Optional[str]]] = None
    ) -> Tuple[Any, HttpResponse]:
        """Perform a DELETE request."""
        return self._request("DELETE", self._base_uri + uri, params=params)

    def post(
        self,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Tuple[Any, HttpResponse]:
        """Perform a POST request."""
        return self._request("POST", self._base_uri + uri, params=params, data=data)

    def put(
        self,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Tuple[Any, HttpResponse]:
        """Perform a PUT request."""
        return self._request("PUT", self._base_uri + uri, params=params, data=data)

    def patch(
        self,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Tuple[Any, HttpResponse]:
        """Perform a PATCH request."""
        return self._request("PATCH", self._base_uri + uri, params=params, data=data)

    @property
    def base_uri(self) -> str:
        return self._base_uri


class _AsyncHttpClientAtUri:
    """Interface to HttpClient for while all queries are relative to a given uri."""

    def __init__(self, client: HttpClient, uri: str) -> None:
        self._client = client
        self._base_uri = uri

    async def _request(
        self,
        method: str,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Tuple[Any, HttpResponse]:
        client = self._client._async_client
        uri, params2 = _expand_uri_params(uri, params)
        response = await client.request(method, uri, json=data, params=params2)
        return _handle_response(response, method, uri), response

    def get(
        self, uri: str, *, params: Optional[Dict[str, Optional[str]]] = None
    ) -> Awaitable[Tuple[Any, HttpResponse]]:
        """Perform a GET request."""
        return self._request("GET", self._base_uri + uri, params=params)

    def head(
        self, uri: str, *, params: Optional[Dict[str, Optional[str]]] = None
    ) -> Awaitable[Tuple[Any, HttpResponse]]:
        """Perform a HEAD request."""
        return self._request("HEAD", self._base_uri + uri, params=params)

    def delete(
        self, uri: str, *, params: Optional[Dict[str, Optional[str]]] = None
    ) -> Awaitable[Tuple[Any, HttpResponse]]:
        """Perform a DELETE request."""
        return self._request("DELETE", self._base_uri + uri, params=params)

    def post(
        self,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Awaitable[Tuple[Any, HttpResponse]]:
        """Perform a POST request."""
        return self._request("POST", self._base_uri + uri, params=params, data=data)

    def put(
        self,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Awaitable[Tuple[Any, HttpResponse]]:
        """Perform a PUT request."""
        return self._request("PUT", self._base_uri + uri, params=params, data=data)

    def patch(
        self,
        uri: str,
        *,
        params: Optional[Dict[str, Optional[str]]] = None,
        data: Optional[Union[Dict[str, Any], Iterable[Any]]] = None
    ) -> Awaitable[Tuple[Any, HttpResponse]]:
        """Perform a PATCH request."""
        return self._request("PATCH", self._base_uri + uri, params=params, data=data)

    @property
    def base_uri(self) -> str:
        return self._base_uri


def _expand_uri_params(
    uri: str, params: Optional[Dict[str, Optional[str]]]
) -> Tuple[str, Optional[Dict[str, str]]]:
    """Expand any params in uri with a url-encoded version of the corresponding value in ``params``.

    Any matched params will be removed from params. Any unmatched params will be left
    as-is in the uri.

    For example, uri can be "/tags/{path}" and params can be {"path": "foo/bar"},
    resulting in the uri "/tags/foo%2Fbar" and params={}.
    """
    if params is None:
        return uri, params
    params2 = {k: v for k, v in params.items() if v is not None}
    if "{" not in uri:
        return uri, params2
    for param, value in params.items():
        param_match = "{" + param + "}"
        if param_match in uri:
            uri = uri.replace(param_match, urllib.parse.quote(value or "", safe=""))
            del params2[param]
    return uri, params2


def _handle_response(response: HttpResponse, method: str, uri: str) -> Any:
    try:
        data = response.json() if len(response.text) > 0 else None
        non_json_error = None
    except json.decoder.JSONDecodeError as ex:
        # For error statuses (e.g. 403), if the body isn't JSON, raise an ApiException
        # with the body text as a message
        data = None
        non_json_error = response.text

        # But if this was supposed to be a non-error, raise the decode error
        if 200 <= response.status_code < 300:
            # TODO: This works around Bug 369006 where SystemLink Cloud returns non-JSON
            # text for some APIs (but only those for which no response is necessary)
            if response.status_code == 200 and response.text in ("Success", "OK"):
                data = None
            elif response.status_code == 201 and response.text.startswith("Created"):
                data = None
            else:
                raise json.decoder.JSONDecodeError(
                    "Error from <{} {}>: {}\n\nResponse text:\n  {}".format(
                        method, uri, ex.args[0], response.text.replace("\n", "\n  ")
                    ),
                    ex.doc,
                    ex.pos,
                ) from None

    if not 200 <= response.status_code < 300:
        msg = "Server responded with <{} {}> when calling {} ({})".format(
            response.status_code,
            getattr(response, "reason_phrase", None) or getattr(response, "reason"),
            method,
            uri,
        )
        if non_json_error:
            msg += ":\n\n" + non_json_error

        if data:
            err_dict = typing.cast(Dict[str, Any], data).get("error", {})
            err_obj = core.ApiError.from_json_dict(err_dict) if err_dict else None
        else:
            err_obj = None

        raise core.ApiException(
            msg, error=err_obj, http_status_code=response.status_code
        )

    return data
