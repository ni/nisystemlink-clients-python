"""Integration tests for FeedsClient."""

from pathlib import Path
from random import randint
from typing import BinaryIO, Callable

import pytest
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.feeds import FeedsClient
from nisystemlink.clients.feeds.models import CreateFeedRequest, Platform


FEED_DESCRIPTION = "Sample feed for uploading packages"
PACKAGE_PATH = str(
    Path(__file__).parent.resolve()
    / "test_files"
    / "sample-measurement_0.5.0_windows_x64.nipkg"
)


@pytest.fixture(scope="class")
def client(enterprise_config) -> FeedsClient:
    """Fixture to create a FeedsClient instance."""
    return FeedsClient(enterprise_config)


@pytest.fixture(scope="class")
def create_feed(client: FeedsClient):
    """Fixture to return a object that creates feed."""
    feed_ids = []

    def _create_feed(feed):
        response = client.create_feed(feed)
        feed_ids.append(response.id)
        return response

    yield _create_feed

    # deleting the created feeds.
    for feed_id in feed_ids:
        client.delete_feed(id=feed_id)


@pytest.fixture(scope="class")
def create_feed_request():
    """Fixture to create a request body of create feed API."""

    def _create_feed_request(feed_name: str, description: str, platform: Platform):
        feed_request = CreateFeedRequest(
            name=feed_name,
            platform=platform,
            description=description,
        )
        return feed_request

    yield _create_feed_request


@pytest.fixture(scope="class")
def binary_pkg_file_data() -> BinaryIO:
    """Fixture to return package file in binary format."""
    package_data = open(PACKAGE_PATH, "rb")
    return package_data


@pytest.fixture(scope="class")
def invalid_id() -> str:
    """Generate a invalid id."""
    id = f"Invalid-id-{randint(1000, 9999)}"
    return id


@pytest.fixture(scope="class")
def get_feed_name():
    """Generate a feed name."""
    name = "testfeed_"
    feed_count = 0

    def _get_feed_name():
        nonlocal feed_count
        feed_count += 1
        feed_name = name + str(feed_count)
        return feed_name

    yield _get_feed_name


@pytest.mark.enterprise
@pytest.mark.integration
class TestFeedsClient:
    def test__create_feed_windows_platform__succeeds(
        self,
        create_feed: Callable,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case of a completely successful create feed API for Windows platform."""
        feed_name = get_feed_name()
        request_body = create_feed_request(
            feed_name=feed_name,
            description=FEED_DESCRIPTION,
            platform=Platform.WINDOWS,
        )
        response = create_feed(request_body)

        assert response.id is not None
        assert response.workspace is not None
        assert response.name == feed_name
        assert response.platform == Platform.WINDOWS
        assert response.description == FEED_DESCRIPTION

    def test__create_feed_linux_platform__succeeds(
        self,
        create_feed: Callable,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case of a completely successful create feed API for Linux platform."""
        feed_name = get_feed_name()
        request_body = create_feed_request(
            feed_name=feed_name,
            description=FEED_DESCRIPTION,
            platform=Platform.NI_LINUX_RT,
        )
        response = create_feed(request_body)

        assert response.id is not None
        assert response.workspace is not None
        assert response.name == feed_name
        assert response.platform == Platform.NI_LINUX_RT
        assert response.description == FEED_DESCRIPTION

    def test__query_feeds_windows_platform__succeeds(
        self,
        client: FeedsClient,
        create_feed: Callable,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case for querying available feeds for Windows platform."""
        create_feed_request_body = create_feed_request(
            feed_name=get_feed_name(),
            description=FEED_DESCRIPTION,
            platform=Platform.WINDOWS,
        )
        create_feed_resp = create_feed(create_feed_request_body)
        assert create_feed_resp.id is not None

        query_feed_resp = client.query_feeds(platform=Platform.WINDOWS)
        assert query_feed_resp is not None

    def test__query_feeds_linux_platform__succeeds(
        self,
        client: FeedsClient,
        create_feed: Callable,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case for querying available feeds for Linux platform."""
        create_feed_request_body = create_feed_request(
            feed_name=get_feed_name(),
            description=FEED_DESCRIPTION,
            platform=Platform.NI_LINUX_RT,
        )
        create_feed_resp = create_feed(create_feed_request_body)
        assert create_feed_resp.id is not None

        query_feed_resp = client.query_feeds(platform=Platform.NI_LINUX_RT)
        assert query_feed_resp is not None

    def test__query_feeds__invalid_workspace_raises(
        self,
        client: FeedsClient,
        invalid_id: str,
    ):
        """Test the case of query feeds API with invalid workspace id."""
        with pytest.raises(ApiException, match="UnauthorizedWorkspaceError"):
            client.query_feeds(workspace=invalid_id)

    def test__upload_package__succeeds(
        self,
        client: FeedsClient,
        create_feed: Callable,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case of upload package to feed."""
        create_feed_request_body = create_feed_request(
            feed_name=get_feed_name(),
            description=FEED_DESCRIPTION,
            platform=Platform.WINDOWS,
        )
        create_feed_resp = create_feed(create_feed_request_body)
        assert create_feed_resp.id is not None

        upload_pacakge_rsp = client.upload_package(
            package_file_path=PACKAGE_PATH,
            feed_id=create_feed_resp.id,
            overwrite=True,
        )
        assert upload_pacakge_rsp is not None

    def test__upload_package_content__succeeds(
        self,
        client: FeedsClient,
        create_feed: Callable,
        create_feed_request: Callable,
        binary_pkg_file_data: BinaryIO,
        get_feed_name: Callable,
    ):
        """Test the case of upload package content to feed."""
        create_feed_request_body = create_feed_request(
            feed_name=get_feed_name(),
            description=FEED_DESCRIPTION,
            platform=Platform.WINDOWS,
        )
        create_feed_resp = create_feed(create_feed_request_body)
        assert create_feed_resp.id is not None

        upload_pacakge_rsp = client.upload_package_content(
            package=binary_pkg_file_data,
            feed_id=create_feed_resp.id,
            overwrite=True,
        )
        assert upload_pacakge_rsp is not None

    def test__upload_package_content__invalid_feed_id_raises(
        self,
        client: FeedsClient,
        binary_pkg_file_data: BinaryIO,
        invalid_id: str,
    ):
        """Test the case of uploading package to Invalid feed."""
        with pytest.raises(ApiException, match="FeedNotFoundError"):
            client.upload_package_content(
                package=binary_pkg_file_data,
                feed_id=invalid_id,
            )

    def test__delete_windows_feed__succeeds(
        self,
        client: FeedsClient,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case of deleting Windows feed."""
        create_feed_request_body = create_feed_request(
            feed_name=get_feed_name(),
            description=FEED_DESCRIPTION,
            platform=Platform.WINDOWS,
        )
        create_feed_resp = client.create_feed(create_feed_request_body)
        assert create_feed_resp.id is not None

        delete_feed_resp = client.delete_feed(id=create_feed_resp.id)
        assert delete_feed_resp is None

    def test__delete__linux_feed__succeeds(
        self,
        client: FeedsClient,
        create_feed_request: Callable,
        get_feed_name: Callable,
    ):
        """Test the case of deleting Linux feed."""
        create_feed_request_body = create_feed_request(
            feed_name=get_feed_name(),
            description=FEED_DESCRIPTION,
            platform=Platform.NI_LINUX_RT,
        )
        create_feed_resp = client.create_feed(create_feed_request_body)
        assert create_feed_resp.id is not None

        delete_feed_resp = client.delete_feed(id=create_feed_resp.id)
        assert delete_feed_resp is None
