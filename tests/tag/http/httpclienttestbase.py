import asyncio
from unittest import mock

from systemlink.clients.core._internal._http_client import (
    _AsyncHttpClientAtUri,
    _HttpClientAtUri,
    HttpClient,
)


class HttpClientTestBase:
    def setup_method(self, method):
        is_async = asyncio.iscoroutinefunction(method)
        self._client = MockHttpClient(is_async)

    @classmethod
    def _get_mock_request(cls, side_effects):
        def mock_request(method, uri, params=None, data=None):
            ret = side_effects.pop(0)
            if isinstance(ret, Exception):
                raise ret

            return ret, MockResponse(method, uri)

        return mock_request


class MockResponse:
    class MockRequest:
        def __init__(self, method, uri):
            self.method = method
            self.url = uri

    def __init__(self, method, uri):
        self.request = self.MockRequest(method, uri)


class MockHttpClient(HttpClient):
    def __init__(self, is_async):
        # don't call super().__init__

        self.__is_async = is_async

        self.all_requests = mock.Mock()

    def at_uri(self, uri):
        return MockHttpClientAtUri(self, uri, self.__is_async)

    @property
    def _client(self):
        raise NotImplementedError()

    @property
    def _async_client(self):
        raise NotImplementedError()


class MockHttpClientAtUri(_HttpClientAtUri):
    def __init__(self, client, uri, is_async):
        super().__init__(client, uri)
        self.__client = client
        self.__base_uri = uri
        self.__is_async = is_async

    @property
    def as_async(self):
        # Note: the base class raises a RuntimeError here if running on py35; if we want
        # to test that, we'll need to do it some other way, but it's easier on the tests
        # if we just pretend that it would work on py35, too
        return MockAsyncHttpClientAtUri(self.__client, self.__base_uri, self.__is_async)

    def _request(self, method, *args, **kwargs):
        if method != "DELETE":  # don't error on DELETE -- it's used during cleanup
            assert not self.__is_async, "Non-async method called in async test"
        return self._client.all_requests(method, *args, **kwargs)


class MockAsyncHttpClientAtUri(_AsyncHttpClientAtUri):
    def __init__(self, client, uri, is_async):
        super().__init__(client, uri)
        self.__client = client
        self.__base_uri = uri
        self.__is_async = is_async

    async def _request(self, *args, **kwargs):
        assert self.__is_async, "async method called in non-async test"
        return self._client.all_requests(*args, **kwargs)
