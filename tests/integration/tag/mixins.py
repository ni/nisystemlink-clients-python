# noqa: D104
# -*- coding: utf-8 -*-

import uuid

import pytest  # type: ignore
from systemlink.clients import tag as tbase
from systemlink.clients.core._internal._http_client import HttpClient


class TagBaseMixin:
    @pytest.fixture
    def generate_each_tag_type(self, generate_tag_paths, request, setup_tag_manager):
        """Fixture to generate a tag of each type with a common path prefix and create the tags on the server.

        The tags will be automatically deleted at the end of the current test.

        Returns:
            A 2-tuple containing:
            - The generated tags.
            - The common prefix for each of the generated tags, including the trailing dot.

        Raises:
            systemlink.clients.core.ApiException: if the API call fails.
        """

        def fn():
            # Create a tag of each data type.
            data_types = [t for t in tbase.DataType if t != tbase.DataType.UNKNOWN]
            paths, prefix = generate_tag_paths(len(data_types))
            tags = [tbase.TagData(p, t) for (p, t) in zip(paths, data_types)]
            for tag in tags:
                tag.collect_aggregates = True

            request.cls.tag_manager.update(tags)
            return tags, prefix

        return fn

    @pytest.fixture
    def generate_tag_path(self, request, setup_tag_manager):
        """Fixture to generate a tag path to be used within the scope of a single test.

        Args:
            suffix (Optional[str]): Optional suffix to add to the tag for informational
                purposes.

        Returns:
            The generated tag path
        """

        def fn(suffix=None):
            test_class = request.cls.__name__  # .rsplit(".", 1)[-1]
            test_name = request.node.originalname or request.node.name
            path = ".".join(("test", test_class, test_name, str(uuid.uuid4())))
            if suffix:
                path += "." + suffix
            request.cls.created_tags.append(path)
            return path

        return fn

    @pytest.fixture
    def generate_tag_paths(self, request, setup_tag_manager):
        """Generates tag paths to be used within the scope of a single test.

        Args:
            count: The number of paths to generate.

        Returns:
            A 2-tuple containing:
            - The generated tag paths.
            - The common prefix for each of the generated paths, including the trailing dot.
        """

        def fn(count):
            test_class = request.cls.__name__  # .rsplit(".", 1)[-1]
            test_name = request.node.originalname or request.node.name
            prefix = ".".join(("test", test_class, test_name, str(uuid.uuid4()), ""))
            paths = [prefix + str(x) for x in range(count)]
            request.cls.created_tags += paths
            return paths, prefix

        return fn


@pytest.mark.cloud
@pytest.mark.integration
class CloudMixin(TagBaseMixin):
    @pytest.fixture(scope="class", autouse=True)
    def setup_tag_manager(self, verified_tag_config, request):
        request.cls.tag_manager = tbase.TagManager(verified_tag_config)
        request.cls.created_tags = []
        yield
        if request.cls.created_tags:
            request.cls.tag_manager.delete(request.cls.created_tags)

    @pytest.fixture(scope="class")
    def verified_tag_config(self, cloud_config):
        # Verify that we can successfully use the tags API with this config
        client = HttpClient(cloud_config)
        tags = client.at_uri("/nitag/v2")
        tags.get("/tags", params={"path": ""})

        return cloud_config


@pytest.mark.webserver
@pytest.mark.integration
class ServerMixin(TagBaseMixin):
    @pytest.fixture(scope="class", autouse=True)
    def setup_tag_manager(self, verified_tag_config, request):
        request.cls.tag_manager = tbase.TagManager(verified_tag_config)
        request.cls.created_tags = []
        yield
        if request.cls.created_tags:
            request.cls.tag_manager.delete(request.cls.created_tags)

    @pytest.fixture(scope="class")
    def verified_tag_config(self, server_config):
        # Verify that we can successfully use the tags API with this config
        client = HttpClient(server_config)
        tags = client.at_uri("/nitag/v2")
        tags.get("/tags", params={"path": ""})

        return server_config
