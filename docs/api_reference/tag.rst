.. _api_tag_page:

nisystemlink.clients.tag
======================

Workspace configuration
-----------------------

Pass an :class:`~nisystemlink.clients.core.HttpConfiguration` with a workspace ID
to :class:`~nisystemlink.clients.tag.TagManager` to use that workspace for tag
metadata, values, queries (including subsequent pages), selections, subscriptions,
and buffered writes::

    from nisystemlink.clients.core import HttpConfiguration
    from nisystemlink.clients.tag import DataType, TagManager

    configuration = HttpConfiguration(
        "https://systemlink.example.com", workspace="your-workspace-id"
    )
    manager = TagManager(configuration)
    tag = manager.open("MyTags.Example", DataType.DOUBLE, create=True)
    with manager.create_writer(buffer_size=10) as writer:
        writer.write(tag.path, tag.data_type, 3.5)

When no workspace is configured, the existing server defaults are preserved.

.. automodule:: nisystemlink.clients.tag
   :members:
   :inherited-members:
   :imported-members:
